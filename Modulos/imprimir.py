from time import sleep

from win32print import EnumPrinters

from win32printing import Printer


class Printing:
    # Cria uma lista com todas as impressoras configuradas na máquina
    @staticmethod
    def listar_impressoras():
        lista_de_impressoras = [impressora[2] for impressora in EnumPrinters(2)]
        return lista_de_impressoras

    def imprimir(self, cpf, nome):
        fonte_cpf = {
            "height": 10,
        }
        fonte_nome = {
            "height": 20,
        }
        impressora = self.frame_principal.children['impressora'].get()

        with Printer(linegap = 2, printer_name = impressora, doc_name = nome) as imprimir:
            imprimir.text(f"CPF: {cpf}", font_config = fonte_cpf)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(text = "", font_config = fonte_nome)
            imprimir.text(f"Nome: {nome}", font_config = fonte_nome)

        return sleep(0.1)
