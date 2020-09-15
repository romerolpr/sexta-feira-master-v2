from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

session = HTMLSession()

# variáveis do projeto
projeto = 'markmed.com.br'
htdocs = f'C://xampp/htdocs/{projeto}/' # alterar para htdocs proprio

# Quando "True", 
# ignora os arquivos inseridos manualmente na lista, 
# e pega todas as mpis automaticamente
vAll = False

# inserir os arquivos para serem editados (sem .php)
f = [
	'cateter-oxigenio',
	'fabricantes-material-medico-hospitalar',
	'empresas-material-medico-hospitalar'
]

Log = { 
	'Não foi possível ajustar a description': [],
	'Description atual está correta.': [],
}

Error = {'Não foi possível ler o(s) arquivo(s)':[],'Não foi possível criar o arquivo':[],'Não foi possível realizar o ajustes no(s) arquivo(s)':[],'Não foi possível recuperar o título da página':[], 'Falha na execução.': [], 'Não foi possível iniciar a função.': [], }
Success = []

# pegar todas as mpis

def get_mpis(URL):
    rm = session.get(URL + 'mapa-site')
    subMenuInfo = rm.html.find('.sitemap ul.sub-menu-info li a')

    for linkMPI in subMenuInfo:
        f.append(linkMPI.attrs['href'].split('/')[-1])

# le arquivo e recupera valores
def file_read(f):
	content = []
	import os.path
	try:
		with open(f + '.php', 'r', encoding='utf-8') as file:
			lines = file.readlines()
			for elem in lines:
				content.append(elem)
				# string converter
			return ''.join(map(str, content))
	except IOError:
		return False	
		Error['Não foi possível ler o(s) arquivo(s)'].append(f'=> {f}')

# montar url do temporario
def url_replace(path, file):
	path = path.split('//')
	r = path[1].split('/')
	if file:
		return 'http://mpitemporario.com.br/projetos/' + r[2] + '/' + file
	else:
		return 'http://mpitemporario.com.br/projetos/' + r[2] + '/'

# funcao para retirar os acentos
def remove_accent(string):
	from unidecode import unidecode
	return unidecode(string)

# variáveis para mascara
elements = []
msk = '!!!PHP!!!'

# funções pra fazer a remoção
def remove(d):
    elements.append(d.group().strip())
    return msk
def add(e):
    return elements.pop(0)

# funcao para aplicar/ retirar mascara no codigo
def mask(c, i):
	import re
	try:

		# aplica a mascara
		m = re.sub(r"<\?.*\?>", remove, c)
		soup = BeautifulSoup(m, "html.parser")

		mask = re.sub(msk, remove, str(soup.prettify(formatter=None))) if i else re.sub(msk, add, str(soup.prettify(formatter=None)))
			
	except:
		mask = False

	return mask

# cria o arquivo
def create(body, file):
	from pathlib import Path
	arquivo = projeto + '/' + file
	# realiza a criacao dos arquivos
	try:

		# faz a criacao da pasta
		Path(f'./projetos/{projeto}').mkdir(parents=True, exist_ok=True)

	    # faz a criacao dos arquivos
		with open(f'./projetos/{arquivo}' + '.php', 'w', encoding='utf-8') as f:
			f.write(body)
			f.write('</html>')
	except: 
	    Error['Não foi possível criar o arquivo'].append(f'=> {file}')

# faz o ajuste nos strongs do projeto
def fix_code(t, html, a):
	import re
	# armazenando elementos
	content = []
	try:

		# removendo tags
		m = re.search(r"\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]", html)
		sub = re.sub(r'<.*>', '', m.group(0)).strip()

		# redigita o código
		html = re.sub(r'\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]', sub, html)

		# criando o soup em html
		soup = BeautifulSoup(mask(html, True), "html.parser")
		title = t.strip()

		# resgata a description atual no mpitemporario e arquiivo local
		currentDesc = session.get(url_replace(htdocs, a)).html.find('head meta[name="description"]', first=True).attrs['content']

		# verifica se a description está realmente errada
		descfix = True if remove_accent(title.lower()) not in remove_accent(currentDesc.lower()) or re.search(r'<.*>', m.group()) else False

		if descfix:
			# resgata os paragrafos
			article = session.get(url_replace(htdocs, a)).html.find('article p')
			# verifica a description
			for p in article:

				# compara já retirando acentos
				a = p.text.lower().find(remove_accent(title).lower())
				b = remove_accent(p.text).lower().find(title.lower())
				
				if b >= 0:
					if len(p.text[b:]) >= 125:
						desc = remove_accent(p.text[b:]).strip()
						break
				elif a >= 0:
					if len(p.text[a:]) >= 125:
						desc = p.text[a:].strip()
						break

			if desc:
				if desc[-1] == '.' and len(desc) >= 140 and len(desc) <= 160 :
				    desc = desc.lower()
				else:
					while len(desc) > 145:
					    desc = desc.split(" ")
					    del desc[-1]
					    desc = " ".join(desc)

					desc.lower()
					desc += '... saiba mais.'.encode("latin1").decode("unicode_escape")

				desc = f'$desc				= "{desc.capitalize()}";'

				# print(desc)

			else:
				Log['Não foi possível ajustar a description'].append(f'=> {a}')

		else:
			Log['Description atual está correta.'].append(f'=> {a}')

		# aplica a nova description

		# retorna novo código
		for elem in soup.prettify(formatter=None):
			content.append(elem)
		value = ''.join(map(str, content))

		value = re.sub(r"\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]", desc, str(soup)) if desc else value

		return mask(value, False)

	except:
		return False


# Inicia função principal para executar as correções
print(Fore.YELLOW)
print('Iniciando correções... Aguarde\n', Style.RESET_ALL)
	
if vAll:
	del f[:]
	get_mpis(url_replace(htdocs, False))

try:
	import re

	for a in tqdm(f):

		r = session.get(url_replace(htdocs, a))

		# constroi o arquivo
		html = file_read(htdocs + a.strip())

		try:
			# retorna o title da pagina local
			title = re.search(r"\$h1\s*=\s*[\"\']\w*\s*.+[\"\'\;]", html).group(0)
			title = re.search(r"\s*[\"\']\w*\s*.+[\"\']", title).group(0).replace('"', '').strip()
		except:
			# retorna erro do title
			Error['Não foi possível recuperar o título da página'].append(f'=> {a}')
		else:
			try:

				# Após receber todos os valores com sucesso, realiza os ajustes e retira a máscara do código
				body = fix_code(title, html, a)

				# tudo certo, gera o arquivo
				if body != False:
					create(body, a)
					# print(body)
					Success.append(f'=> {a}')
				else:
					Error['Falha na execução.'].append(f'=> {a}')

			except:
				Error['Não foi possível realizar o ajustes no(s) arquivo(s)'].append(f'=> {a}')

			del elements[:]
		
except:
	Error['Não foi possível iniciar a função.'].append(f'=> {htdocs}')

# Exibe log na tela
print(Fore.RED)
for errosItens in Error.keys():
    if len(Error[errosItens]) > 0:

        print(errosItens)

        for errosValores in Error[errosItens]:
            print(errosValores)

        msg = 'Falha ao tentar executar 1 ou mais funções.'
    else:
    	msg = 'Ajustes realizados em ({}) projetos.'.format(len(Success))
	

print(Fore.YELLOW)
for logItens in Log.keys():
	if len(Log[logItens]) > 0:
	    print('!!! AVISO !!!\n')
	    print(logItens)
	    for logValores in Log[logItens]:
	        print(logValores)

if len(Success) > 0:
	print(Fore.GREEN)
else:
	print(Fore.RED)

print('\n')
print(msg, Style.RESET_ALL)	

input('\nFinalizado. Aperte "ENTER" para encerrar o programa.')