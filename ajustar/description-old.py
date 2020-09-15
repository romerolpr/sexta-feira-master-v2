from requests_html import HTMLSession
from tqdm.auto import tqdm
import re
import os

descriptionOK = False

def AjustaDescription(arquivo ,r):
    h1 = r.html.find('h1')[0].text.lower()
    todosParagrafo = r.html.find('article p')
    for p in todosParagrafo:
        i = p.text.lower().find(h1)
        if i >= 0:
            if len(p.text[i:]) >= 125:
                novaDescription = p.text[i:]
                descriptionOK = True
                break

        else:
            descriptionOK = False
    
    if descriptionOK:
        if novaDescription[-1] == '.' and len(novaDescription) >= 140 and len(novaDescription) <= 160 :
            novaDescription = novaDescription.capitalize()

        else:
            while len(novaDescription) > 145:
                novaDescription = novaDescription.split(" ")
                del novaDescription[-1]
                novaDescription = " ".join(novaDescription)

            novaDescription = novaDescription.capitalize()
            novaDescription += "... Saiba mais.".encode("latin1").decode("unicode_escape")
        
        novaDescription = f"$desc           = \"{novaDescription}\";"
        mpi = open(f"{arquivo}.php", "rt", -1, "utf-8")
        dados = mpi.read()
        dados = re.sub(r"\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]", novaDescription, dados)
        mpi = open(f"{arquivo}.php", "wt", -1, "utf-8")
        mpi.write(dados)
        mpi.close()

    else:
        naoAjustado.append(f"=> {arquivo}")

def arquivo(url):
    url = url.split('//')
    url = url[1].split('/')
    return url[-1]

urls = [
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/bolsa-termica-atacado-personalizada',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/bolsa-termica-fabricante',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/bolsa-termica-fitness-atacado',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/bolsa-termica-empresas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/bolsa-termica-personalizada',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/bolsas-necessaires-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/bolsas-personalizadas-corporativas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/bolsas-personalizadas-empresas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/bolsas-personalizadas-eventos',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/comprar-necessaire-atacado',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/confeccao-mochilas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/confeccao-mochilas-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/empresa-malas-viagem',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/empresa-malas-mochilas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/empresa-mochilas-esportivas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/empresa-fabricante-mochila',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-bolsa-termica',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-bolsa-termica-personalizada',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-bolsas-mochilas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-bolsas-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-malas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-malas-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-mochilas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-mochilas-bolsas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-mochilas-escolares',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-mochilas-escolares-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabrica-mochilas-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fabricante-bolsa-termica-personalizada',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/fornecedores-mochilas-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/industria-mochilas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mala-empresa',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/malas-corporativas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/malas-viagem-empresa',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/malas-ecologicas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/malas-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/malas-personalizadas-empresas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochila-carrinho-executivo',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochila-corporativa-personalizada',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochila-rodinha-corporativa',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochila-ecologica',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochila-ecologica-comprar',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochila-sustentavel',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-corporativas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-ecologicas-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-executivas-notebook',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-executivas-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-brinde-personalizado',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-brindes-corporativos',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-empresas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-eventos',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-personalizadas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-personalizadas-faculdade',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-personalizadas-empresas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-personalizadas-eventos',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-personalizadas-lembrancinhas',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/mochilas-promocionais',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/necessaire-corporativa',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/necessaire-couro-ecologico',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/necessaire-ecologica',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/necessaire-ecologica-personalizada',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/necessaire-empresa',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/necessaire-personalizada-empresa',
    'http://mpitemporario.com.br/projetos/nowbuck.com.br/shoulder-bag-personalizada',
]

naoAjustado = []

session = HTMLSession()

try:
    for pagina in tqdm(urls):
        r = session.get(pagina)
        AjustaDescription(arquivo(pagina), r)
except IOError:
    print('\nO arquivo especificado não existe.')

if len(naoAjustado) > 0:
    print(f"\n Description que nao conseguimos ajustar :( \n")
    for link in naoAjustado:
        print(link)

confirm = input('\nAperte a tecla "ENTER" para encerrar o programa')

os.remove('description.py')