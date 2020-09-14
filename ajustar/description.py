from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

session = HTMLSession()

# variáveis do projeto
projeto = 'nowbuck.com.br'
htdocs = f'C://xampp/htdocs/{projeto}/' # alterar para htdocs proprio

# Quando "True", 
# ignora os arquivos inseridos manualmente na lista, 
# e pega todas as mpis automaticamente
vAll = True

# inserir os arquivos para serem editados (sem .php)
f = [
	'armazenagem-graos-galpao',
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
	    Error['Não foi possível criar o arquivo'].append(f'=> {file}')

# faz o ajuste nos strongs do projeto
def fix_code(t, html, a):
	import re
	# armazenando elementos
	content = []
	try:

		# criando o soup em html
		soup = BeautifulSoup(mask(html, True), "html.parser")
		title = t.strip()

		# verifica se a description está realmente errada
		currentDesc = re.search(r"\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]", str(soup))
		# currentDesc.group(0)

		if currentDesc != None:

			math = currentDesc.group(0)
			if math.lower().find(title.lower()) >= 0:
				descfix = True

		if descfix:

			for p in soup.select('article'):

				# resgata o primeiro paragrafo do article
				child = p.find_all('p')

				# verifica a description
				for p in child:

					i = remove_accent(str(p)).lower().find(title.lower())

					if i >= 0:

						if len(str(p)) >= 125:
							desc = title + ' ' + str(p)[:].strip()
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

				else:
					Log['Não foi possível ajustar a description'].append(f'=> {a}')
		else:
			Log['Description atual está correta.'].append(f'=> {a}')

		# retorna novo código
		for elem in soup.prettify(formatter=None):
			content.append(elem)
		value = ''.join(map(str, content))

		# aplica a nova description
		if desc:
			value = re.sub(r"\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]", desc, value)

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
	for a in tqdm(f):

		r = session.get(url_replace(htdocs, a))
		# constroi o arquivo
		html = file_read(htdocs + a.strip())
		# retorna o title da pagina
		try:
			t = r.html.find('head title')
			for v in t:
				title = v.text.split('-')[0]
		except:
			Error['Não foi possível recuperar o título da página'].append(f'=> {url_replace(htdocs, a)}')
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