# v1.0 (Beta)
import json
import os
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style, init
import sys

init(autoreset=True)

# Converter objeto em json
def encode_json(config):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

# interação com os arquivos no data
def decode_json(load):
    with open(load + '.json', 'r', encoding='utf-8') as f:
        return json.load(f)

if os.path.isfile('config.json'):

	# Verifica se o htdocs está vazio
	htdocs = '' if decode_json('config')['htdocs'] == '' else decode_json('config')['htdocs']

	if htdocs == '':
		print(Fore.YELLOW + '\nEspecifique o endereço do htdocs')
		htdocs = str(input('$ '))
		encode_json({'htdocs': htdocs, 'code': decode_json('config')['code'], 'url': decode_json('config')['url'], 'sub-menu': decode_json('config')['sub-menu'], 'vAll': decode_json('config')['vAll'] })

else:

	print(Fore.YELLOW + '\nEspecifique o endereço do htdocs')
	htdocs = str(input('$ '))

	# Cria com os valores padrões
	encode_json({'htdocs': htdocs, 'code': '$caminhoBread2', 'url': 'mpitemporario.com.br/projetos/', 'sub-menu': False, 'vAll': True })

# Define as variáveis do sistema
VAR = { 
	'htdocs': decode_json('config')['htdocs'], 
	'code': decode_json('config')['code'],
	'url': decode_json('config')['url'],
	'sub-menu': decode_json('config')['sub-menu'],
	# Controle de interação MPIs
	'vAll': decode_json('config')['vAll'],
	# Lista para interar nas mpis manualmente
	'MPI': ['empresa-cilindros-hidraulicos-pneumaticos'],
}

# comandos do sistema
def commands(console):

	# help
	if ' help' in console or 'help' == console:
		print('planos_py, versão 1.0 (beta)')
		print('Comandos de execução')
		print(' -a      Inicia o programa.')
		print(' -s      Edita e salva variável já existente do sitema.   [var] [...] -s')
		print(' -p      Imprime na tela uma variável existente.          [var] -p')
		print('\nComandos rápidos')
		print(' clear   Limpa todos os elementos na tela.')
		print(' exit    Encerra todos os processos.')
		print(' help    Exibe comandos completos do sistema.')
		print(' var     Exibe todas as variáveis do sistema.')

	# comandos rápidos
	if ' clear' in console or 'clear' == console:
		clear = lambda: os.system('cls')
		clear()
	if 'exit' == console:
		print('Logout')
		sys.exit()
	if 'var' == console:
		print('Variáveis do sistema')
		for item in VAR.keys():
			if type(VAR[item]) == str:
				print(' ' + item + ': ' + VAR[item])
	if 'reset' == console:
		print(Fore.YELLOW + '\nVocê deseja realmente resetar todas as variáveis do sistema?' + Fore.CYAN + ' (y/ n)')
		reset = input("$ ")
		if reset.lower() == 'y':
		    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

	# comandos de execução
	if ' -p' in console:
		for event in VAR:
			if console.split(' -p')[0] in event:
				print(VAR[event])
	if ' -s' in console:

		nvar = console.split(' ')
		ncode = nvar[0]

		# deleta índices não uteis
		del nvar[0]
		del nvar[-1]
		for event in VAR:
			if ncode in VAR:
				if len(nvar) <= 1:
					VAR[ncode] = nvar[-1]
					encode_json(VAR)
					print(nvar[-1])
				else:
					VAR[ncode] = ' '.join(map(str, nvar))
					encode_json(VAR)
					print(' '.join(map(str, nvar)))
				break

while True:

	# Sistema
	Start 		= False
	terminal 	= ''

	# projeto
	while ' -a' not in terminal:
		print(Fore.YELLOW + '\nEspecifique o nome do projeto' + Fore.CYAN + ' (-a para iniciar)')
		terminal = str(input('$ '))
		# definindo funções do console
		if terminal not in ' -a':
			commands(terminal)
		else:
			Start = True if terminal else False

	# Variáveis interativas
	projeto 	= terminal.split(' -a')[0].strip()
	workplace 	= VAR['htdocs'] + projeto + '/'
	g 			= []

	# Rewrite url
	def url_replace(url, file):
		rewrite = 'http://' + VAR['url'] + projeto + '/' if not file else 'http://' + VAR['url'] + projeto + '/' + file
		return rewrite

	def get_mpis(URL):
		rm = session.get(URL + 'mapa-site')
		submenu = rm.html.find('.sitemap ul.sub-menu-info li a') if rm.html.find('.sitemap ul.sub-menu-info') else rm.html.find('.sitemap ul.sub-menu li a') if not VAR['sub-menu'] else rm.html.find(VAR['sub-menu'])
		for links in submenu:
			VAR['MPI'].append(links.attrs['href'].split('/')[-1])

	Log = {

		'Warning': {
			'Não foi possível inserir "{}" no arquivo'.format(VAR['code']): []
		},

		'Error': {
			'Não foi possível ler o(s) arquivo(s)':[],
			'Não foi possível criar o arquivo':[],
			'Não foi possível realizar o ajustes no(s) arquivo(s)':[],
			'Não foi possível recuperar o título da página':[],
			'Não foi possível inserir após o H2': [],
			'Não foi possível montar a sessão do projeto': [],
			'Não foi possível iniciar a função.': [],
			'Falha na execução.': [],
		},

		'Success': []
	}

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
		except IOLog['Error']:
			return False	
		
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
		import re
		arquivo = projeto + '/breadcrumb/' + file
		# realiza a criacao dos arquivos
		try:

			# faz a criacao da pasta
			Path(f'./projetos/{projeto}/breadcrumb/').mkdir(parents=True, exist_ok=True)

		    # faz a criacao dos arquivos
			with open(f'./projetos/{arquivo}' + '.php', 'w', encoding='utf-8') as f:

				body = body.replace('<!-- {} -->'.format(VAR['code']), '<?={}?>'.format(VAR['code']))
				body = re.sub(r'<\?=\s*\$caminho2\s*\?>', '', body)
				#cria
				f.write(body)
				f.write('</html>')
		except: 
		    Log['Error']['Não foi possível criar o arquivo'].append(f'=> {file}')

	# insere o codigo
	def add_content(t, html, a):


		# armazenando elementos
		content = []
		try:

			# criando o soup em html
			soup = BeautifulSoup(mask(html, True), "html.parser")

			# tenta rodar os ajustes

			for wrapper in soup.select('div.wrapper'):

				soup.find('h1').extract()

				tag = soup.new_tag('div')
				tag.string = '<!-- {} -->'.format(VAR['code'])

				wrapper.insert_before(tag)

			for e in elements:
				if '$h1' in e:
					del elements[elements.index(e)]


			# retorna novo código
			for elem in soup.prettify(formatter=None):
				content.append(elem)
			value = ''.join(map(str, content))

			return mask(value, False)

		except:
			return False

	# Inicia função principal para executar as correções
	# informa o projeto e metodo
	print(Fore.MAGENTA + f'\nmethod -a ' + Fore.YELLOW + '{}'.format('/' + workplace.split('//')[-1]) + Fore.CYAN + ' (running)\n')

	session = HTMLSession()

	try:
		
		try:

			if VAR['vAll']:
				get_mpis(url_replace(workplace, False))

		except:

			Log['Error']['Não foi possível recuperar as palavras chaves do projeto'].append(f'=> {url_replace(workplace, a)}')

		else:

			for a in tqdm(VAR['MPI']):

				# monta sessão
				r = session.get(url_replace(workplace, a))

				# lê e monta o arquivo
				html = file_read(workplace + a.strip())
				if not html:
					# exibe erro se nao conseguir ler o arquivo
					Log['Error']['Não foi possível ler o(s) arquivo(s)'].append(f'=> {a}')
					break
				# retorna o title da pagina
				try:
					t = r.html.find('head title')
					for v in t:
						title = v.text.split('-')[0]
				except:
					Log['Error']['Não foi possível recuperar o título da página'].append(f'=> {url_replace(workplace, a)}')
				else:
					try:
						
						# Após receber todos os valores com sucesso, realiza os ajustes e retira a máscara do código
						body = add_content(title, html, a)

						if body != False:
							create(body, a)
							# print(body)
							g.append(a)
							Log['Success'].append(f'=> {a}')
						else:
							Log['Error']['Falha na execução.'].append(f'=> {a}')

					except:
						Log['Error']['Não foi possível realizar o ajustes no(s) arquivo(s)'].append(f'=> {a}')

					del elements[:]
			
	except:
		Log['Error']['Não foi possível iniciar a função.'].append('=> {}'.format(workplace))

	# Exibe log na tela
	for x in Log.keys():
		for y in Log[x]:
			if x == 'Success':
				print('\nForam realizados {}/{} ajustes no projeto.'.format(len(Log['Success']), len(VAR['MPI'])))
				break
			else:
				if len(Log[x][y]) > 0:
					print('\n' + y)
					for z in Log[x][y]:
						print(' ' + z)

	Start = False
	workplace = VAR['htdocs']

	del VAR['MPI'][:]