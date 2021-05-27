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
    total_pi = np.zeros(1)
    data = np.zeros(1)
    data[0] = calcPi(840, comm.Get_size(), rank)

comm.Barrier()
tcalc=MPI.Wtime()

comm.Reduce(data, total_pi, op=MPI.SUM, root=0)
tfinal=MPI.Wtime()

ttotalcal = tcalc - tinicial
ttotal = tfinal - tinicial

if rank == 0:
    #print("Pelo somatorio do metodo Reduce, o valor de pi =", total_pi[0])
    print("Pelo somatorio do metodo Reduce, o valor de pi = {}\nLevou {} para a realizaçao do calculo e {} contando com o processo de comunicacao"
    .format(total_pi[0], ttotalcal, ttotal))