# -*- coding: utf-8 -*-
import pdftotext
#https://github.com/jalan/pdftotext

import os
from nltk.corpus import stopwords
from nltk import word_tokenize

#Retorna un diccionario de palabras que no deben considerarse (stopWords) o basura
def stopWordsSpanish():

    stopWords = stopwords.words('spanish')
    dict_stopWords = {}

    i=0
    n = len(stopWords)

    while i < n:
        dict_stopWords[ stopWords[i] ] = 1
        i += 1

    return dict_stopWords

#Crea un diccionario apartir del string words : Llave = terminos unicos. Valor = frecuencia de apariciones
def createTerms( words ):

    list_of_words = word_tokenize(words)
    stopwords = stopWordsSpanish()
    terminos = {}

    for palabra in list_of_words:
        if palabra not in stopwords:
            if palabra not in terminos:
                terminos[palabra] = 1
            else:
                terminos[palabra]+= 1
    return terminos

#Contenido del main

path_pdfs = '/Users/salgado/Desktop/BigData/ProyectoAnalizadorTesis/articules/pdfs'
files = os.listdir(path_pdfs)
string_texto = ''

#Para cada pdf obtenemos su texto
for file in files:

        with open( path_pdfs + '/' + file , "rb") as f:
            pdf = pdftotext.PDF(f)

        for page in pdf:
            string_texto += page

string_texto = string_texto.lower()
terminos = createTerms(string_texto)
print(terminos)