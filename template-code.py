### TEAM MEMBERS
## MEMBER 1: 210050006
## MEMBER 2: 210050156
## MEMBER 3: 210050030


from z3 import *
import sys

file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	matrix = []
	for line in f:
		matrix.append([int(x) for x in line.split()])

s = Solver()

# Set s to the required formula

Inputs = []
States=[]

for i in range(T):
	tmp=[]
	tmp.append(Bool(f'in_0_{i}'))
	tmp.append(Int(f'in_1_{i}'))
	tmp.append(Bool(f'in_2_{i}'))
	Inputs.append(tmp)

	s.add(tmp[1]>=0, tmp[1]<n)

	state=[]
	for j in range(n):
		row=[]
		for k in range(n):
			var= Int(f'S_{i}_x_{j}_{k}')
			row.append(var)
			s.add(var>=1,var<=n*n)
		
		state.append(row)

	States.append(state)

st=States[0]
for i in range(n):
	for j in range(n):
		s.add(st[i][j]==matrix[i][j])




for i in range(T-1):
	inp=Inputs[i]

	for j in range(n):
		
		for k in range(n):

			#Row Left Shift
			s.add(Implies(And(inp[0]==False, inp[1]==j, inp[2]==False), States[i+1][j][k]==States[i][j][(k+1)%n]))
			s.add(Implies(And(inp[0]==False, inp[1]!=j, inp[2]==False), States[i+1][j][k]==States[i][j][k]))

			#Row Right Shift
			s.add(Implies(And(inp[0]==False, inp[1]==j, inp[2]==True), States[i+1][j][(k+1)%n]==States[i][j][k]))
			s.add(Implies(And(inp[0]==False, inp[1]!=j, inp[2]==True), States[i+1][j][k]==States[i][j][k]))

			#Column down Shift
			s.add(Implies(And(inp[0]==True, inp[1]==j, inp[2]==False), States[i+1][(k+1)%n][j]==States[i][k][j]))
			s.add(Implies(And(inp[0]==True, inp[1]!=j, inp[2]==False), States[i+1][k][j]==States[i][k][j]))

			#Column Up Shift
			s.add(Implies(And(inp[0]==True, inp[1]==j, inp[2]==True), States[i+1][k][j]==States[i][(k+1)%n][j]))
			s.add(Implies(And(inp[0]==True, inp[1]!=j, inp[2]==True), States[i+1][k][j]==States[i][k][j]))
		

x = s.check()
print(x)
if x == sat:
	m = s.model()
	for i in range(T-1):
		inp=Inputs[i]

		
	# Output the moves