from collections import defaultdict, deque
import itertools
from logic_structures import Not
from layered_dict import LayeredDict, LayeredListOfDict

class RemainingDict(LayeredDict):
	def pre_init(self):
		super().pre_init()
		self.remaining = sum(atom == False for atom in self.d.values())
		self.remaining_layers = []
	def add_layer(self):
		super().add_layer()
		self.remaining_layers.append(self.remaining)
	def pop_layer(self):
		super().pop_layer()
		self.remaining = self.remaining_layers[-1]
		self.remaining_layers.pop()
	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		self.remaining -= 1
	def valid(self):
		return self.remaining == 0
		
class DpllStructure:
	def __init__(self, cnf):
		self._atom_to_disj_indices = defaultdict(list)
		self._disj_index_to_atoms_sign = [{} for i in range(len(cnf.clauses))]
		for disj_index, disj in enumerate(cnf.clauses):
			for signed_atom in disj.clauses:
				sign = type(signed_atom) != Not
				for atom in signed_atom.atoms():
					self._atom_to_disj_indices[atom].append(disj_index)
					self._disj_index_to_atoms_sign[disj_index][atom] = sign
		self._disj_index_to_atoms_sign = LayeredListOfDict(self._disj_index_to_atoms_sign)
		self.valuation = LayeredDict({atom : None for atom in cnf.atoms()})
		self.disj_done = RemainingDict({i : False for i in range(len(cnf.clauses))})
	def disj_indices(self, atom):
		return self._atom_to_disj_indices[atom]
	def find_atoms_sign(self, disj_index):
		return self._disj_index_to_atoms_sign[disj_index]
	def all_atoms(self):
		return self._disj_index_to_atoms_sign
	def add_layer(self):
		self._disj_index_to_atoms_sign.add_layer()
		self.valuation.add_layer()
		self.disj_done.add_layer()
	def pop_layer(self):
		self._disj_index_to_atoms_sign.pop_layer()
		self.valuation.pop_layer()
		self.disj_done.pop_layer()

def dpll(cnf):
	data = DpllStructure(cnf)

	init_valuations = []
	for atoms in data.all_atoms():
		if len(atoms) == 1:
			atom, sign = list(atoms.items())[0]
			init_valuations.append((atom, sign))
	
	def choose_atom():
		for atom, val in data.valuation.items():
			if val == None:
				return atom
		return None
	
	def apply_valuation(atom, sign, new_valuations):
		data.valuation[atom] = sign
		for disj_index in data.disj_indices(atom):
			if data.disj_done[disj_index]:
				continue
			atoms_sign = data.find_atoms_sign(disj_index)
			true_sign = atoms_sign[atom]
			if true_sign == sign:
				data.disj_done[disj_index] = True
			else:
				atoms_sign.pop(atom)
				if len(atoms_sign) == 1:
					single_atom, single_sign = atoms_sign.popitem()
					new_valuations.appendleft((single_atom, single_sign))
					data.disj_done[disj_index] = True

	def dpll_rec(new_valuations_list):
		data.add_layer()
		new_valuations = deque(new_valuations_list)
		while new_valuations:
			new_atom, new_sign = new_valuations.pop()
			old_valuation = data.valuation[new_atom]
			if old_valuation != None:
				if old_valuation == new_sign:
					continue
				else:
					data.pop_layer()
					return
			apply_valuation(new_atom, new_sign, new_valuations)

		if data.disj_done.valid():
			yield dict(data.valuation.d)
		else:
			next_atom = choose_atom()
			yield from itertools.chain(dpll_rec([(next_atom, False)]), dpll_rec([(next_atom, True)]))
		data.pop_layer()

	yield from dpll_rec(init_valuations)