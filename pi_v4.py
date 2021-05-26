from mpi4py import MPI
import numpy as np

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
maq=MPI.Get_processor_name()

def calcPi(M, total, rank):
    sum = 0
    pi = 0
    N = M//total
    begin = (N*(rank + 1)) - (N - 1)
    end = (N*(rank + 1))
    
    for i in range(begin, end+1):
        sum = sum + 1/(1 + np.power((i - 1/2)/M, 2))
    
    pi = 4/M * sum
    return pi

total_pi = np.zeros(1)
data = np.zeros(1)
data[0] = calcPi(840, comm.Get_size(), rank)

comm.Reduce(data, total_pi, op=MPI.SUM, root=0)

if rank == 0:
    print("Pelo somatorio do metodo Reduce, o valor de pi =", total_pi[0])