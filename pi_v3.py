from mpi4py import MPI
import numpy as np

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
maq=MPI.Get_processor_name()

total_pi = 0
tcalc = 0

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
        data = calcPi(840, comm.Get_size(), rank)

comm.Barrier()
tcalc=MPI.Wtime()

comm.send([data, maq], dest=0)

if rank == 0:
    for i in range(0, comm.Get_size()):
        data = comm.recv(source=i)

        partial_pi = data[0]
        maqSender = data[1]

        total_pi = total_pi + partial_pi
        print("A {} enviou o valor parcial de pi {} calculado pelo processo {} e o valor atual de pi = {}".format(maqSender, partial_pi, i, total_pi))
tfinal=MPI.Wtime()

ttotalcalc = tcalc - tinicial
ttotal = tfinal - tinicial

if rank == 0:
    print("\nO processo {} na maquina {} retornou que o valor final de pi = {}\nLevou {} para a realizaçao do calculo e {} contando com o processo de comunicacao".format(rank, maq, total_pi, ttotalcalc, ttotal))