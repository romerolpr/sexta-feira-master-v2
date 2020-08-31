from requests_html import HTMLSession
from tqdm.auto import tqdm
import re
import os

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
    'INSERIR URL AQUI'
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