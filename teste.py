from os.path import abspath
import magic


arquivo = abspath('./Para análise/Testando.csv')
arquivo = abspath('sorteio 11.csv')

with open(file=arquivo) as csv:
    x = magic.detect_from_content(csv)
    print(x)
