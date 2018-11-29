import sys
import random
from PIL import Image
from fastecdsa import keys, curve
from fastecdsa.curve import P256
from fastecdsa.point import Point

""" DEFINES """
RANDOM_LOWER_K_ = 100
RANDOM_UPER_K_  = 100
"""........."""

""" funcao que trata da imagem
Recebe:
 1. Uma imagem

Retorna:
 1. lista de pixeis
"""
def convert_image(imagem): return list((Image.open(imagem)).getdata())


""" funcao que cria uma imagem
Recebe:
 1. Uma lista com os pixeis
 2. mode da imagem
 3. tamanho da imagem

Retorna:
 1. nova imagem com os pixeis da lista
"""
def create_image(list_, mode, size):
    res = Image.new(mode,size)
    res.putdata(list_)
    return res

""" funcao que mostra a imagem
Recebe:
 1. Uma imagem

"""
def show_image(imagem): return (Image.open(imagem)).show()

""" funcao que cifra a imagem
Recebe:
 1. Uma imagem

Retorna:
 1. Imagem encriptada
"""
def Elgamal(imagem,Pubkey,Privkey):
    # gerar um numero aleatorio 1 ou 2
    rand = random.randint(1,2)
    # somar a todos os pontos esse valor
    imagem = list(map(lambda x: (x[0]+rand,x[1]+rand,x[2]+rand), imagem ))
    # numero de alteracoes
    alteracaoes = len(imagem)
    #
    # gerar aleatoriamente o k
    k = random.randint(RANDOM_LOWER_K_,RANDOM_UPER_K_)


""" funcao que cifra a imagem
Recebe:
 1. Uma imagem
 2. Nome de um protocologo de cifracao

Retorna:
 1. Imagem encriptada
"""
def cifra(imagem , protocologo):
    if (protocologo == 'Elgamal'): return Elgamal(imagem,"","")
    else: return (-1)


""" funcao principal que gere todo o processo
    call python main <img> <from>

    argumentos do programa
    1. imagem
    2. para quem
    3. protocologo usado para a cifracao
"""
def main():
    """ temporariamente , so para ser mais facil testar"""
    imagem1 = 'jc.jpg'
    protocologo = 'Elgamal'
    """..............."""

    # funcao que recebe a imagem e trata de passar para lista
    #img = convert_image(sys[1])
    show_image(imagem1)
    img = convert_image(imagem1)
    print(img)

    # funcao que cifra a mensagem usando o protocolog enunciado
    #eimg = cifra(img, sys[3])
    eimg = cifra(img, protocologo)

main()
