from itertools import chain

class Sentence:
	def toCNF(self):
		pass
	def size(self):
		pass

class Atom(Sentence):
	def __init__(self, value):
		self.value = value
	def toCNF(self):
		return And([Or([self])])
	def size(self):
		return 1
	def atoms(self):
		return set([self.value])
	def __str__(self):
		return self.value

class Not(Sentence):
	def __init__(self, clause):
		self.clause = clause
	def toCNF(self):
		clause_cnf = self.clause.toCNF()
		disj = Or([And(disj.clauses) for disj in clause_cnf.clauses])
		conj = disj.toCNF()
		for disj in conj.clauses:
			disj.clauses = [atom.clause if type(atom) == Not else Not(atom) for atom in disj.clauses]
		return conj
	def size(self):
		return self.clause.size()
	def atoms(self):
		return self.clause.atoms()
	def __str__(self):
		return "~" + str(self.clause)

class And(Sentence):
	def __init__(self, clauses):
		self.clauses = clauses
	def toCNF(self):
		conjs = And([])
		for clause in self.clauses:
			conjs.clauses += clause.toCNF().clauses
		return simplify_cnf(conjs)
	def size(self):
		return sum(clause.size for clause in self.clauses)
	def atoms(self):
		return set(chain.from_iterable(clause.atoms() for clause in self.clauses))
	def __str__(self):
		if not self.clauses:
			return 'True'
		return '(' + ' & '.join(map(str, self.clauses)) + ')'

class Or(Sentence):
	def __init__(self, clauses):
		self.clauses = clauses
	def toCNF(self):
		clauses_cnf = [clause.toCNF() for clause in self.clauses]
		def iter(index, curr_disj):
			if index == len(clauses_cnf):
				yield Or(curr_disj)
			else:
				for disj in clauses_cnf[index].clauses:
					for res_disj in iter(index + 1, curr_disj + disj.clauses):
						yield res_disj
		conjs = And(list(iter(0, [])))
		return simplify_cnf(conjs)
	def size(self):
		return sum(clause.size() for clause in self.clauses)
	def atoms(self):
		return set(chain.from_iterable(clause.atoms() for clause in self.clauses))
	def __str__(self):
		if not self.clauses:
			return 'False'
		return '(' + ' | '.join(map(str, self.clauses)) + ')'

class Implication(Sentence):
	def __init__(self, left, right):
		self.left = left
		self.right = right
	def toCNF(self):
		return Or([Not(self.left), self.right]).toCNF()
	def size(self):
		return self.left.size() + self.right.size()
	def atoms(self):
		return self.left.atoms() | self.right.atoms()
	def __str__(self):
		return '(' + str(self.left) + ' => ' + str(self.right) + ')'

class Equivalence(Sentence):
	def __init__(self, left, right):
		self.left = left
		self.right = right
	def toCNF(self):
		return And([Implication(self.left, self.right), Implication(self.right, self.left)]).toCNF()
	def size(self):
		return self.left.size() + self.right.size()
	def atoms(self):
		return self.left.atoms() | self.right.atoms()
	def __str__(self):
		return '(' + str(self.left) + ' <=> ' + str(self.right) + ')'

def simplify_disj(disj):
	atoms = []
	atoms_signs = {}
	for atom in disj.clauses:
		sign = True
		if type(atom) == Not:
			sign = False
			value = atom.clause.value
		else:
			value = atom.value
		if value in atoms_signs:
			if sign != atoms_signs[value]:
				return None
		else:
			atoms_signs[value] = sign
			atoms.append(atom)
	return Or(atoms)

def simplify_cnf(conj):
	clauses = map(simplify_disj, conj.clauses)
	clauses = list(filter(lambda disj: disj != None, clauses))
	for disj in clauses:
		if not disj.clauses:
			clauses = [Or([])]
	return And(clauses)