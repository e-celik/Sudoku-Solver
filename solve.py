from pysat.formula import CNF, IDPool
from pysat.card import CardEnc
from pysat.solvers import Solver

vpool = IDPool()
cnf = CNF()

# Create 9x9x9 variables: x_(1,1):1 to x_(9,9):9
vars = [vpool.id(f'({i},{j}):{k}') for i in range(1, 10) for j in range(1, 10) for k in range(1, 10)]


# Get vars at cell i, j. Indexed from 1 to 9
def cell(i, j):
    return vars[(i-1)*9*9+(j-1)*9:(i-1)*9*9+(j)*9]

# Get vars for particular digit in row
def row_digit(i, k):
    return vars[(i-1)*9*9+(k-1):(i)*9*9:9]
    
# Get vars for particular digit in col
def col_digit(j, k):
    return vars[(j-1)*9+(k-1)::9*9]

# Get vars for digit in square, indexed 1 to 3
def square_digit(m, n, k):
    return row_digit((m-1)*3+1, k)[(n-1)*3:n*3] + row_digit((m-1)*3+2, k)[(n-1)*3:n*3] + row_digit((m-1)*3+3, k)[(n-1)*3:n*3]
    
    
# Encode cells: 
cell_clauses = []
for a in range(1, 10):
    for b in range(1, 10):
        enc = CardEnc.equals(lits=cell(a,b), bound=1, vpool=vpool, encoding=0)
        cell_clauses.extend(enc.clauses)
cnf.extend(cell_clauses)
        
# Encode rows:
row_clauses = []
for a in range(1,10):
    for c in range(1,10):
        enc = CardEnc.equals(lits=row_digit(a,c), bound=1, vpool=vpool, encoding=0)
        row_clauses.extend(enc.clauses)
cnf.extend(row_clauses)
        
# Encode cols:
col_clauses = []
for b in range(1,10):
    for c in range(1,10):
        enc = CardEnc.equals(lits=col_digit(b,c), bound=1, vpool=vpool, encoding=0)
        col_clauses.extend(enc.clauses)
cnf.extend(col_clauses)
        
# Encode squares:
square_clauses = []
for a_ in range(1,4):
    for b_ in range(1,4):
        for c in range(1,10):
            enc = CardEnc.equals(lits=square_digit(a_,b_,c), bound=1, vpool=vpool, encoding=0)
            square_clauses.extend(enc.clauses)
cnf.extend(square_clauses)


def add_constraint(i, j, k):
    cnf.extend([[vars[(i-1)*9*9+(j-1)*9+(k-1)]]])

add_constraint(1,3,6)
add_constraint(1,4,3)
add_constraint(1,6,7)
add_constraint(2,3,4)
add_constraint(2,9,5)
add_constraint(3,1,1)
add_constraint(3,6,6)
add_constraint(3,8,8)
add_constraint(3,9,2)
add_constraint(4,1,2)
add_constraint(4,3,5)
add_constraint(4,5,3)
add_constraint(4,7,1)
add_constraint(4,9,6)
add_constraint(5,4,2)
add_constraint(5,7,3)
add_constraint(6,1,9)
add_constraint(6,5,7)
add_constraint(6,9,4)
add_constraint(7,2,5)
add_constraint(8,2,1)
add_constraint(9,3,8)
add_constraint(9,4,1)
add_constraint(9,6,9)
add_constraint(9,8,4)
    

def print_sol(model):
    for i in range(0, 9):
        for j in range(0,9):
            for n in model[i*9*9+j*9:(i)*9*9+(j+1)*9]:
                if n > 0:
                    print((n-1)%9+1, end=' ') 
                    if j == 8:
                        print()
            
with Solver(name='glucose3', bootstrap_with=cnf) as solver:
    if solver.solve():
        print("Solution Found: ")        
        model = solver.get_model()
        print_sol(model)
    else:
        print("No Solution")
        
