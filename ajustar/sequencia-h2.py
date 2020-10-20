from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

session = HTMLSession()

# variáveis do projeto
projeto = 'gjdistribuidora.com.br'
htdocs = f'C://xampp/htdocs/{projeto}/' # alterar para htdocs proprio

# inserir os arquivos para serem editados (sem .php)
f = [
	'ordenhadeira-portatil-pequena',
	'ordenhadeira-quanto-custa',
	'ordenhadeira-valor',
	'pecas-motores-eletricos',
	'pecas-ordenha',
	'pecas-ordenha-canalizada',
	'valor-ordenhadeira-portatil',
]

Log = { 
	'O arquivo não possui sequência de H2': [],
	'Não foi possível realizar a adequação do H2': [],
}

Error = {
	'Não foi possível ler o(s) arquivo(s)':[],
	'Não foi possível criar o arquivo':[],
	'Não foi possível realizar o ajustes no(s) arquivo(s)':[],
	'Não foi possível recuperar o título da página':[], 'Falha na execução do strong.': [] 
}

Success = []

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
		Error['Não foi possível ler o(s) arquivo(s)'].append(f'=> {f}.php')

# montar url do temporario
def urlReplace(x, y):
	x = x.split('//')
	r = x[1].split('/')
	return 'http://mpitemporario.com.br/projetos/' + r[2] + '/' + y

# funcao para retirar os acentos
def removeAccent(string):
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
		if i == True:
			mask = re.sub(msk, remove, soup.prettify(formatter=None))
		else:
			mask = re.sub(msk, add, soup.prettify(formatter=None))
	except:
		mask = False

	return mask

# cria o arquivo
def create(body, file):
	from pathlib import Path
	arquivo = projeto + '/sequencia-h2/' + file
	# realiza a criacao dos arquivos
	try:

		# faz a criacao da pasta
		Path(f'./projetos/{projeto}/sequencia-h2/').mkdir(parents=True, exist_ok=True)

	    # faz a criacao dos arquivos
		with open(f'./projetos/{arquivo}' + '.php', 'w', encoding='utf-8') as f:
			f.write(body)
			f.write('</html>')
	except: 
	    Error['Não foi possível criar o arquivo'].append(f'=> {file}.php')

# faz o ajuste nos strongs do projeto
def fix_strong(t, html, a):
	import re
	# armazenando elementos
	content = []
	try:

		# criando o soup em html
		soup = BeautifulSoup(mask(html, True), "html.parser")
		title = t.strip()

		# tenta rodar os ajustes

		for p in soup.select('article'):

			child = p.select('h2 + h2')

			# verifica se o paragrafo tem sequencia de h2
			if child:
				for h2 in child:
					# if removeAccent(title).lower() != removeAccent(h2.string).lower():
					h2.name = 'p'
					h2.string = h2.string.lower().capitalize()
					# else:
						# Log['Não foi possível realizar a adequação do H2'].append(f'=> {a}')
			else:
				Log['O arquivo não possui sequência de H2'].append(f'=> {a}')

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
try:
	for a in tqdm(f):

		r = session.get(urlReplace(htdocs, a))
		# constroi o arquivo
		html = file_read(htdocs + a.strip())
		# retorna o title da pagina
		try:
			t = r.html.find('head title')
			for v in t:
				title = v.text.split('-')[0]
		except:
			Error['Não foi possível recuperar o título da página'].append(f'=> {urlReplace(htdocs, a)}')
		else:
			try:
				
				# Após receber todos os valores com sucesso, realiza os ajustes e retira a máscara do código
				body = fix_strong(title, html, a)

				# tudo certo, gera o arquivo
				if body != False:
					create(body, a)
					# print(body)
					Success.append(f'=> {a}.php')
				else:
					Error['Falha na execução do strong.'].append(f'=> {a}.php')

			except:
				Error['Não foi possível realizar o ajustes no(s) arquivo(s)'].append(f'=> {a}.php')

			del elements[:]
		
except:
	print(Fore.RED)
	print('Não foi possível iniciar a função.', Style.RESET_ALL)

# Exibe log na tela
print(Fore.RED)
for errosItens in Error.keys():
    if len(Error[errosItens]) > 0:

        print(errosItens)

        for errosValores in Error[errosItens]:
            print(errosValores)

        msg = 'Falha ao tentar executar funções.'
    else:
    	msg = 'Ajustes realizados com sucesso em ({}) projetos.'.format(len(Success))
	

print(Fore.YELLOW)
for logItens in Log.keys():
	if len(Log[logItens]) > 0:
	    print('!!! AVISO !!!\n')
	    print(logItens)
	    for logValores in Log[logItens]:
	        print(logValores)

if 'sucesso' in msg and len(Success) > 0:
	print(Fore.GREEN)
else:
	print(Fore.RED)

print('\n')
print(msg, Style.RESET_ALL)	

input('\nFinalizado. Aperte "ENTER" para encerrar o programa.')