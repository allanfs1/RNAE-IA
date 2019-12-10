#!/usr/bin/env python3.6
#-*- Coding: UTF-8 -*-
"""
Dados para teste.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.

FONTE:
http://archive.ics.uci.edu/ml/datasets/Acute+Inflammations
https://archive.ics.uci.edu/ml/datasets/Iris?spm=a2c4e.11153940.blogcont603256.5.333b1d6f05ZggC
"""

import pkg_resources
from numpy import loadtxt



IRIS = loadtxt(pkg_resources.resource_filename('rnae',
                                        '/dados/iris.csv'),
                                        delimiter=",")

IRIS_NAME = {1:"Setosa", 2:"Versicolor", 3:"Virginica"}

DIAGNOSTICO = loadtxt(pkg_resources.resource_filename('rnae',
                                              '/dados/diagnostico.csv'),
                                               delimiter=",")
