from numpy.random import shuffle
from numpy import array

from pygenec import binarray2int

from rnae import RNAE
from rnae import DIAGNOSTICO as dados


entrada = dados[:,0:-2].astype(float)
entrada[:, 0] = ((entrada[:, 0] - entrada[:, 0].min()) /
                 (entrada[:, 0].max() - entrada[:, 0].min())
                 )

saidas = dados[:,-2:].astype(int)

itrain = array(list(range(saidas.shape[0])))
shuffle(itrain)
etrain = entrada[itrain,:]
esaid = saidas[itrain, :]
print(esaid.shape)

n = int(esaid.shape[0] * 0.70)

neurons = [entrada.shape[1], 4, 2]

rna = RNAE(neurons)

rna.treinamento(etrain[0:n, :], esaid[0:n, :],
             tpop=100, gens=1000, bits=16, pmut=0.5, pcruz=0.6, epidemia=150)

rna.salvar_modelo("./modelos/Diagnostico.txt")
rna = RNAE.carregar_modelo("./modelos/Diagnostico.txt")
pred = rna.propagacao(etrain[n:,:])
expct = esaid[n:,:]
expct = binarray2int(expct).reshape((expct.shape[0], 1))
#
pred = binarray2int(pred).reshape((expct.shape[0], 1))
# print("\n")
# print([IRIS_NAME[i] for i in pred.flatten().astype(int)])
# print("\n")
# print([IRIS_NAME[i] for i in expct.flatten().astype(int)])
# print("\n")

accu = 100 * sum(pred == expct) / expct.size
print("Acuracia {} %".format(accu))
