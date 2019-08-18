## Proposition logic parser and solver

A propositional logic parser and solver made for fun.
It can convert expressions to [CNF](https://en.wikipedia.org/wiki/Conjunctive_normal_form) and solve the [SAT](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem) problem using the [DPLL](https://en.wikipedia.org/wiki/DPLL_algorithm) algorithm.
It uses the [Lark](https://github.com/lark-parser/lark) parser.

### Example

```
$ py src\plogic.py examples\example2.txt --cnf --dpll
Parsed expression : (((((X1 & X2) => ((X2 & ~X3) | ((X4 & ~X2) <=> X3))) & X2) & True) | False)
CNF expression : ((~X1 | ~X2 | ~X3 | X4) & (~X1 | ~X2 | ~X3) & (X2))
DPLL solutions :
X1: False, X3: None, X4: None, X2: True
X1: True, X3: False, X4: None, X2: True
```