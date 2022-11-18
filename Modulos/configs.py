from os.path import abspath
from json import load


class Configs:
    def __init__(self):
        self.__abre_configs()

    def __abre_configs(self):
        path = abspath('./configs/configs.json')
        with open(file=path, mode='r', encoding='UTF-8') as arquivo_configs:
            configs = load(arquivo_configs)
            arquivo_configs.close()
        self.configs: dict = configs

    @property
    def __cor_da_borda(self):
        return 'green'

    @property
    def __cor_de_fundo(self):
        return 'lightgreen'

    @property
    def __fonte(self):
        return 'Times 15 bold'

    @property
    def labels_param(self):
        param = {
            'bg': self.__cor_de_fundo,
            'font': self.__fonte
        }
        return param

    @property
    def frame_param(self):
        param = {
            'bg': self.__cor_de_fundo
        }
        return param

    @property
    def root_param(self):
        param = {
            'bg': self.__cor_da_borda
        }
        return param