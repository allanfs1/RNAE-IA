from numpy import loadtxt, array
from numpy.random import randn, choice, shuffle
from pygenec import binarray2int

from rnae import RNAE


arqvinho = "./dados/sonar.csv"
dados = loadtxt(arqvinho, delimiter=",")
print(dados.shape)

itrain = array(list(range(dados.shape[0])))

shuffle(itrain)

dados = dados[itrain,:]

n_trei = int(dados.shape[0] * 0.90)
entrada = dados[:, :-1]

for k in range(entrada.shape[1]):
    entrada[:, k] = ((entrada[:, k] - entrada[:, k].min()) /
                    (entrada[:, k].max() - entrada[:, k].min())
                    )
saida  = dados[:,-1].astype(int)

saida = array([list(map(int, list("{0:4b}".format(s).replace(" ", "0")))) for s in  saida])

neurons = [entrada.shape[1], 8, 4, 2, 1]

rna = RNAE(neurons)

rna.treinamento(entrada[0:n_trei, :], saida[0:n_trei, :],
             tpop=200, gens=1000, bits=16, pmut=0.1, pcruz=0.6, epidemia=150)

rna.salvar_modelo("./modelos/rnae_sonar.txt")
rna = RNAE.carregar_modelo("./modelos/rnae_sonar.txt")
pred = rna.propagacao(entrada[n_trei:,:])
expct = saida[n_trei:]
expct = binarray2int(expct).reshape((expct.shape[0], 1))

pred = binarray2int(pred).reshape((expct.shape[0], 1))

accu = 100 * sum(pred == expct) / expct.size
print("Acuracia {} %".format(accu))
