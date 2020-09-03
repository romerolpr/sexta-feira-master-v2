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
	'esquadria-pvc-imitando-madeira',
	# 'esquadrias-pvc-campos-do-jordao',
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

# le arquivo e recupera valores
def file_read(f):
	import os.path
	content = []
	try:
		with open(f + '.php', 'r', encoding='utf8') as file:
			lines = file.readlines()
			for elem in lines:
				content.append(elem)
				# string converter
				value = ''.join(str(e) for e in content)
			return value
	except IOError:
		return False	
		Error['Não foi possível ler o(s) arquivo(s)'].append(f'=> {f}.php')

# montar url do temporario
def urlReplace(x, y):
	x = x.split('//')
	r = x[1].split('/')
	URL = 'http://mpitemporario.com.br/projetos/' + r[2] + '/' + y
	return URL

# variáveis para mascara
php_elements = []

# funções pra fazer a remoção
def php_remove(c):
    php_elements.append(c.group())
    return '!!!PHP!!!'
def php_add(c):
    return php_elements.pop(0)

# funcao para aplicar/ retirar mascara no codigo
def php_mask(c, i):
	import re
	try:

		m = re.sub(r'<\?.*?\?>', php_remove, c, flags=re.S+re.M)
		soup = BeautifulSoup(m, "html.parser")

		if i == True:
			mask = re.sub('!!!PHP!!!', php_remove, soup.prettify())
		else:
			mask = re.sub('!!!PHP!!!', php_add, soup.prettify())

	except:
		return False
	else:
		return mask.strip()

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
			f.write(php_mask(body, False))
	except: 
	    Error['Não foi possível criar o arquivo'].append(f'=> {file}.php')

# faz o ajuste nos strongs do projeto
def fix_strong(title, c):
	newContent = []
	body = php_mask(c, True)
	soup = BeautifulSoup(body, "html.parser")
	paragraph = soup.find_all('p')

	# realiza os ajustes
	for p in paragraph:
		strong = p.findChildren("strong", recursive=True)
		for child in strong:
			pstrong = child.text.lower()
			if title.lower() not in pstrong:
				child.string = title.lower().strip()
	for elem in soup:
		newContent.append(elem)
	# string converter
	value = ''.join(str(e) for e in elem)

	# retorna os valores
	return value.strip()

Error = { 'Não foi possível ler o(s) arquivo(s)':[],'Não foi possível criar o arquivo':[],'Não foi possível realizar o ajustes no(s) arquivo(s)':[],'Não foi possível recuperar o título da página':[] }


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
				#del php_elements[:]
				# Após receber todos os valores com sucesso, realiza os ajustes e retira a máscara do código
				body = fix_strong(title, php_mask(html, True))
			except:
				Error['Não foi possível realizar o ajustes no(s) arquivo(s)'].append(f'=> {a}.php')
			else:
				# tudo certo, gera o arquivo
				#create(body, a)
				print(php_elements)
		
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