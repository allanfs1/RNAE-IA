#!/usr/bin/env python3.6
# -*- Codigin: UTF-8 -*-
"""
Rede Neural Artificial Evolucionária.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
import json
import zlib

from numpy import array, dot, sum, exp
from numpy.random import randn
from numpy import load, save, hsplit, concatenate, sqrt

from pygenec.populacao import Populacao
from pygenec.selecao.torneio import Torneio
from pygenec.cruzamento.embaralhamento import Embaralhamento
from pygenec.mutacao.sequenciareversa import SequenciaReversa
from pygenec.evolucao import Evolucao
from pygenec import binarray2int


class RNAE:
    '''
    Rede Neural Artificial Evolucionária.
    '''
    def __init__(self, neuronios):
        self._neuronios = neuronios
        self.__melhor_ind = None
        self._inicializar()

    def _inicializar(self):
        self._camadas = len(self._neuronios)
        self._pesos = [randn(self._neuronios[i], self._neuronios[i + 1])
                         for i in range(self._camadas - 1)]
        self._vies = [randn(1, self._neuronios[i + 1])
                      for i in range(self._camadas - 1)]

        self._psize = [self._neuronios[i] * self._neuronios[i + 1]
                 for i in range(self._camadas - 1)]

        self._vsize = [self._neuronios[i + 1] for i in range(self._camadas - 1)]

        self._tipoat = ["sigmoid"] * (self._camadas - 1)
        self._tipoat[-1] =  "passobinario"


        self._ativacao = {"limiar": self.limiar,
                          "sigmoid": self.sigmoid,
                          "passobinario": self.passobinario}


    def propagacao(self, input):
        y = input
        for i in range(self._camadas - 1):
            x = dot(y, self._pesos[i]) + self._vies[i]
            y = self.ativacao(x, self._tipoat[i])
        return y

    def ativacao(self, x, tipoat):
        if tipoat is None:
            tipoat = "limiar"
        return self._ativacao[tipoat](x)

    def limiar(self, x, limit=0.5):
        out = x.copy()
        out[out >= limit] = 1
        out[out < limit] = 0
        return out.astype(int)

    def passobinario(self, x):
        out = x.copy()
        out[out >= 0] = 1
        out[out < 0] = 0
        return out.astype(int)

    def sigmoid(self, x):
        return 1.0 / (1.0 + exp(-x))

    def cromossosmos_peso(self, individuo):
        w0 = 0
        b0 = sum(self._psize)
        pesos = []
        vies = []
        for i in range(self._camadas - 1):
            wtmp = individuo[w0:w0 + self._psize[i]].reshape(self._neuronios[i],
                                               self._neuronios[i + 1]
                                               )
            btmp = individuo[b0:b0 + self._vsize[i]].reshape(1, self._neuronios[i + 1])
            pesos.append(wtmp)
            vies.append(btmp)
            w0 += self._psize[i]
            b0 += self._vsize[i]
        return pesos, vies

    def valores(self, populacao, cromossomos, bits, xr):
        bx = hsplit(populacao, cromossomos)
        const = 2.0 ** bits - 1.0
        const = xr[1] / const
        x = [xr[0] + const * binarray2int(xi).astype(float) for xi in bx]
        x = concatenate(x).T
        return x

    def carregar_pesos_vies(self, individuo):
        del self._pesos
        del self._vies

        self._pesos = []
        self._vies = []
        self._pesos, self._vies = self.cromossosmos_peso(individuo)


    def salvar_modelo(self, arquivo):
        if self.__melhor_ind is None:
            print("Treinamento não realizado")
            return

        dados = {}
        dados["neuronios"] = self._neuronios
        dados["cromossomos"] = self.__melhor_ind[0].tolist()
        dados["genes"] = self.__melhor_ind[1]

        with open(arquivo, "w") as arq:
            json.dump(dados, arq, indent=4)

    def treinamento(self, dt_in, dt_out, tpop=100, gens=1000, bits=8, pmut=0.1,
                 pcruz=0.4, xr=[-1000, 2000],
                 epidemia=500):

        tamanho_populacao = tpop
        cromossomos = sum(self._psize) + sum(self._vsize)
        tamanho = int(0.1 * tamanho_populacao)
        genes = bits * cromossomos
        elitista = True

        def objetivo(individuo):
            self.carregar_pesos_vies(individuo)
            out = self.propagacao(dt_in)
            accu = -sum(out != dt_out) / dt_out.size
            return accu

        def avaliacao(populacao):
            individuos = self.valores(populacao, cromossomos, bits, xr)
            return  array([objetivo(individuos[k, :])
                          for k in range(len(populacao))])

        populacao = Populacao(avaliacao,
                              genes,
                              tamanho_populacao)

        selecao = Torneio(populacao, tamanho=tamanho)
        cruzamento = Embaralhamento(tamanho_populacao)
        mutacao = SequenciaReversa(pmut=pmut)

        evolucao = Evolucao(populacao,
                            selecao,
                            cruzamento,
                            mutacao)

        evolucao.nsele = tamanho
        evolucao.pcruz = pcruz
        evolucao.manter_melhor = elitista
        evolucao.epidemia = epidemia

        for i in range(gens):
            vmin, vmax = evolucao.evoluir()
            print(evolucao.geracao, vmax, vmin)

        x = self.valores(populacao.populacao, cromossomos, bits, xr)
        individuo = x[-1, :]
        genesb = populacao.populacao[-1,:].tolist()
        self.__melhor_ind = [individuo, genesb]
        objetivo(individuo)

    @property
    def melhor_individuo(self):
        return self.__melhor_ind

    @melhor_individuo.setter
    def melhor_individuo(self, mind):
        self.__melhor_ind = mind

    @classmethod
    def carregar_modelo(cls, arquivo):
        with open(arquivo) as arq:
            dados = json.load(arq)
        rnae = cls(dados["neuronios"])

        rnae.melhor_individuo = [array(dados["cromossomos"]).astype(float),
                                 array(dados["genes"])]
        rnae.carregar_pesos_vies(array(dados["cromossomos"]).astype(float))


        return rnae
