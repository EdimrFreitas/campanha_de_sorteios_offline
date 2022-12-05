import os.path
import csv


caminho_lista_codecs = os.path.abspath('./Para análise/sorteio 11 (utf-8).csv')

arquivo = open(file=caminho_lista_codecs, mode='r', encoding='u16')
info = arquivo.readline()
campo_cpf = 'CPF (sem pontos e traço ex: 12345678900)' in info

print(campo_cpf)
print(info)
