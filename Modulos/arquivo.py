import csv
import os.path
from tkinter.filedialog import askopenfilename


class AbreArquivo:
    def __init__(self):
        self.dicionario_arquivo = self.__abre_arquivo()
        self.dicionario_arquivo_filtrado = self.__inicia_arquivo_filtrado()

    def __abre_arquivo(self):
        extenssoes = [('Arquivos CSV', '*.csv')]
        documento = askopenfilename(filetypes=extenssoes, initialdir=os.path.abspath('./'), title='Selecione o arquivo')

        self.base_dir = os.path.dirname(documento)

        arquivo = open(file=documento, mode='r', encoding='utf-16', newline='')
        self.total_de_cadastros = len(arquivo.readlines())-1
        arquivo.seek(0)

        dicionario_arquivo = csv.DictReader(arquivo, dialect='excel-tab')
        return dicionario_arquivo

    def __inicia_arquivo_filtrado(self):
        caminho = os.path.join(self.base_dir, 'filtrado.csv')
        arquivo = open(file=caminho, mode='w', newline='', encoding='utf-16')
        campos = self.dicionario_arquivo.fieldnames
        dicionario_arquivo_filtrado = csv.DictWriter(arquivo, fieldnames=campos)
        return dicionario_arquivo_filtrado