from requests_html import HTMLSession
from tqdm.auto import tqdm
import re

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
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/alarme-monitoramento-24-horas ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/camera-gravacao-nuvem ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/cameras-alarmes ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/empresa-monitoramento-24-horas ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/empresa-seguranca-eletronica ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/empresa-seguranca-eletronica-sp ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/empresa-terceirizacao-servicos-portaria ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/instalacao-sistema-cameras-seguranca ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/monitoramento-alarme ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/seguranca-portaria-24-horas ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/terceirizacao-portaria ',
    'http://mpitemporario.com.br/projetos/omegaserv.com.br/terceirizada-limpeza '
]

naoAjustado = []

session = HTMLSession()

for pagina in tqdm(urls):
    r = session.get(pagina)
    AjustaDescription(arquivo(pagina), r)

if len(naoAjustado) > 0:
    print(f"\n Description que nao conseguimos ajustar :( \n")
    for link in naoAjustado:
        print(link)