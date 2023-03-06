### TEAM MEMBERS
## MEMBER 1: 210050006
## MEMBER 2: 210050156
## MEMBER 3: 210050030


from z3 import *
import sys
import numpy as np

file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	matrix = []
	for line in f:
		matrix.append([int(x) for x in line.split()])

# print(matrix)

s = Solver()

# Set s to the required formula
solution = [[[Int(f"s{k}x{i}y{j}") for j in range(n)] for i in range(n)] for k in range(T+1)]
s.add(And([solution[0][i][j] == matrix[i][j] for j in range(n) for i in range(n)]))
s.add(Or(And([solution[T][i][j] == n*i+j+1 for j in range(n) for i in range(n)]), And([solution[T-1][i][j] == n*i+j+1 for j in range(n) for i in range(n)])))

for i in range(T):
	transition = []
	for rc in range(n):
		left, right, up, down = [], [], [], []
		for j in range(n):
			for k in range(n):
				left.append(solution[i+1][j][k] == solution[i][j][k if j != rc else (k+1)%n])
				right.append(solution[i+1][j][k if j != rc else (k+1)%n] == solution[i][j][k])
				up.append(solution[i+1][j][k] == solution[i][j if k != rc else (j+1)%n][k])
				down.append(solution[i+1][j if k != rc else (j+1)%n][k] == solution[i][j][k])
		transition.append(And(left))
		transition.append(And(right))
		transition.append(And(up))
		transition.append(And(down))

	s.add(Or(transition))

x = s.check()
print(x)
if x == sat:
	m = s.model()
	
	# Output the moves
	moves = [[[0 for i in range(n)] for j in range(n)] for k in range(T+1)]
	for var in m:
		name = str(var)
		s, x, y = int(name[1]), int(name[3]), int(name[5])
		moves[s][x][y] = m[var]
 
	Tmoves = (np.arange(1, n*n+1).reshape(n, n) == moves[T]).all()
 
	for move in range(T - (not Tmoves)):
		dif = [(i, j) for i in range(n) for j in range(n) if not moves[move][i][j] == moves[move+1][i][j]]
		if dif[0][0] == dif[1][0]:
			row = dif[0][0]
			print(row, end="")
			print("r" if moves[move+1][row][1] == moves[move][row][0] else "l")
		else:
			col = dif[0][1]
			print(col, end="")
			print("d" if moves[move+1][1][col] == moves[move][0][col] else "u")
   