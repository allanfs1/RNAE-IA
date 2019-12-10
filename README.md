# RNAE
Rede Neural Artificial Evolucionária

## Instalation

```bash
$ pip install rnea
```

ou


```bash
$ python setup.py install
```



## Utilização

```python
from numpy.random import shuffle
from numpy import array

from pygenec import binarray2int

from rnae import RNAE
from rnae import IRIS as dados
from rnae import IRIS_NAME


#Normalização dos dados de entrada

entrada = dados[1:,0:-1].astype(float)
for k in range(entrada.shape[1]):
    entrada[:, k] = ((entrada[:, k] - entrada[:, k].min()) /
                    (entrada[:, k].max() - entrada[:, k].min())
                    )

#Resultado esperado, em inteiro.

saidas = dados[1:,-1]

saidas = array([list(map(int, list("{0:2b}".format(int(s)).replace(" ", "0")))) for s in  saidas])
itrain = array(list(range(saidas.shape[0])))
shuffle(itrain)
etrain = entrada[itrain,:]
esaid = saidas[itrain, :]

n = int(esaid.shape[0] * 0.90)

neurons = [4, 4, 2]

rna = RNAE(neurons)
rna.treinamento(etrain[0:n, :], esaid[0:n, :],
             tpop=500, gens=1000, bits=16, pmut=0.1, pcruz=0.6, epidemia=150)

rna.salvar_modelo("./modelos/rnae_iris.txt")
rna = RNAE.carregar_modelo("./modelos/rnae_iris.txt")
pred = rna.propagacao(etrain[n:,:])
expct = esaid[n:]
expct = binarray2int(expct).reshape((expct.shape[0], 1))

pred = binarray2int(pred).reshape((expct.shape[0], 1))
print("\n")
print([IRIS_NAME[i] for i in pred.flatten().astype(int)])
print("\n")
print([IRIS_NAME[i] for i in expct.flatten().astype(int)])
print("\n")

accu = 100 * sum(pred == expct) / expct.size
print("Acuracia {} %".format(accu))
```
