from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

session = HTMLSession()

# variáveis do projeto
projeto = 'bumeranguebrindes.com'
htdocs = f'C://xampp/htdocs/{projeto}/' # alterar para htdocs proprio

# variáveis do sistema
VAR = {
	
	'htdocs': f'C://xampp/htdocs/{projeto}/',
	'url': 'localhost/',
	'nova-mpi': False,

	# Recupera todas as mpis automaticamente
	'vAll': False,
	'vMPI': [
		# Inserir aqui arquivos manualmentes (sem .php)
		'brindes-personalizados-comprar',
		'brindes-personalizados-empresas',
		'brindes-personalizados-eventos-empresariais',
		'brindes-personalizados-feiras',
		'camisas-personalizadas',
		'camisas-personalizadas-atacado',
		'camisas-personalizadas-mg',
		'camisas-personalizadas-empresas',
		'camisas-personalizadas-preco',
		'camisetas-personalizadas-bh',
		'caneca-acrilico-personalizada',
		'chinelos-personalizados',
		'chinelos-personalizados-brindes',
		'comprar-camisas-personalizadas',
		'empresa-brinde',
		'empresa-brindes-personalizados',
		'empresa-brindes-promocionais',
		'empresa-camisetas-personalizadas',
		'empresa-chinelos-personalizados',
		'empresa-chinelos-personalizados-casamento',
		'empresa-que-faz-brindes-personalizados',
		'fabrica-chinelos-personalizados',
		'fabrica-camisa-personalizada',
		'fornecedor-chinelos-personalizados',
		'fornecedores-camisas-personalizadas',
		'papel-arroz-personalizado',
		'papel-arroz-personalizado-comprar',
		'papel-arroz-personalizado-preco',
		'papel-arroz-personalizado-valor',
		'preco-chinelos-personalizados',
		'preco-topo-bolo-personalizado',
		'servicos-graficos',
		'servicos-graficos-comunicacao-visual',
		'servicos-graficos-geral',
		'taca-gin-brindes',
		'taca-gin-personalizada-acrilico',
		'taca-gin-acrilico-atacado',
		'taca-gin-acrilico-personalizada-bh',
		'topo-bolo-personalizado',
		'topo-bolo-personalizado-preco',
		'valor-chinelos-personalizados',
		'valor-topo-bolo-personalizado',
	] 
}

Log = {

	'Warning': {
		'O arquivo não possui H2': [],
	},

	'Error': {
		'Não foi possível ler o(s) arquivo(s)': [],
		'Não foi possível criar o arquivo': [],
		'Não foi possível realizar o ajustes no(s) arquivo(s)': [],
		'Não foi possível recuperar o título da página': [],
		'Não foi possível inserir strong no parágrafo do arquivo': [],
		'Não foi possível iniciar a função.': [],
		'Falha na execução.': [],
	},

	'Success': []
}

# remover os arquivos caso exista
def remove_files():
	import os
	path = 'projetos/' + projeto
	dir = os.listdir(path)
	for file in dir:
	    os.remove(file)
	    return True

# pegar todas as mpis

def get_mpis(url):
    rm = session.get(url + 'mapa-site')
    subMenuInfo = rm.html.find('.sitemap ul.sub-menu-info li a')

    for linkMPI in subMenuInfo:
        VAR['vMPI'].append(linkMPI.attrs['href'].split('/')[-1])

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
	except IOLog:
		return False	
		Log['Error']['Não foi possível ler o(s) arquivo(s)'].append(f'=> {f}')

# montar url do temporario
def url_replace(url, file):
	rewrite = 'http://' + VAR['url'] + projeto + '/' if not file else 'http://' + VAR['url'] + projeto + '/' + file
	return rewrite

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
	arquivo = projeto + '/h2 = h1/' + file
	# realiza a criacao dos arquivos
	try:

		# faz a criacao da pasta
		Path(f'./projetos/{projeto}/h2 = h1/').mkdir(parents=True, exist_ok=True)

	    # faz a criacao dos arquivos
		with open(f'./projetos/{arquivo}' + '.php', 'w', encoding='utf-8') as f:
			f.write(body)
			f.write('</html>')
	except: 
	    Log['Error']['Não foi possível criar o arquivo'].append(f'=> {file}')

# faz o ajuste nos strongs do projeto
def add_content(t, html, a):
	import re
	# armazenando elementos
	content = []
	try:

		method = '.mpi-content > p, .tabs-content > p' if VAR['nova-mpi'] else 'article > p'

		# criando o soup em html
		soup = BeautifulSoup(mask(html, True), "html.parser")
		title = t.lower().strip()

		# tenta rodar os ajustes

		for i in soup.select('article'):

			Element = i.find_all('h2')

			# verifica se o paragrafo tem sequencia de h2
			if Element:
				for e in Element:
					if e.string.lower().strip() == title:
						e.string = 'CONHEÇA MAIS SOBRE ' + e.string.strip()
			else:
				Log['O arquivo não possui H2'].append(f'=> {a}')

		# retorna novo código
		for elem in soup.prettify(formatter=None):
			content.append(elem)
		value = ''.join(map(str, content))

		return mask(value, False)

	except:
		return False


# Inicia função principal para executar as correções
print(Fore.YELLOW)
print('Iniciando correções... Aguarde\n', Style.RESET_ALL)
	
if VAR['vAll']:
	del VAR['vMPI'][:]
	get_mpis(url_replace(VAR['htdocs'], False))

try:
	import re

	for a in tqdm(VAR['vMPI']):

		a = a.strip()

		r = session.get(url_replace(VAR['htdocs'], a))

		# constroi o arquivo
		html = file_read(VAR['htdocs'] + a.strip())

		try:
			# retorna o title da pagina local
			title = re.search(r"\$h1\s*=\s*[\"\']\w*\s*.+[\"\'\;]", html).group(0)
			title = re.search(r"\s*[\"\']\w*\s*.+[\"\']", title).group(0).replace('"', '').strip()
		except:
			# retorna erro do title
			Log['Error']['Não foi possível recuperar o título da página'].append(f'=> {a}')
		else:
			try:

				# Após receber todos os valores com sucesso, realiza os ajustes e retira a máscara do código
				body = add_content(title, html, a)

				# tudo certo, gera o arquivo
				if body != False:
					# if remove_files():
					create(body, a)
					# print(body)
					Log['Success'].append(f'=> {a}')
				else:
					Log['Error']['Falha na execução.'].append(f'=> {a}')
					# print(body)

			except:
				Log['Error']['Não foi possível realizar o ajustes no(s) arquivo(s)'].append(f'=> {a}')

			del elements[:]
		
except:
	Log['Error']['Não foi possível iniciar a função.'].append('=> {}'.format(VAR['htdocs']))

# Exibe log na tela
for x in Log.keys():
	for y in Log[x]:
		if x == 'Success':
			print('\nForam realizados {}/{} ajustes no projeto.'.format(len(Log['Success']), len(VAR['vMPI'])))
			break
		else:
			if len(Log[x][y]) > 0:
				print('\n' + y)
				for z in Log[x][y]:
					print(' ' + z)

input('\nFinalizado. Aperte "ENTER" para encerrar o programa.')
