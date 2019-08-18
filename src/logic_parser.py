from lark import Lark, Transformer, v_args
from logic_structures import Atom, Not, And, Or, Implication, Equivalence

@v_args(inline=True)
class TreeToLogic(Transformer):
	def atom(self, value):
		return Atom(value.value)
	def true(self):
		return And([])
	def false(self):
		return Or([])
	def not_(self, child):
		return Not(child)
	def and_(self, left, right):
		return And([left, right])
	def or_(self, left, right):
		return Or([left, right])
	def implication(self, left, right):
		return Implication(left, right)
	def equivalence(self, left, right):
		return Equivalence(left, right)

class LogicParser:
	def __init__(self):
		self.lark_parser = Lark.open(
			'src/logic.lark', parser = 'lalr', start = 'sentence', transformer = TreeToLogic()
		)
	def parse(self, sentence):
		return self.lark_parser.parse(sentence)