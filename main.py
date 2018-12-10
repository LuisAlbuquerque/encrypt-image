""" 
----------------------------------------Image Encryption---------------------------
using : 
#Eliptic curve cryptography
    -> Elgamal
#others
    -> RSA

-------Note---------
#python3.6 ou >
    python3.6 main.py

# type checking
mypy main.py
--------------------

-----------------------------------------------------------------------------------
"""

import sys
import random
import sympy
from PIL import Image
#from fastecdsa import keys, curve
#from fastecdsa.curve import P256
#from fastecdsa.point import Point
from functools import reduce
from toolz import curry
from typing import *

""" outros ficheiros """
import elipticCurve

"""........."""

""" DEFINES """
RANDOM_LOWER_K_ = 100
RANDOM_UPER_K_  = 1000
RANDOM_LOWER = 100
RANDOM_UPER  = 1000
R = 0
G = 1
B = 2
DELTA = 0
GAMA = 1
"""........."""

""" Globais """
Curva_eliptica = (sympy.nextprime(random.randint(RANDOM_LOWER,RANDOM_UPER)),
                        random.randint(RANDOM_LOWER,RANDOM_UPER ),
                        random.randint(RANDOM_LOWER,RANDOM_UPER)
                        )
"""........."""

""" funcao que transforma um inteiro 
    num ponto na curva eliptica
Recebe: 
 1. mensagem (numero : int)
 2. dados da curva eliptica
    curva[0] = p ( Z[p] )
    curva[1] = a ( y^2 = x^3 + [a]x + b )
    curva[2] = b ( y^2 = x^3 + ax + [b] )
 3. k

Retorna:
 1. Ponto na curva eliptica 
"""
#def Koblitz(mens: int, Ecurve: Tuple[int,int,int] = Curva_eliptica, k: int =30)-> any:
#    (p, a, b) = Ecurve
#    Zp=IntegerModRing(p)
#    E = EllipticCurve(0, 0, 0, a, b, domain = ZZ)
#    E=EllipticCurve(Zp, [a,b])
#    x = mens*k
#    existe_y = sympy.legendre_symbol(x^3+a*x+b, p)==1
#    contador=0
#    while not existe_y and contador <k:
#        x+=1
#        contador+=1
#        existe_y = sympylegendre_symbol(x^3+a*x+b, p)==1
#    if existe_y:
#        x=Zp(x)
#        return (x, sqrt(x^3+a*x+b)
#    return[]

def Koblitz(x: int, Ecurve: Tuple[int,int,int] = Curva_eliptica, k: int =30, f: int = 1)-> any:
    if(f): x = x*30
    if(legendre_symbol(x**3 + Ecurve[1]*x + Ecurve[2],Ecurve[0]) == 1):
         return EllipticCurve(0, 0, 0, a, b, domain = ZZ)(x,sqrt(x^3+a*x+b),1)
    return koblitz(x+1,Ecurve,0)

""" funcao que aplica uma funcao
    a cada elemento da lista
Recebe:
 1. funcao
 2. lista de base
 3. lista de retorno (neste caso por onde comeca) 

Retorna:
 1. nova lista aplicando a funcao a cada elemento
"""
def forEachVec(f,lista, res = []):
    for i in lista:
        res.append(f(i))
    return res

""" funcao que transforma uma string
    num pixel
Recebe:
 1. string que contem todas as componentes do pixel
 2. separador de componentes do pixel

Retorna:
 1. Pixel
"""
def stringCHAR_to_image_aux(string_pixel: str, separator = ",")-> Tuple[int,int,int]:
    pixel = string_pixel.split(separator)
    return (pixel[R],pixel[G],pixel[B])

""" funcao que transforma uma string
    em uma imagem
Recebe:
 1. string que contem toda a informacao da imagem
 2. separador de pixel

Retorna:
 1. imagem
"""
def stringCHAR_to_image(string: str, separator: str = " ")-> List[Tuple[int,int,int]]:
    forEachVec( lambda x: stringCHAR_to_image_aux(x), string.split(separator))


""" funcao que transforma uma string de
    inteiros numa string de char
    fazendo a associacao ASCI
Recebe:
 1. string (int)

Retorna:
 1. string (char)
"""
def stringInt_to_stringCHAR(string: str)-> str: return func_convert(string,curry(chr))

""" funcao que transforma uma string de
    char numa string de inteiros
    fazendo a associacao ASCI
Recebe:
 1. string (char)

Retorna:
 1. string (int)
"""
def stringChar_to_StringInt(string: str)-> int: return func_convert(string,curry(ord))

""" funcao de conversao de strings
    usando uma funcao
Recebe:
 1. String para converter
 2. funcao
"""
def func_convert(string: str,f): return reduce(lambda x,y: f (x) + f (y), string )

""" numer ----> 1number """
def string_to_int(string: str)-> int: return int('1' + string)

""" 1number ----> number """
def int_to_string(integer: int)-> str: return str(int)[1:]

"""
MACRO para ser mais legivel
"""
def pixel_to_string_aux(pixel_element: List[Tuple[int,int,int]])-> str:
    return '0'*( 3 - len(str(pixel_element)) ) + str(pixel_element)

""" funcao auxiliar de image_to_string_aux
   que transforma um pixel numa string 
Recebe:
 1. Um pixel (r,g,b)
 3. Um separador, forma como vai juntar os valores as componentes do pixel

 Retorna:
  1. string com o pixeis em string, com as componetes separadas por (espaco =separador)
"""
def pixel_to_string(pixel: Tuple[int,int,int], separator: str =",")-> str:
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
def image_to_string_aux(pixel1: Tuple[int,int,int],pixel2: Tuple[int,int,int], separator: str = " ")-> str:
    return (pixel_to_string(pixel1) + separator + pixel_to_string(pixel2))

""" funcao que transforma uma imagem (conjunto de pixeis)
    em uma string (conjunto de carateres)
Recebe: 
 1. imagem (somento os pixeis)

 Retorna:
  1. string com os pixeis separados por (espaco)
"""

def image_to_string(image: List[Tuple[int,int,int]])-> str:
     return reduce(lambda x,y: image_to_string_aux(x,y),image)

""" funcao que trata da imagem
Recebe:
 1. Uma imagem

Retorna:
 1. lista de pixeis
"""
def convert_image(imagem)-> List[Tuple[int,int,int]]: return list((Image.open(imagem)).getdata())


""" funcao que cria uma imagem
Recebe:
 1. Uma lista com os pixeis
 2. mode da imagem
 3. tamanho da imagem

Retorna:
 1. nova imagem com os pixeis da lista
"""
def create_image(list_: List[Tuple[int,int,int]], mode, size):
    res = Image.new(mode,size)
    res.putdata(list_)
    return res

""" funcao que mostra a imagem
Recebe:
 1. Uma imagem

"""
def show_image(imagem): return (Image.open(imagem)).show()

""" funcao de encriptacao
    usa como base o sistema criptografico
    de chave publica RSA
Recebe:
 1. pixel
 2. n
 3. e

Retorna:
 1. pixel encriptado
"""
def rsa_c_aux(pixel: Tuple[int,int,int],n: int,e: int)-> Tuple[int,int,int]:
    return (pixel[R]**e % n,pixel[G]**e % n,pixel[B]**e % n)

""" funcao de decifracao
    usa como base o sistema criptografico
    de chave publica RSA
Recebe:
 1. pixel encriptado
 2. n
 3. chave privada

Retorna:
 1. pixel 
"""
def rsa_d_aux(pixel: Tuple[int,int,int],n: int,PrivKey: int)-> Tuple[int,int,int]:
    return (pixel[R]**PrivKey % n,pixel[G]**PrivKey % n,pixel[B]**PrivKey % n)

""" funcao de encriptacao
    usa como base o sistema criptografico
    de chave publica RSA
Recebe:
 1. imagem
 2. (n,e)

Retorna:
 1. imagem encriptada
"""
def RSA_c(image: List[Tuple[int,int,int]],Pubkey: Tuple[int,int])-> List[Tuple[int,int,int]]:
    return list(map(lambda x: rsa_c_aux(x,Pubkey[0],Pubkey[1]), image))

""" funcao de decifracao
    usa como base o sistema criptografico
    de chave publica RSA
Recebe:
 1. imagem encriptada
 2. (n,e)
 3. chave privada

Retorna:
 1. imagem
"""
def RSA_d(image: List[Tuple[int,int,int]],Pubkey,PrivKey: int)-> List[Tuple[int,int,int]]:
    return list(map(lambda x: rsa_d_aux(x,Pubkey[0],PrivKey), image))

""" funcao que cifra a imagem
Recebe:
 1. Uma imagem

Retorna:
 1. Imagem encriptada
"""
def Elgamal_c(imagem: List[Tuple[int,int,int]],Pubkey: Tuple[any,int,int])-> List[Tuple[int,int,int]]:
    """
    # gerar um numero aleatorio 1 ou 2
    rand = random.randint(1,2)
    # somar a todos os pontos esse valor
    imagem = list(map(lambda x: (x[0]+rand,x[1]+rand,x[2]+rand), imagem ))
    # numero de alteracoes
    alteracaoes = len(imagem)
    """

    E , P , Q = Pubkey
    ponto = Koblitz( string_to_int( stringChar_to_StringInt(image_to_string(imagem) ) ))

    K = random.randint(RANDOM_LOWER_K_,RANDOM_UPER_K_)
    return (K*P , ponto + K*Q)

   # #tentar implementar o elgamal normal
   # E , P , Q = Pubkey
   # k = random.randint(1,2*E[0])
   # imagem = list(map(lambda x: (x[0]+rand,x[1]+rand,x[2]+rand), imaem ))
   # # gerar aleatoriamente o k
   # return (k*P, list(map(lambda x: (( x[0] + k * Q )%255, ( x[1] + k * Q )%255, ( x[2] + k * Q )%255, imagem ))))

""" funcao que decifra a imagem
Recebe:
 1. Uma imagem encriptada
 2. chave publida
 3. chave privada

Retorna:
 1. Imagem decifrada
""" 
def Elgamal_d(imagem: Tuple[any,any],Pubkey: Tuple[any,int,int],PrivKey: int)-> List[Tuple[int,int,int]]:
    return ((-1)*PrivKey*imagem[DELTA] + imagem[GAMA] )
   # delta , gama = imagem
   # E , P , Q = Pubkey
   # return (list(map(lambda x: ( (-1)*PrivKey*x[0]+gama, (-1)*PrivKey*x[1]+gama, (-1)*PrivKey*x[2]+gama), delta )))


""" funcao que cifra a imagem
Recebe:
 1. Uma imagem
 2. Nome de um protocologo de cifracao

Retorna:
 1. Imagem encriptada
"""
def cifra(imagem: List[Tuple[int,int,int]] , protocologo: str):
    if (protocologo == 'Elgamal'): 
        (p,a,b) = Curva_eliptica
        EllipticCurve(0, 0, 0, a, b, domain = ZZ)

        #PubKey = ((p,a,b), P, Q)
        return Elgamal_c(imagem,Pubkey)
    else: return (-1)

def DEUS_EC():
    #Curva_eliptica = (p,a,b)
    (p,a,b) = Curva_eliptica
    EllipticCurve(0, 0, 0, a, b, domain = ZZ)

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
    #print(len(img))

    # funcao que cifra a mensagem usando o protocolog enunciado
    #eimg = cifra(img, sys[3])
    eimg = cifra(img, protocologo)

main()
