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
        arquivo = None
        campo_cpf = None
        caminho_lista_codecs = os.path.abspath('./configs/lista de codecs.txt')

        lista_de_decoders = list()
        with open(caminho_lista_codecs, encoding='u16') as lista_codecs:
            for linha in lista_codecs:
                lista_de_decoders += linha.strip('\n').split(', ')
            lista_codecs.close()
        print(len(lista_de_decoders))

        for CODEC in lista_de_decoders:
            print(f'Testando CODEC {CODEC}', end='\n')
            try:
                arquivo = open(file=documento, mode='r', encoding=CODEC)
                info = arquivo.readline()
                campo_cpf = 'CPF (sem pontos e traço ex: 12345678900)' in info
                if CODEC == lista_de_decoders[len(lista_de_decoders)-1] and not campo_cpf:
                    raise 'NÃO FOI ENCONTRADO NENHUM CODEC PARA USAR'
                elif campo_cpf:
                    print(f'Decoder utilizado: {arquivo.encoding}')
                    break
                else:
                    print(f"'{CODEC}' codec can't decode byte 0xfe in position 0: "
                          f"Can't find complete CPF field")
                arquivo.seek(0)
            except UnicodeDecodeError as err:
                if CODEC == lista_de_decoders[len(lista_de_decoders)-1] and not campo_cpf:
                    raise f'NÃO FOI ENCONTRADO NENHUM CODEC PARA USAR'
                print(f'{err}')
            except UnicodeError as err:
                if CODEC == lista_de_decoders[len(lista_de_decoders)-1] and not campo_cpf:
                    raise f'NÃO FOI ENCONTRADO NENHUM CODEC PARA USAR'
                print(f'{err}')

        self.total_de_cadastros = len(arquivo.readlines())-1
        arquivo.seek(0)

        csv.register_dialect('ponto_virgula', delimiter=';', quoting=csv.QUOTE_NONE)

        dicionario_arquivo = self.verifica_formatacao(arquivo)

        return dicionario_arquivo

    def __inicia_arquivo_filtrado(self):
        caminho = os.path.join(self.base_dir, 'filtrado.csv')
        arquivo = open(file=caminho, mode='w', encoding='UTF-16')
        campos = self.dicionario_arquivo.fieldnames
        dicionario_arquivo_filtrado = csv.DictWriter(arquivo, fieldnames=campos)
        return dicionario_arquivo_filtrado

    @staticmethod
    def verifica_formatacao(arquivo):
        for dialect in csv.list_dialects():
            dicionario_arquivo = csv.DictReader(arquivo, dialect=dialect)
            for field in dicionario_arquivo.fieldnames:
                if field == 'CPF (sem pontos e traço ex: 12345678900)':
                    print(f'Dialeto utilizado: {dialect}')
                    return dicionario_arquivo
                else:
                    arquivo.seek(0)
