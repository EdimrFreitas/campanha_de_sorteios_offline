import threading
from tkinter import Tk
from tkinter.messagebox import showinfo

from docbr import parse, validate

from Modulos.arquivo import AbreArquivo
from Modulos.configs import Configs
from Modulos.construtor import Construtor
from Modulos.imprimir import Printing


class Main(Configs, Printing, AbreArquivo, Tk):
    total_de_cadastros = 0
    total_de_participantes_validos = 0
    total_de_cpfs_invalidos = 0
    linha_atual = 0

    def __init__(self):
        Configs.__init__(self)
        Tk.__init__(self)
        self.iniciar_root()
        AbreArquivo.__init__(self)
        self.inicia_frame()
        self.inicia_widgets()
        self.binds()

        self.mainloop()

    def iniciar_root(self):
        # Parâmetros de  tamanh da tela
        tam_x, tam_y = 450, 425
        self.configure(**self.root_param)
        self.title('Verificador offline')
        # Parâmetros de posicionamento da janela na tela do usuário
        pos_x = int((self.winfo_screenwidth() - tam_x) / 2)
        pos_y = int((self.winfo_screenheight() - tam_y) / 2)
        self.geometry(f'{tam_x}x{tam_y}+{pos_x}+{pos_y}')
        # Seta como fixo os tamanhos da tela
        self.resizable(False, False)

    def inicia_frame(self):
        frame = dict()

        frame['frame_principal'] = {
            'param': {'master': self, 'name': 'principal', **self.frame_param},
            'place': {'relwidth': 0.96, 'relheight': 0.96, 'relx': 0.02, 'rely': 0.02}
        }
        Construtor.frame(frame)

    def inicia_widgets(self):
        frame_principal = self.children['principal']
        labels = dict()
        barra_de_progresso = dict()
        comboboxes = dict()
        botoes = dict()

        labels['impressora1'] = {
            'param': {'master': frame_principal, 'text': 'Selecione a impressora 1', **self.labels_param},
            'grid': {'column': 0, 'row': 0, 'padx': 10, 'pady': 10}
        }

        comboboxes['printer1'] = {
            'param': {'master': frame_principal, 'name': 'impressora1', 'values': self.listar_impressoras()},
            'grid': {'column': 1, 'row': 0, 'padx': 10, 'pady': 10}
        }

        labels['impressora2'] = {
            'param': {'master': frame_principal, 'text': 'Selecione a impressora 2', **self.labels_param},
            'grid': {'column': 0, 'row': 1, 'padx': 10, 'pady': 10}
        }

        comboboxes['printer2'] = {
            'param': {'master': frame_principal, 'name': 'impressora2', 'values': self.listar_impressoras()},
            'grid': {'column': 1, 'row': 1, 'padx': 10, 'pady': 10}
        }

        barra_de_progresso['barra1'] = {
            'param': {
                'master': frame_principal, 'orient': 'horizontal', 'mode': 'determinate', 'length': 420,
                'maximum': self.total_de_cadastros, 'value': 0, 'name': 'progresso'
            },
            'grid': {'columnspan': 2, 'row': 2, 'padx': 5, 'pady': 10}
        }

        labels['texto_info'] = {
            'param': {'master': frame_principal, 'text': f'Analisando: ', **self.labels_param},
            'grid': {'column': 0, 'row': 3, 'padx': 10, 'pady': 10, 'sticky': 'e'}
        }

        labels['numero_info'] = {
            'param': {
                'master': frame_principal, 'name': 'info', 'text': f'{self.linha_atual} de {self.total_de_cadastros}',
                **self.labels_param
            },
            'grid': {'column': 1, 'row': 3, 'padx': 0, 'pady': 10, 'sticky': 'w'}
        }

        labels['texto_participantes_validos'] = {
            'param': {'master': frame_principal, 'text': 'Participantes válidos:', **self.labels_param},
            'grid': {'column': 0, 'row': 4, 'padx': 10, 'pady': 10, 'sticky': 'e'}
        }

        labels['numero_participantes_validos'] = {
            'param': {'master': frame_principal, 'text': '-', 'name': 'numero_validos', **self.labels_param},
            'grid': {'column': 1, 'row': 4, 'padx': 0, 'pady': 10, 'sticky': 'w'}
        }

        labels['texto_cpfs_invalidos'] = {
            'param': {'master': frame_principal, 'text': 'CPFs inválidos:', **self.labels_param},
            'grid': {'column': 0, 'row': 5, 'padx': 10, 'pady': 10, 'sticky': 'e'}
        }

        labels['numero_cpfs_invalidos'] = {
            'param': {'master': frame_principal, 'text': '-', 'name': 'numero_invalidos', **self.labels_param},
            'grid': {'column': 1, 'row': 5, 'padx': 0, 'pady': 10, 'sticky': 'w'}
        }

        labels['texto_cadastro_repetido'] = {
            'param': {'master': frame_principal, 'text': 'Cadastros repetidos:', **self.labels_param},
            'grid': {'column': 0, 'row': 6, 'padx': 10, 'pady': 10, 'sticky': 'e'}
        }

        labels['numero_cadastro_repetido'] = {
            'param': {'master': frame_principal, 'text': '-', 'name': 'numero_repetidos', **self.labels_param},
            'grid': {'column': 1, 'row': 6, 'padx': 0, 'pady': 10, 'sticky': 'w'}
        }

        botoes['iniciar'] = {
            'param': {
                'master': frame_principal, 'name': 'bt_inicia_analise', 'command': self.inicia_verificacao,
                'text': 'Iniciar análises'
            },
            'grid': {'columnspan': 2, 'row': 7, 'padx': 10, 'pady': 10, 'sticky': 'nsew'}
        }

        Construtor.label(labels)
        Construtor.combobox(comboboxes)
        Construtor.progressbar(barra_de_progresso)
        Construtor.button(botoes)

        frame_principal.children['impressora1'].current(0)

    def inicia_verificacao(self):
        t1 = threading.Thread(target=self.verifica, daemon=True)
        t1.start()
        self.children['principal'].children['bt_inicia_analise'].destroy()

    def verifica(self):
        ja_registrados = list()
        self.dicionario_arquivo_filtrado.writeheader()
        impressora1 = self.children['principal'].children['impressora1'].get()
        impressora2 = self.children['principal'].children['impressora2'].get()
        qual_impressora = True
        for cadastro in self.dicionario_arquivo:
            cpf_bruto = str(cadastro['CPF (sem pontos e traço ex: 12345678900)'])
            cpf = self.mascara_cpf(cpf_bruto)
            if cpf not in ja_registrados and self.valida_cpf([cpf]):
                self.total_de_participantes_validos += 1

                if not impressora2:
                    impressora_atual = impressora1
                elif qual_impressora:
                    impressora_atual = impressora1
                    qual_impressora = not qual_impressora
                elif not qual_impressora:
                    impressora_atual = impressora2
                    qual_impressora = not qual_impressora

                self.imprimir(cpf=cpf, nome=cadastro['Nome completo'].capitalize(), impressora=impressora_atual)
                self.dicionario_arquivo_filtrado.writerow(cadastro)
                ja_registrados.append(cpf)

            self.atualiza_progresso()

        (self.show_info(titulo='Concluido', mensagem='Análise e impressões concluidas'))

    def atualiza_progresso(self):
        frame_child = self.children['principal'].children

        self.linha_atual = self.dicionario_arquivo.line_num-1
        repetidos = self.linha_atual - self.total_de_cpfs_invalidos - self.total_de_participantes_validos
        porcentagem = round(self.linha_atual / self.total_de_cadastros * 100, ndigits=2)

        frame_child['progresso'].configure(value=self.linha_atual)
        frame_child['info'].configure(text=f'{self.linha_atual} de {self.total_de_cadastros} -- {porcentagem}%')
        frame_child['numero_validos'].configure(text=self.total_de_participantes_validos)
        frame_child['numero_invalidos'].configure(text=self.total_de_cpfs_invalidos)
        frame_child['numero_repetidos'].configure(text=repetidos)

    def valida_cpf(self, cpf):
        validado = validate(doc=cpf, doctype='cpf', lazy=False)
        if not validado:
            self.total_de_cpfs_invalidos += 1
        return validado

    @staticmethod
    def mascara_cpf(cpf):
        return parse(doc=cpf, doctype='cpf', mask=True)

    def binds(self):
        # Cria os binds na tela do root
        self.bind('<Escape>', lambda e: self.quit())
        self.bind('<Return>', lambda e: self.inicia_verificacao())

    @staticmethod
    def show_info(titulo, mensagem):
        return showinfo(title=titulo, message=mensagem)


if __name__ == '__main__':
    Main()
