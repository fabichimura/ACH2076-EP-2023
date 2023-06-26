import numpy as np
from itertools import product
import re
import unicodedata
import numpy as np
import sympy as sp

def is_invertible(matrix):
    det = np.linalg.det(matrix)
    return det != 0

def remover_acentos(texto):
    texto_sem_acentos = ''.join(
        letra for letra in unicodedata.normalize('NFD', texto)
        if unicodedata.category(letra) != 'Mn'
    )
    return texto_sem_acentos

def substituir_por_posicao(frase):
    lista_numeros = []
    for letra in frase:
        posicao = ord(letra.lower()) - ord('a')
        lista_numeros.append(posicao)
    return lista_numeros

def substituir_por_letra(numero):
    if 0 <= numero <= 25:
        letra = chr(numero + ord('a'))
        return letra
    else:
        return ""


with open('Grupo07_texto_cifrado.txt','r') as arquivo:
    texto_cifrado = arquivo.read()
    tam_texto_cifrado = len(texto_cifrado)

with open('policarpo_quaresma.txt', 'r', encoding='utf-8') as arquivo:
    policarpo_quaresma = arquivo.read()

    # transforma as letras em minúsculas
    policarpo_quaresma = policarpo_quaresma.lower()

    # remove os acentos das vogais
    policarpo_quaresma = remover_acentos(policarpo_quaresma)

    # remove todos os caracteres que não são letras
    policarpo_quaresma = re.sub(r'[^a-z]', '', policarpo_quaresma)

with open('policarpo_analise.txt','w', encoding='utf-8') as arquivo_saida:
    arquivo_saida.write(policarpo_quaresma)

# pelo GeraEP1.py -> a matriz para a encriptação é 2 x 2)
matrizes = list(product(range(26), repeat=4))
matrizes = [list(zip(matriz[:2], matriz[2:])) for matriz in matrizes]

matrizes_invertiveis = []

for matriz in matrizes:
    if(is_invertible(matriz)):
        matrizes_invertiveis.append(matriz)

# decripta e verifica se esta no texto
indice = 0
numeros_encriptado = substituir_por_posicao(texto_cifrado)
texto_decriptado = ''
numeros_decriptado = []
for matriz in matrizes_invertiveis:
    for i in range(0, 100, 2):
        if (i == 0):
            matriz_bloco = np.array([[numeros_encriptado[0], numeros_encriptado[1]]])
        else:
            matriz_bloco = np.array([[numeros_encriptado[i], numeros_encriptado[i + 1]]])
        produto = np.dot(matriz_bloco, matriz)
        produto = produto[0].tolist()
        produto_modulo = list(map(lambda x: x % 26, produto))
        primeiro_caract = substituir_por_letra(produto_modulo[0])
        segundo_caract = substituir_por_letra(produto_modulo[1])
        texto_decriptado = texto_decriptado + primeiro_caract + segundo_caract
    print(texto_decriptado)
    if(texto_decriptado in policarpo_quaresma and len(texto_decriptado) == len(texto_cifrado)):

        print('Este é o trecho decriptado:', texto_decriptado)
        print('Esta é a matriz que gerou', matriz)
    else:
        texto_decriptado = ''
    


# encripta novamente para conferir
'''
trecho_decriptado1 =  'oporemtaocoherentecomellemesmotaodeaccordocomasubstanciadavidaqueellemesmofabricaraqueselimitouasorr'
# calculado na mao
matriz_chave = [[7, 0], [4, 3]]
numeros_encriptado = substituir_por_posicao(trecho_decriptado1)

texto_decriptado = ''
for i in range(0, 100, 2):
    if (i == 0):
        matriz_bloco = np.array([[numeros_encriptado[0], numeros_encriptado[1]]])
    else:
        matriz_bloco = np.array([[numeros_encriptado[i], numeros_encriptado[i + 1]]])
    #print(matriz_bloco)
    produto = np.dot(matriz_bloco, matriz_chave)
    produto = produto[0].tolist()
    produto_modulo = list(map(lambda x: x % 26, produto))
    primeiro_caract = substituir_por_letra(produto_modulo[0])
    segundo_caract = substituir_por_letra(produto_modulo[1])
    texto_decriptado = texto_decriptado + primeiro_caract + segundo_caract
print(texto_decriptado)
print(texto_decriptado == texto_cifrado)
print(is_invertible(matriz_chave))
'''