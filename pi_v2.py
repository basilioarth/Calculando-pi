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

comm.Barrier()
tinicial=MPI.Wtime()
for i in range (0, 200):
    result = calcPi(840, comm.Get_size(), rank)
comm.Barrier()
tfinal=MPI.Wtime()

ttotal = tfinal - tinicial

print("O processo {} na maquina {} retornou que o valor parcial de pi = {} em {} segundos".format(rank, maq, result, ttotal))