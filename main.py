from os.path import abspath
from json import load
from tkinter import LabelFrame, Entry, Button, PhotoImage, Tk
from tkinter.ttk import Combobox, Progressbar


class Configs:
    def __init__(self):
        self.abre_configs()

    def abre_configs(self):
        path = abspath('./configs/configs.json')
        with open(file = path, mode = 'r', encoding = 'UTF-8') as arquivo_configs:
            configs = load(arquivo_configs)
            arquivo_configs.close()
        self.configs: dict = configs


class Main(Configs):
    def __init__(self):
        Configs.__init__(self)
        self.iniciar_root()

    def iniciar_root(self):
        # Parâmetros de  tamanh da tela
        tam_x, tam_y = 450, 400
        root = Tk(screenName = 'Controle de campanha')
        root.configure(background = self.cor_da_borda)
        # Parâmetros de posicionamento da janela na tela do usuário
        pos_x = int((root.winfo_screenwidth() - tam_x) / 2)
        pos_y = int((root.winfo_screenheight() - tam_y) / 2)
        root.geometry(f'{tam_x}x{tam_y}+{pos_x}+{pos_y}')
        # Seta como fixo os tamanhos da tela
        root.resizable(False, False)
        # Cria os binds na tela do root
        root.bind('<Escape>', lambda e: root.quit())
        root.bind('<Return>', lambda e: self.inicia_campanha())
        self.root = root
