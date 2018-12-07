import sys
import random
from PIL import Image
#from fastecdsa import keys, curve
#from fastecdsa.curve import P256
#from fastecdsa.point import Point
from functools import reduce
from toolz import curry

""" DEFINES """
RANDOM_LOWER_K_ = 100
RANDOM_UPER_K_  = 1000
R = 0
G = 1
B = 2
"""........."""

#def Koblitz(mens, (p, a, b), k =30):
#    Zp=IntegerModRing(p)
#    E=EllipticCurve(Zp, [a,b])
#    x = mens*k
#    existe_y=legendre_symbol(x^3+a*x+b, p)==1
#    contador=0
#    while not existe_y and contador <k:
#        x+=1
#        contador+=1
#        existe_y=legendre_symbol(x^3+a*x+b, p)==1
#    if existe_y:
#        x=Zp(x)
#        return E(x, sqrt(x^3+a*x+b))
#    return[]

""" funcao que percorre uma lista
    e que retorna uma outra cujos 
    elementos sao o resultado de
    aplicar uma funcao aos elementos
    da lista recebida.
Recebe:
 1. funcao que cria elementos a partir de outros
 2. lista de entrada
 3. lista de retoro

 Retorna:
  1. nova lista aplicando a funcao
"""

def forEachVec(f,lista, res = []):
    for i in lista:
        res.append(f(i))
    return res

def stringCHAR_to_image_aux(string_pixel):
    pixel = string_pixel.split(",")
    return (pixel[R],pixel[G],pixel[B])

def stringCHAR_to_image(string):
    forEachVec( lambda x: stringCHAR_to_image_aux(x), string.split(" "))


def stringInt_to_stringCHAR(string): return func_convert(string,curry(chr))

def string_int(string): return func_convert(string,curry(ord))

def func_convert(string,f): return reduce(lambda x,y: f (x) + f (y), string )

""" numer ----> 1number """
def string_to_int(string): return int('1' + string)

def pixel_to_string_aux(pixel_element):
    return '0'*( 3 - len(str(pixel_element)) ) + str(pixel_element)

""" funcao auxiliar de image_to_string_aux
   que transforma um pixel numa string 
Recebe:
 1. Um pixel (r,g,b)
 3. Um separador, forma como vai juntar os valores as componentes do pixel

 Retorna:
  1. string com o pixeis em string, com as componetes separadas por (espaco =separador)
"""
def pixel_to_string(pixel, separator =","):
    if(separator != ''): return (str(pixel[R]) + separator + str(pixel[G])+ separator + str(pixel[B]))
    return (pixel_to_string_aux(pixel[R]) + separator + pixel_to_string_aux(pixel[G])+ separator + pixel_to_string_aux(pixel[B]))


""" funcao auxiliar de image_to_string
    que transforma dois pixeis numa string
Recebe: 
 1. Um pixel (r,g,b)
 2. Outro pixel (r,g,b)
 3. Um separador, forma como vai juntar os valores dos pixeis

 Retorna:
  1. string com os pixeis separados por (espaco =separador)
""" 
def image_to_string_aux(pixel1,pixel2, separator = " "): return (pixel_to_string(pixel1) + separator + pixel_to_string(pixel2))

""" funcao que transforma uma imagem (conjunto de pixeis)
    em uma string (conjunto de carateres)
Recebe: 
 1. imagem (somento os pixeis)

 Retorna:
  1. string com os pixeis separados por (espaco)
"""

def image_to_string(image):
     return reduce(lambda x,y: image_to_string_aux(x,y),image)

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

def rsa_c_aux(pixel,n,e):
    return (pixel[R]**e % n,pixel[G]**e % n,pixel[B]**e % n)

def rsa_d_aux(pixel,n,PrivKey):
    return (pixel[R]**PrivKey % n,pixel[G]**PrivKey % n,pixel[B]**PrivKey % n)

def RSA_c(image,Pubkey):
    return list(map(lambda x: rsa_c_aux(x,Pubkey[0],Pubkey[1]), image))

def RSA_d(image,Pubkey,PrivKey):
    return list(map(lambda x: rsa_d_aux(x,Pubkey[0],PrivKey), image))

""" funcao que cifra a imagem
Recebe:
 1. Uma imagem

Retorna:
 1. Imagem encriptada
"""
def Elgamal(imagem,Pubkey):
    """
    # gerar um numero aleatorio 1 ou 2
    rand = random.randint(1,2)
    # somar a todos os pontos esse valor
    imagem = list(map(lambda x: (x[0]+rand,x[1]+rand,x[2]+rand), imagem ))
    # numero de alteracoes
    alteracaoes = len(imagem)
    """

    #tentar implementar o elgamal normal
    E , P , Q = Pubkey
    imagem = list(map(lambda x: (x[0]+rand,x[1]+rand,x[2]+rand), imagem ))
    # gerar aleatoriamente o k
    k = random.randint(1,2*E[0])
    return (k*P, list(map(lambda x: (( x[0] + k * Q )%255, ( x[1] + k * Q )%255, ( x[2] + k * Q )%255, imagem ))))

""" funcao que decifra a imagem
Recebe:
 1. Uma imagem encriptada
 2. chave publida
 3. chave privada

Retorna:
 1. Imagem decifrada
""" 
def Elgamal_d(imagem,Pubkey,PrivKey):
    delta , gama = imagem
    E , P , Q = Pubkey
    return (list(map(lambda x: ( (-1)*PrivKey*x[0]+gama, (-1)*PrivKey*x[1]+gama, (-1)*PrivKey*x[2]+gama), delta )))


""" funcao que cifra a imagem
Recebe:
 1. Uma imagem
 2. Nome de um protocologo de cifracao

Retorna:
 1. Imagem encriptada
"""
def cifra(imagem , protocologo):
    if (protocologo == 'Elgamal'): return Elgamal(imagem,"")
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
    print(len(img))

    # funcao que cifra a mensagem usando o protocolog enunciado
    #eimg = cifra(img, sys[3])
    #eimg = cifra(img, protocologo)

main()
