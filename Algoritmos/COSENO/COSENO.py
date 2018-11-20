# -*- coding: utf-8 -*-

import csv
from nltk import word_tokenize
from pyspark import SparkContext
from pyspark import SparkConf
import math as math
from nltk.corpus import stopwords
from operator import itemgetter
from collections import OrderedDict

class NLP_UTILS_IPN_CIC :

    def __init__(self):
            self.documents =[]
            self.matrix = []
            self.dictionary_terms = {}
            self.original_documents = []
            self.dictionary_lemma = self.getDictionaryLemmatizationSpanish()
            self.dictionary_stopWords = self.stopWordsSpanish()


    def getDictionaryLemmatizationSpanish( self ) :

        file = open("/Users/salgado/vagrant/data/diccionarioLematizador.txt","r")
        lemma = {}
        for line in file:
            bloq = line.split()
            lemma[bloq[0]] = bloq[1]
        return lemma


    def stopWordsSpanish( self ):

        file = open("/Users/salgado/vagrant/data/stopwords.txt","r")
        dict_stopWords = {}
        for line in file:
            if line not in dict_stopWords:
                dict_stopWords[line] = 1
        return dict_stopWords


    def wordMappingLemma(self, word):

        word = word.lower()
        if word in self.dictionary_lemma:
            correct = self.dictionary_lemma.get(word)
        else:
            correct = word

        return correct


    def createVectorBool(self,  document , dictionary ):

        for word in dictionary:
            vector=[]
            if word in document:
                vector.append(1)
            else:
                vector.append(0)
        return vector


    def createVectorFrequency(self, document, dictionary):
        vector = []

        for palabra in dictionary:
            contador = 0

            for palabradocs in document:
                if palabradocs == palabra:
                    contador += 1

            vector.append(contador)

        return vector


    def loadFile(self, file):

        i=0

        file = open( file , "r")
        dic = {}
        documents_ok = []

        #every line is a document
        i=0
        for line in file:
            self.original_documents.append(line)
            tmp_min = line.lower()
            tmp_split = word_tokenize(tmp_min, 'spanish')

            list_word_document = []

            #every word
            for word in tmp_split:

                word_ok = self.wordMappingLemma(word)
                if word_ok not in self.stopWordsSpanish():

                    list_word_document.append(word_ok)
                    if word_ok not in dic:
                        dic[word_ok] = 1

            documents_ok.append(list_word_document)

        self.dictionary_terms = dic
        self.documents = documents_ok

    def getMatrixFrecuency( self ):

            for i in self.documents:
                self.matrix.append( self.createVectorFrequency(i, self.dictionary_terms ) )
            return self.matrix


    def cosine_similarity(self, v1, v2):
        sumxx, sumxy, sumyy = 0., 0., 0.
        for i in range(len(v2)):
            x = v1[i] + 0.
            y = v2[i] + 0.
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y

        value = sumxx * sumyy

        if value >0:
            return sumxy / math.sqrt( value )
        else:
            return 0


    def consulta(self, str_noticia):

        cosines = {}
        i = 0
        vector_num = self.createVectorFrequency(str_noticia, self.dictionary_terms)
        for doc in self.matrix:
            cosine = self.cosine_similarity(doc, vector_num)
            cosines[self.original_documents[i]] = cosine
            i+= 1

        #Get the top ten
        sorted_x = cosines(sorted( cosines.items(), key=itemgetter(1)))

        return sorted_x[0:9]


a = NLP_UTILS_IPN_CIC()
a.loadFile("/Users/salgado/vagrant/data/noticias.min.csv")
b = a.getMatrixFrecuency()
c = a.consulta('estado de aguascalientes sexenio')
print(c)

