"""plogic

Usage:
	plogic.py <input_file> [--cnf] [--dpll]
"""
from docopt import docopt

from logic_parser import LogicParser
from dpll import dpll

args = docopt(__doc__)

def read(file):
	with open(file) as f:
		return f.read()

tree = LogicParser().parse(read(args['<input_file>']))

print('Parsed expression :', tree)
if args['--cnf']:
	print('CNF expression :', tree.toCNF())
if args['--dpll']:
	print('DPLL solutions :')
	for sol in dpll(tree.toCNF()):
		print(', '.join(atom + ': ' + str(value) for atom, value in sol.items()))