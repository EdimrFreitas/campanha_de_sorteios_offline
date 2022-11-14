from os.path import abspath
from json import load


class Configs:
    def __init__(self):
        self.__abre_configs()

    def __abre_configs(self):
        path = abspath('./configs/configs.json')
        with open(file = path, mode = 'r', encoding = 'UTF-8') as arquivo_configs:
            configs = load(arquivo_configs)
            arquivo_configs.close()
        self.configs: dict = configs

    @property
    def cor_da_borda(self):
        return 'green'

    @property
    def cor_de_fundo(self):
        return 'lightgreen'

    @property
    def fonte(self):
        return 'Times 15 bold'
