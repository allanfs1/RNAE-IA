from rnae import RNAE
from numpy import array

tempmax = 40.0
tempmin= 34.0

rna = RNAE.carregar_modelo("./modelos/Diagnostico.txt")



temperatura = 38.9
normalizado=(temperatura - tempmin) / (tempmax-tempmin);
entrada = array([normalizado,0,1,1,0,1])
pred = rna.propagacao(entrada)
print(pred)
