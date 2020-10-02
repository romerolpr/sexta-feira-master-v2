from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

projeto = 'hidralpress.com.br'

# variáveis do sistema
VAR = {
	
	'htdocs': f'C://xampp/htdocs/{projeto}/',
	'url': 'mpitemporario.com.br/projetos/',
	'nova-mpi': False,

	# Recupera todas as mpis automaticamente
	'vAll': True,
	'vMPI': [
		'confeccao-moldes-plasticos'
	] 
}

Log = {

	'Warning': {
		'Não foi possível inserir o strong no parágrafo': [], 
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

session = HTMLSession()


def get_mpis(URL):
    rm = session.get(URL + 'mapa-site')
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
	except IOError:
		return False	
		Log['Error']['Não foi possível ler o(s) arquivo(s)'].append(f'=> {f}.php')

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
    elements.append(d.group())
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
	arquivo = projeto + '/strong/' + file
	# realiza a criacao dos arquivos
	try:

		# faz a criacao da pasta
		Path(f'./projetos/{projeto}/strong/').mkdir(parents=True, exist_ok=True)

	    # faz a criacao dos arquivos
		with open(f'./projetos/{arquivo}' + '.php', 'w', encoding='utf-8') as f:
			f.write(body)
			f.write('</html>')
	except: 
	    Log['Error']['Não foi possível criar o arquivo'].append(f'=> {file}.php')

# faz o ajuste nos strongs do projeto
def fix_strong(t, html, a):
	import re
	# armazenando elementos
	content = []
	try:

		# criando o soup em html
		soup = BeautifulSoup(mask(html, True), "html.parser")
		title = t.strip()

		method = '.mpi-content > p, .tabs-content > p' if VAR['nova-mpi'] else 'article > p'

		# tenta rodar os ajustes

		for p in soup.select(method):

			child = p.find_all('strong')

			# verifica se o paragrafo tem strong
			if child:
				for strong in child:
					# ajusta quais não estão corretas
					if remove_accent(title).lower() != remove_accent(strong.string).lower().strip():
						strong.string = title.lower()
			else:

				try:
					# insere onde não tem strong
					if remove_accent(title).lower() in remove_accent(p.string).lower().strip():
						r = remove_accent(p.string).lower().strip().replace(remove_accent(title).lower().strip(), '<strong>'+title.lower()+'</strong>')
						p.string = r
				except:
					Log['Warning']['Não foi possível inserir o strong no parágrafo'].append(f'=> {a}')
					return False
				

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

	for a in tqdm(VAR['vMPI']):

		r = session.get(url_replace(VAR['htdocs'], a))
		# constroi o arquivo
		html = file_read(VAR['htdocs'] + a.strip())
		# retorna o title da pagina
		try:
			t = r.html.find('head title')
			for v in t:
				title = v.text.split('-')[0]
		except:
			Log['Error']['Não foi possível recuperar o título da página'].append('=> {}'.format(url_replace(VAR['htdocs'], a)))
		else:
			try:
				
				# Após receber todos os valores com sucesso, realiza os ajustes e retira a máscara do código
				body = fix_strong(title, html, a)

				# tudo certo, gera o arquivo
				if body != False:
					create(body, a)
					# print(body)
					Log['Success'].append(f'=> {a}')
				else:
					Log['Error']['Falha na execução.'].append(f'=> {a}')
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