from bs4 import BeautifulSoup, Comment
from tqdm.auto import tqdm
from requests_html import HTMLSession
from colorama import Fore, Style

session = HTMLSession()

# variáveis do projeto
projeto = 'fluxoambiental.com.br'
htdocs = f'C://xampp/htdocs/{projeto}/' # alterar para htdocs proprio

# inserir os arquivos para serem editados (sem .php)
f = [
	'aproveitamento-agua-chuva-preco',
	'custo-ete-compacta',
	# 'empresa-aproveitamento-agua-chuva',
	# 'empresa-estacao-tratamento-agua',
	# 'empresa-ete',
	# 'estacao-compacta-tratamento-efluentes-sanitarios',
	# 'estacao-tratamento-biologico-efluentes-sanitarios-industriais',
	# 'estacao-tratamento-agua',
	# 'estacao-tratamento-agua-cinza',
	# 'estacao-tratamento-agua-compacta',
	# 'estacao-tratamento-agua-chuva',
	# 'estacao-tratamento-agua-reuso',
	# 'estacao-tratamento-agua-esgoto',
	# 'estacao-tratamento-agua-eta-compacta',
	# 'estacao-tratamento-agua-industrial',
	# 'estacao-tratamento-agua-escola',
	# 'estacao-tratamento-agua-abastecimento',
	# 'estacao-tratamento-aguas-residuais-industriais',
	# 'estacao-tratamento-efluentes-sanitarios',
	# 'estacao-tratamento-esgoto',
	# 'estacao-tratamento-esgoto-compacta',
	# 'estacao-tratamento-esgoto-compacta-preco',
	# 'estacao-tratamento-esgoto-comprar',
	# 'estacao-tratamento-esgoto-convencional',
	# 'estacao-tratamento-esgoto-domiciliar',
	# 'estacao-tratamento-esgoto-condominios',
	# 'estacao-tratamento-esgoto-individual',
	# 'estacao-tratamento-esgoto-preco',
	# 'estacao-tratamento-esgoto-projeto',
	# 'estacao-tratamento-esgoto-residencial',
	# 'eta-compacta-modular',
	# 'eta-compacta-preco',
	# 'eta-convencional-compacta',
	# 'eta-estacao-tratamento-da-agua',
	# 'ete-compacta-fibra',
	# 'ete-compacta-fabricante',
	# 'ete-compacta-industrial',
	# 'ete-compacta-modular',
	# 'ete-compacta-preco',
	# 'ete-compacta-valor',
	# 'ete-estacao-tratamento-efluentes',
	# 'ete-estacao-tratamento-esgoto',
	# 'ete-estacao-tratamento-esgoto-compacta',
	# 'fabricantes-ete-compacta',
	# 'preco-ete-compacta',
	# 'reuso-aguas-cinzas-edificacoes',
	# 'reuso-aguas-cinzas-irrigacao',
	# 'sistema-esgoto-condominial',
	# 'sistema-esgoto-condominial-convencional',
	# 'sistema-tratamento-efluentes-sanitarios',
	# 'sistemas-simples-tratamento-esgotos-sanitarios',
	# 'tratamento-biologico-efluentes',
	# 'tratamento-biologico-efluentes-domesticos',
	# 'tratamento-efluente-sanitario-areas-rurais',
	# 'tratamento-efluentes-fisico-quimico-biologico',
	# 'tratamento-efluentes-hospitalares',
]

Error = { 'Não foi possível ler o(s) arquivo(s)':[],'Não foi possível criar o arquivo':[],'Não foi possível realizar o ajustes no(s) arquivo(s)':[],'Não foi possível recuperar o título da página':[], 'Não foi possível inserir strong no parágrafo do arquivo': [] }

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
			mask = re.sub(msk, remove, soup.prettify())
		else:
			mask = re.sub(msk, add, soup.prettify())
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
		with open(f'./projetos/{arquivo}' + '.php', 'a', encoding='utf8') as f:
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
				
				# se nao tiver, localiza onde deveria e insere
				if p.string.count(title.upper()) > 0:
					r = p.string.replace(title.upper(), '<strong>'+title.lower()+'</strong>')
					p.string = r

				elif p.string.count(title.capitalize()) > 0:
					r = p.string.replace(title.capitalize(), '<strong>'+title.lower()+'</strong>')
					p.string = r

				elif p.string.count(title.lower()) > 0:
					r = p.string.replace(title.lower(), '<strong>'+title.lower()+'</strong>')
					p.string = r

				elif p.string.count(title.title()) > 0:
					r = p.string.replace(title.title(), '<strong>'+title.lower()+'</strong>')
					p.string = r
				else:
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
    	print('Ajustes realizados com sucesso!')	
    	break

print(Style.RESET_ALL)

input('\nFinalizado. Aperte "ENTER" para encerrar o programa.')