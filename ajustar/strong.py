from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

session = HTMLSession()

# variáveis do projeto
projeto = 'romapvc.com.br'
htdocs = f'E://xampp/htdocs/{projeto}/' # alterar para htdocs proprio

# inserir os arquivos para serem editados (sem .php)
f = [
	# 'esquadria-pvc-imitando-madeira',
	'esquadrias-pvc-campos-do-jordao',
	# 'esquadrias-pvc-atibaia',
	# 'esquadrias-pvc-braganca-paulista',
	# 'esquadrias-aluminio-vinhedo',
	# 'esquadrias-pvc-valinhos',
	# 'esquadrias-pvc-preco',
	# 'fabrica-esquadrias-pvc',
	# 'fabrica-portas-pvc',
	# 'janela-maxim-ar-pvc-preco',
	# 'janelas-pvc-acustica',
	# 'janelas-pvc-medida'
]

Error = { 'Não foi possível ler o(s) arquivo(s)':[],'Não foi possível criar o arquivo':[],'Não foi possível realizar o ajustes no(s) arquivo(s)':[],'Não foi possível recuperar o título da página':[] }

# le arquivo e recupera valores
def file_read(f):
	content = []
	import os.path
	try:
		with open(f + '.php', 'r', encoding='utf8') as file:
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

# variáveis para mascara
elements = []
msk = '!!!PHP!!!'

# funções pra fazer a remoção
def remove(c):
    elements.append(c.group())
    return msk
def add(c):
    return elements.pop(0)

# funcao para aplicar/ retirar mascara no codigo
def mask(c, i):
	import re
	try:
		# aplica a mascara
		m = re.sub(r"<\?.*\?>|<\?php^\s.*\?>", remove, c)
		soup = BeautifulSoup(m, "html.parser")
		if i == True:
			mask = re.sub(msk, remove, soup.prettify())
		else:
			mask = re.sub(msk, add, soup.prettify())
	except:
		return False

# cria o arquivo
def create(body, file):
	from pathlib import Path
	arquivo = projeto + '/' + file
	# realiza a criacao dos arquivos
	try:

		# faz a criacao da pasta
		Path(f'./ajustar/projetos/{projeto}').mkdir(parents=True, exist_ok=True)

	    # faz a criacao dos arquivos
		with open(f'./ajustar/projetos/{arquivo}' + '.php', 'a', encoding='utf8') as f:
			f.write(body)
	except: 
	    Error['Não foi possível criar o arquivo'].append(f'=> {file}.php')

# faz o ajuste nos strongs do projeto
def fix_strong(t, html):
	# armazenando elementos
	content = []
	try:
		# criando o soup em html
		soup = BeautifulSoup(mask(html, True), "html5lib")
		# tenta rodar os ajustes
		for p in soup.find_all('p'):
			child = p.findChildren("strong", recursive=True)
			for strong in child:

				# ajusta quais não estão corretas
				if t.strip().lower() not in strong.string.lower():
					strong.string = t.strip().lower()

		# retorna novo código
		for elem in soup.prettify():
			content.append(elem)
		return ''.join(map(str, content))

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
				body = fix_strong(title, html)

				# tudo certo, gera o arquivo
				if body != False:
					# create(php_mask(body, False), a)
					print(body)
				else:
					print(Fore, RED)
					print('Falha na execução do strong.')

				# limpa cache
				del php_elements[:]

			except:
				Error['Não foi possível realizar o ajustes no(s) arquivo(s)'].append(f'=> {a}.php')
		
except:
	print(Fore.RED)
	print('Não foi possível iniciar a função.', Style.RESET_ALL)

print(Fore.RED)
# Exibe log na tela
for errosItens in Error.keys():

    if len(Error[errosItens]) > 0:
        print(errosItens+'\n')
        for errosValores in Error[errosItens]:
            print(errosValores)
        print('\n')
    else:
    	print(Fore.GREEN)
    	print('Todas as correções foram finalizadas com sucesso!')	
    	break

print(Style.RESET_ALL)

input('\nFinalizado. Aperte "ENTER" para encerrar o programa.')