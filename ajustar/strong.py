from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

session = HTMLSession()

# variáveis do projeto
projeto = 'fastinox.com.br'
htdocs = f'C://xampp/htdocs/{projeto}/' # alterar para htdocs proprio

# Quando "True", 
# ignora os arquivos inseridos manualmente na lista, 
# e pega todas as mpis automaticamente
vAll = False

# inserir os arquivos para serem editados (sem .php)
f = [
	'instrumentos-cirurgicos-ribeirao-preto'
]

Error = { 'Não foi possível ler o(s) arquivo(s)':[],'Não foi possível criar o arquivo':[],'Não foi possível realizar o ajustes no(s) arquivo(s)':[],'Não foi possível recuperar o título da página':[], 'Não foi possível inserir strong no parágrafo do arquivo': [] }
Success = []

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
		Error['Não foi possível ler o(s) arquivo(s)'].append(f'=> {f}.php')

# montar url do temporario
def urlReplace(x, y):
	x = x.split('//')
	r = x[1].split('/')
	if y:
		return 'http://mpitemporario.com.br/projetos/' + r[2] + '/' + y
	else:
		return 'http://mpitemporario.com.br/projetos/' + r[2] + '/'

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

		for p in soup.select('article > p'):

			child = p.find_all('strong')

			# verifica se o paragrafo tem strong
			if child:
				for strong in child:
					# ajusta quais não estão corretas
					if title.lower() != strong.string.lower():
						strong.string = title.lower()
			else:

				try:
					if removeAccent(title).lower() in removeAccent(p.string).lower().strip():
						r = p.string.lower().replace(title.lower().strip(), '<strong>'+title.lower()+'</strong>')
						p.string = r
				except:
					Error['Não foi possível inserir strong no parágrafo do arquivo'].append(f'\n=> {a}')
				

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
if vAll:
	del f[:]
	get_mpis(urlReplace(htdocs, False))
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
					print(Fore, RED)
					print('Falha na execução do strong.')

			except:
				Error['Não foi possível realizar o ajustes no(s) arquivo(s)'].append(f'=> {a}.php')

			del elements[:]
		
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
    	print(f'Ajustes realizados com sucesso em ({len(Success)}) projetos.')	
    	break

print(Style.RESET_ALL)

input('\nFinalizado. Aperte "ENTER" para encerrar o programa.')