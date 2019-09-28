from KenKenSolver import KenKenSolver
import time

kenken = KenKenSolver()
kenken.get_input()
start_time = time.time()
kenken.backtrack(0)
kenken.bestBacktracking(0)

print "\nLocal Search: "
kenken.localSearch()