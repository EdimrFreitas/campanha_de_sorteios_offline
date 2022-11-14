import pip
from os.path import abspath
import threading
from tkinter import Tk

from docbr import parse, validate

from Modulos.configs import Configs
from Modulos.construtor import self
from Modulos.imprimir import Printing


class Main(Configs, Printing, self):
    total_de_cadastros = 0
    total_de_participantes_validos = 0
    total_de_cpfs_invalidos = 0
    linha_atual = 0

    def __init__(self):
        Configs.__init__(self)
        self.iniciar_root()
        self.abre_arquivo()
        self.inicia_frames()
        self.inicia_widgets()
        self.binds()

        self.root.mainloop()

    def iniciar_root(self):
        # Parâmetros de  tamanh da tela
        tam_x, tam_y = 500, 400
        root = Tk()
        root.configure(background = self.cor_da_borda)
        root.title('Verificador offline')
        # Parâmetros de posicionamento da janela na tela do usuário
        pos_x = int((root.winfo_screenwidth() - tam_x) / 2)
        pos_y = int((root.winfo_screenheight() - tam_y) / 2)
        root.geometry(f'{tam_x}x{tam_y}+{pos_x}+{pos_y}')
        # Seta como fixo os tamanhos da tela
        root.resizable(False, False)
        self.root = root

    def inicia_frames(self):
        frames = {
            'frame_principal': {
                'param': {'master': self.root, 'name': 'principal', 'bg': self.cor_de_fundo},
                'place': {'relwidth': 0.96, 'relheight': 0.96, 'relx': 0.02, 'rely': 0.02}
            }
        }
        self.frame(frames)
        self.frame_principal = self.root.children['principal']

    def inicia_widgets(self):
        barra_de_progresso = {
            'barra1': {
                'param': {
                    'master':  self.frame_principal, 'orient': 'horizontal', 'mode': 'determinate', 'length': 420,
                    'maximum': self.total_de_cadastros, 'value': 0, 'name': 'progresso'
                },
                'grid':  {'columnspan': 2, 'row': 1, 'padx': 5, 'pady': 10}
            }
        }
        self.progressbar(barra_de_progresso)

        labels = {
            'impressora':                   {
                'param': {
                    'master': self.frame_principal, 'text': 'Selecione a impressora', 'bg': self.cor_de_fundo,
                    'font':   self.fonte
                },
                'grid':  {'column': 0, 'row': 0, 'padx': 10, 'pady': 10}
            },
            'texto_info':                   {
                'param': {
                    'master': self.frame_principal, 'text': f'Analisando: ', 'bg': self.cor_de_fundo,
                    'font':   self.fonte
                },
                'grid':  {'column': 0, 'row': 2, 'padx': 10, 'pady': 10, 'sticky': 'e'}
            },
            'numero_info':                  {
                'param': {
                    'master': self.frame_principal, 'name': 'info', 'text': f'{self.linha_atual} de'
                                                                            f' {self.total_de_cadastros}',
                    'bg':     self.cor_de_fundo, 'font': self.fonte
                },
                'grid':  {'column': 1, 'row': 2, 'padx': 0, 'pady': 10, 'sticky': 'w'}
            },
            'texto_participantes_validos':  {
                'param': {
                    'master': self.frame_principal, 'text': 'Participantes válidos:', 'bg': self.cor_de_fundo,
                    'font':   self.fonte
                },
                'grid':  {'column': 0, 'row': 3, 'padx': 10, 'pady': 10, 'sticky': 'e'}
            },
            'numero_participantes_validos': {
                'param': {
                    'master': self.frame_principal, 'text': '-', 'name': 'numero_validos', 'bg': self.cor_de_fundo,
                    'font':   self.fonte
                },
                'grid':  {'column': 1, 'row': 3, 'padx': 0, 'pady': 10, 'sticky': 'w'}
            },
            'texto_cpfs_invalidos':         {
                'param': {
                    'master': self.frame_principal, 'text': 'CPFs inválidos:', 'bg': self.cor_de_fundo,
                    'font':   self.fonte
                },
                'grid':  {'column': 0, 'row': 4, 'padx': 10, 'pady': 10, 'sticky': 'e'}
            },
            'numero_cpfs_invalidos':        {
                'param': {
                    'master': self.frame_principal, 'text': '-', 'name': 'numero_invalidos', 'bg': self.cor_de_fundo,
                    'font':   self.fonte
                },
                'grid':  {'column': 1, 'row': 4, 'padx': 0, 'pady': 10, 'sticky': 'w'}
            },
            'texto_cadastro_repetido':      {
                'param': {
                    'master': self.frame_principal, 'text': 'Cadastros repetidos:', 'bg': self.cor_de_fundo,
                    'font':   self.fonte
                },
                'grid':  {'column': 0, 'row': 5, 'padx': 10, 'pady': 10, 'sticky': 'e'}
            },
            'numero_cadastro_repetido':     {
                'param': {
                    'master': self.frame_principal, 'text': '-', 'name': 'numero_repetidos', 'bg': self.cor_de_fundo,
                    'font':   self.fonte
                },
                'grid':  {'column': 1, 'row': 5, 'padx': 0, 'pady': 10, 'sticky': 'w'}
            },
        }
        self.label(labels)

        comboboxes = {
            'printers': {
                'param': {'master': self.frame_principal, 'name': 'impressora', 'values': self.listar_impressoras()},
                'grid':  {'column': 1, 'row': 0, 'padx': 10, 'pady': 10}
            }
        }
        self.combobox(comboboxes)

        botoes = {
            'iniciar': {
                'param': {
                    'master': self.frame_principal, 'name': 'bt_inicia_analise', 'command': self.inicia_verificacao,
                    'text':   'Iniciar análises'
                },
                'grid':  {'columnspan': 2, 'row': 6, 'padx': 10, 'pady': 10, 'sticky': 'nsew'}
            },
        }
        self.button(botoes)

        self.frame_principal.children['impressora'].current(5)

    def inicia_verificacao(self):
        print('1234...')
        self.t1 = threading.Thread(target = self.verifica, daemon = True)
        self.t1.start()
        self.frame_principal.children['bt_inicia_analise'].destroy()

    def verifica(self):
        ja_registrados = list()
        with open(file = self.path_arquivo, mode = 'r', encoding = 'UTF-16') as arquivo:
            for id, linha in enumerate(arquivo):
                if id == 0:
                    self.adiciona_info_filtrada(linha)
                else:
                    infos = linha.split('\t')
                    cpf = infos[2]
                    nome = infos[5]
                    if cpf not in ja_registrados and self.cpf_valido(cpf):
                        self.adiciona_info_filtrada(linha)

                        self.imprimir(cpf = self.mascara_cpf(cpf), nome = nome)
                        ja_registrados.append(cpf)

                        self.total_de_participantes_validos += 1
                self.atualiza_progresso()

                (self.show_info(titulo = 'Concluido', mensagem = 'Análise e impressões concluidas'))

    def abre_arquivo(self):
        extenssoes = [('Arquivos CSV', '*.csv')]
        self.path_arquivo = self.abrir_arquivo(titulo = 'Selecione o arquivo', extenssoes = extenssoes)
        with open(file = self.path_arquivo, mode = 'r') as arquivo_csv:
            for _ in arquivo_csv:
                self.total_de_cadastros += 1
            self.total_de_cadastros -= 1
            return arquivo_csv.close()

    def atualiza_progresso(self):
        frame_child = self.frame_principal.children
        self.linha_atual += 1
        repetidos = self.linha_atual - self.total_de_cpfs_invalidos - self.total_de_participantes_validos
        porcentagem = round(self.linha_atual / self.total_de_cadastros * 100, ndigits = 2)

        frame_child['progresso'].configure(value = self.linha_atual)
        frame_child['info'].configure(
            text = f'{self.linha_atual} de {self.total_de_cadastros} -- {porcentagem}%'
        )
        frame_child['numero_validos'].configure(text = self.total_de_participantes_validos)
        frame_child['numero_repetidos'].configure(text = repetidos)

    def cpf_valido(self, cpf):
        validado = validate(doc = cpf, doctype = 'cpf', lazy = False)
        if not validado:
            self.total_de_cpfs_invalidos += 1
            self.frame_principal.children['numero_invalidos'].configure(text = self.total_de_cpfs_invalidos)
        return validado

    @staticmethod
    def mascara_cpf(cpf):
        return parse(doc = cpf, doctype = 'cpf', mask = True)

    @staticmethod
    def adiciona_info_filtrada(linha):
        path = abspath('./Para análise/inscrições_filtradas.csv')
        with open(path, mode = 'a', encoding = 'UTF-16') as arquivo:
            arquivo.write(linha)
            arquivo.close()

    def binds(self):
        # Cria os binds na tela do root
        self.root.bind('<Escape>', lambda e: self.root.quit())
        self.root.bind('<Return>', self.inicia_verificacao)


if __name__ == '__main__':
    Main()
