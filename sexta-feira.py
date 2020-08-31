# Importante
# 30 de Ago de 2020
# =>
# Essa versão não faz uso do "selenium", portanto não verifica o scroll nos projetos

from socket import error as socket_error
from tqdm.auto import tqdm
from datetime import datetime
from colorama import Fore, Style
from requests_html import HTMLSession

session = HTMLSession()

# variaveis data
date_current = datetime.now()
date = date_current.strftime('%d/%m/%Y %H:%M:%S')

errosEncontrado = {
    'W3C':[],
    'Description com números de caracteres incorretos':[],
    'Pagina com mais de um H1':[],
    'O H1 não foi encontrado na description':[],
    'Links não encontrados do Mapa no site': [],
    'Menu':[], 
    'PageSpeed':[],
    'ALT/TITLE':[],
    'Scroll':[],
    'Links duplicados na coluna lateral':[],
    'Imagens quebradas':[],
    'H2 iguais a H1':[],
    'H2 duplicado':[],
    'Parágrafos duplicados':[],
    'A descrição não mencionou H1':[],
    'MPI sem strong':[],
    'H2 com strong':[],
    'Elementos vazios na pagina':[],
    'MPI sem imagens':[],
    'MPI sem H2':[],
    'H2 não foi mencionado em H1':[],
    'Alterar tag P para UL>li':[],
    'Sequência de UL':[],
    'Sequência de H2':[],
    'Description atual não foi encontrada no texto MPI':[],
    'Palavra chave sem Strong':[]
    }

erroValidacao = {
    'Função de validação do W3C':[],
    'Função de validação description e H1':[],
    'Função de validação Menu header e menu footer':[],
    'Função de validação PageSpeed':[],
    'Função de validação Scroll Horizontal':[],
    'Função de validação ColunaLateral':[],
    'Função de validação VerificaImagem':[],
    'Função de validação de MPI':[],
    'Erro ao realizar validação':[]
}


def getUrls():
    with open("sites.txt", "r+") as sites:

        #define variáveis
        arrayUrl = []
        linha = sites.readlines()

        #escreve inicializador
        print(Fore.YELLOW)
        print('┌──────────────────────────────────────────────────┐')
        print('│                   GUIA DE USO                    │')
        print('└──────────────────────────────────────────────────┘')
        print('│                                                  │')
        print('│                                                  │')
        print('│ - Dica: Insira as URL\'s no arquivo "sites.txt"   │')
        print('│                                                  │')
        print('│ - Insira as URL\'s dos projetos para validação    │')
        print('│                                                  │')
        print('│ Exemplo: [url], [url], [url] [...]               │')
        print('│                                                  │')
        print('│                                                  │')
        print('└──────────────────────────────────────────────────┘')
        print(Fore.WHITE)
        getUrl = str(input('\nPor favor informe as URL\'s separando-as por vírgula:\n> '))
        getUrl = getUrl.split(",")
        if len(getUrl) > 0:
            for appendUrl in getUrl:
                sites.write(appendUrl+'\n')
            for url in linha:
                arrayUrl.append(url.strip("\n").strip(" ").strip(","))
        else:
            arrayUrl.append(getUrl)
    return arrayUrl

# Função para limpar a URL
def urlBase(limpaUrl):
    try:
        limpaUrl = limpaUrl.split('//')
        limpaUrl = limpaUrl[1].split('/')
    except:
        print(Fore.RED)
        print(f'Não foi possível limpar a URL do projeto especificado.', Style.RESET_ALL)
        return False
    else:
        return limpaUrl[0]

# Função para retornar a URL do projeto no mpitemporario ex: http://mpitemporario.com.br/projetos/tse.com.br/ === tse.com.br
def urlProjetoMpitemporario(limpaUrl):
    limpaUrl = limpaUrl.split('//')
    limpaUrl = limpaUrl[1].split('/')
    limpaUrl = [x for x in limpaUrl if x]
    return limpaUrl[-1]

# Função para validar URL
def ValidaUrl(url):
    if '?' not in url and '#' not in url and '.jpg' not in url and '.jpeg' not in url and '.png' not in url and '.png' not in url and '.pdf' not in url and 'tel:' not in url and 'mailto:' not in url:
        return True
    else:
        return False


# Função para pegar todas as URLs do site
def PegaLinksDoSite(UrlSite):

    try:
        r = session.get(UrlSite)
        linksDaPagina = r.html.xpath('//a[not(@rel="nofollow")]/@href')
        links = []
        linksConfirmados = {'Todos':[UrlSite], 'Mapa Site':[], 'MPI':[]}
        def Recursividade(linksPrimeiraPagina):
            for link in linksPrimeiraPagina:
                if root in link:
                    if ValidaUrl(link):
                        links.append(link)
            for link in links:
                if link not in linksConfirmados['Todos']:
                    linksConfirmados['Todos'].append(link)
                    r = session.get(link)
                    pageLinks = r.html.absolute_links
                    Recursividade(pageLinks)
        
        Recursividade(linksDaPagina)

    except:
        print(Fore.RED)
        print(f'- Não foi possível validar a URL do projeto =>\n {UrlSite}', Style.RESET_ALL)
        return False
    else:
        rm = session.get(UrlSite + '/mapa-site')
        sitemapElements = rm.html.find('.sitemap li a')
        for linkMapaDoSite in sitemapElements:
            linksConfirmados['Mapa Site'].append(linkMapaDoSite.attrs['href'])
        try:
            subMenuInfo = rm.html.find('.sitemap ul.sub-menu-info li a')
        except:
            print('Não foi possível localizar as MPI\'s do projeto.')
            linksConfirmados['MPI'].append('Nulo')
        else:
            for linkMPI in subMenuInfo:
                linksConfirmados['MPI'].append(linkMPI.attrs['href'])
    try:        
        return linksConfirmados
    except:
        print(Fore.RED)
        print(f'Não foi possível realizar o rastreamento de links do projeto\n=> {UrlSite}')

# Função para validar o W3C da pagina.
def VerificaW3C(pagina):


    w3cLink = f"https://validator.w3.org/nu/?doc={pagina}"  
    try:
        r = session.get(w3cLink)
        erros = r.html.find('#results strong')
        if erros:
            errosEncontrado['W3C'].append(f'=> {pagina}')   
    except:
        erroValidacao['Função de validação do W3C'].append(f'=> {pagina}')


# Função para validar a description e  H1 da pagina
def VerificaDescriptionH1(pagina, r):


    try:
        description = r.html.find('head meta[name="description"]', first=True).attrs['content']
        h1 = r.html.find('h1')

    except:
        erroValidacao['Função de validação description e H1'].append(f'=> {pagina}')

    else:
        if len(description) > 160 or len(description) < 140:
            errosEncontrado['Description com números de caracteres incorretos'].append(f'=> {pagina}')
            
        if(len(h1) > 1):
            errosEncontrado['Pagina com mais de um H1'].append(f'=> {pagina}')
        h1 = h1[0].text

        if h1.lower() not in description.lower() and pagina != url:
            errosEncontrado['O H1 não foi encontrado na description'].append(f'=> {pagina}')


# Função para verificar se a página está no Mapa do site
def VerificaMapaDoSite(pagina):
    if pagina not in listaDeLinks['Mapa Site'] and '/mapa-site' not in pagina:
        errosEncontrado['Links não encontrados do Mapa no site'].append(f'=> {pagina}')


#Função para validar Menu header e menu footer
def VerificaMenuHeaderFooter(pagina, r):


    try:
        menuTopTexts = r.html.xpath('//header//nav/ul/li/a/text()')
        menuFooterTexts = r.html.xpath('//footer//nav/ul/li/a/text()')
        menuTopTexts.append('Mapa do site'.lower())

        menuTopLinks = r.html.xpath('//header//nav/ul/li/a/@href')
        menuFooterLinks = r.html.xpath('//footer//nav/ul/li/a/@href')
        menuTopLinks.append(url + 'mapa-site')

    except:
        erroValidacao['Função de validação menu header e menu footer'].append(f'=> {pagina}')

    else: 
        menuTopTexts = [item.lower() for item in menuTopTexts]
        menuFooterTexts = [item.lower() for item in menuFooterTexts]

        if False in [True if i == j else False for i,j in zip(menuTopTexts, menuFooterTexts)]:
            errosEncontrado['Menu'].append('=> Menu footer diferente do menu header') 

        if False in [True if i == j else False for i,j in zip(menuTopLinks, menuFooterLinks)]:
            errosEncontrado['Menu'].append('=> Links do menu footer diferente do menu header')


# Função para validar PageSpeed da home e 3 MPI(aleatoria)
def PageSpeed(link):

    #import
    import random
    import json
    from requests_html import HTMLSession
    session = HTMLSession()

    try:
        pagespeedUrls = [link]

        while len(pagespeedUrls) != 4:
            paginaMPI = random.choice(listaDeLinks['MPI'])
            if paginaMPI not in pagespeedUrls:
                pagespeedUrls.append(paginaMPI)
        
        apiKey = 'AIzaSyDFsGExCkww5IFLzG1aAnfSovxSN-IeHE0'
        
        def AjusteLinkPageSpeed(link):
            link = link.replace(':', '%3A')
            link = link.replace('/', '%2F')
            return link

    except:
        erroValidacao['Função de validação PageSpeed'].append(f'=> função não foi executada')

    else:
        for pagespeedUrl in pagespeedUrls:
            try:
                mobileUrl = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={AjusteLinkPageSpeed(pagespeedUrl)}&category=performance&locale=pt_BR&strategy=mobile&key={apiKey}'
                desktopUrl = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={AjusteLinkPageSpeed(pagespeedUrl)}&category=performance&locale=pt_BR&strategy=desktop&key={apiKey}'

                mobileRequest = session.get(mobileUrl)
                jsonDataM = json.loads(mobileRequest.text)
                desktopRequest = session.get(desktopUrl)
                jsonDataD = json.loads(desktopRequest.text)
            
            except:
                erroValidacao['Função de validação PageSpeed'].append(f'=> {pagespeedUrl}')
            
            else:
                mobileScore = int(float(jsonDataM['lighthouseResult']['categories']['performance']['score']) * 100)
                if mobileScore < 90:
                    errosEncontrado['PageSpeed'].append(f'Mobile - {mobileScore}')

                desktopScore = int(float(jsonDataD['lighthouseResult']['categories']['performance']['score']) * 100)
                if desktopScore < 90:
                    errosEncontrado['PageSpeed'].append(f'Desktop - {desktopScore}')


# Função para validar ALT e TITLE
def VerificaAltTitle(pagina, r):


    def hrefSrc(link):
        try:
            return link.split(url.split('//')[-1])[-1]
        except:
            return link

    todasImagens = r.html.find('body img')
    for imagem in todasImagens:
        try:
            if imagem.attrs['alt']:
                if 'escrev' in imagem.attrs['alt'].lower():
                    errosEncontrado['ALT/TITLE'].append(f"=> {pagina} - src='{hrefSrc(imagem.attrs['src'])}' ALT com 'ESCREVA AQUI'")

                elif 'exemplo de mpi' in imagem.attrs['alt'].lower():
                    errosEncontrado['ALT/TITLE'].append(f"=> {pagina} - src='{hrefSrc(imagem.attrs['src'])}' ALT com 'Exemplo de MPI'")
        except:
            errosEncontrado['ALT/TITLE'].append(f"=> {pagina} - src='{hrefSrc(imagem.attrs['src'])}' Imagem sem ALT")

        try:    
            if imagem.attrs['title']:
                if 'escrev' in imagem.attrs['title'].lower():
                    errosEncontrado['ALT/TITLE'].append(f"=> {pagina} - src='{hrefSrc(imagem.attrs['src'])}' com TITLE 'ESCREVA AQUI'")

                elif 'exemplo de mpi' in imagem.attrs['title'].lower():
                    errosEncontrado['ALT/TITLE'].append(f"=> {pagina} - src='{hrefSrc(imagem.attrs['src'])}' com TITLE 'Exemplo de MPI'")
        except:
            errosEncontrado['ALT/TITLE'].append(f"=> {pagina} - src='{hrefSrc(imagem.attrs['src'])}' - Imagem sem TITLE")


    todasLinks = r.html.find('body a[href*="http"]')
    for link in todasLinks:
        try:
            if link.attrs['title']:
                if 'escrev' in link.attrs['title'].lower():
                    errosEncontrado['ALT/TITLE'].append(f"=> {pagina} - Link href='/{hrefSrc(link.attrs['href'])}' com TITLE 'ESCREVA AQUI'")

                elif 'exemplo de mpi' in link.attrs['title'].lower():
                    errosEncontrado['ALT/TITLE'].append(f"=> {pagina} - Link href='/{hrefSrc(link.attrs['href'])}' com TITLE 'Exemplo de MPI'")

        except:
            errosEncontrado['ALT/TITLE'].append(f"=>  {pagina} - href='{link.attrs['href']}' Link sem TITLE")

    
#Função para verificar links duplicados na coluna lateral
def VerificaColunaLateral(pagina, r):
    from collections import defaultdict
    if r.html.find('aside'):
        try:
            asideLinks = r.html.xpath("//html//body//main//aside//nav//a/@href")
            keys = defaultdict(list)
            for key, value in enumerate(asideLinks):
                keys[value].append(key)

            for value in keys:
                if len(keys[value]) > 1 and f'=> {value}' not in errosEncontrado['Links duplicados na coluna lateral']:
                    errosEncontrado['Links duplicados na coluna lateral'].append(f'=> {value}')
        
        except:
            erroValidacao['Função de validação ColunaLateral'].append(f'=> {pagina}')

                
#Função para validar imagens             
def VerificaImagem(pagina, r):


    try:
        imagens = r.html.xpath('//body//img/@src')
        for imagem in imagens:    
            if str(session.head(imagem).status_code) != "200":
                errosEncontrado['Imagens quebradas'].append(f'=> {pagina}: {imagem}')
    except:
        erroValidacao['Função de validação VerificaImagem'].append(f'=> {pagina}')


def VerificaMPI(pagina, r):


    try:
        description = r.html.find('head meta[name="description"]', first=True).attrs['content']
        images = len(r.html.find('article ul.gallery img'))
        h1 = r.html.find('h1')
        h2 = r.html.find('article h2')
        articleElements = r.html.find('article h2, article p')
        strongsInArticle = r.html.find('article p strong')
        titleWithStrong = r.html.find('article h2 strong')
        allParagraphs = r.html.xpath('//article/p[not(@class)]')

    except:
        erroValidacao['Função de validação de MPI'].append(f'=> {pagina}')

    else:
        h1 = h1[0].text

        h2HasH1 = False
        for uniqueH2 in h2:
            if h1 in uniqueH2.text:
                h2HasH1 = True
                break

        h2List = []
        h1EqualsH2 = False
        for title in h2:
            h2List.append(title.text)
            if title.text.lower() == h1.lower() and not h1EqualsH2:
                errosEncontrado['H2 iguais a H1'].append(f'=> {pagina}')
                h1EqualsH2 = True

        if len(h2List) != len(set(h2List)):
            errosEncontrado['H2 duplicado'].append(f'=> {pagina}')

        pAllList = []
        for paragraph in allParagraphs:
            pAllList.append(paragraph.text)

        if len(pAllList) != len(set(pAllList)):
            errosEncontrado['Parágrafos duplicados'].append(f'=> {pagina}')

        emptyElements = []
        for emptyElement in articleElements:
            if len(emptyElement.text) < 6:
                emptyElements.append(emptyElement)

        fakeTitles = r.html.find('article p')
        pUpper = []
        for fakeTitle in fakeTitles:
            if fakeTitle.text.isupper():
                pUpper.append(fakeTitle)
                                
        sequentialList = r.html.find('article ul + ul')
        sequentialTitle = r.html.find('article h2 + h2')

        descriptionNoTexto = 0
        pListErroCont = 0
        msmString = []
        for p in allParagraphs:
            descriptionErro = False if description.replace("  ", " ")[:-35].lower() in p.text.lower() else True
            if not descriptionErro:
                descriptionNoTexto += 1

            try:
                pListErro = False if p.text[:-1] != ";" else True
                if pListErro:
                    pListErroCont += 1
            except:
                erroValidacao['Função de validação de MPI'].append(f'=> {pagina}')

            if len(strongsInArticle) > 3:
                strong = True if p.find('strong') else False
                h1InP = True if h1.lower() in p.text.lower() else False
                if strong != h1InP:
                    msmString.append(f"{allParagraphs.index(p) + 1}°")

        
        if h1.lower() not in description.lower() : 
            errosEncontrado['A descrição não mencionou H1'].append(f'=> {pagina}')

        if len(strongsInArticle) < 3:
            errosEncontrado['MPI sem strong'].append(f'=> {pagina}')

        if len(titleWithStrong) > 0:
            errosEncontrado['H2 com strong'].append(f'=> {pagina}')

        if len(msmString) > 0:
            errosEncontrado['Palavra chave sem Strong'].append("=> " + pagina + " - " + ", ".join(msmString) + ' parágrafo sem strong')

        if len(emptyElements) > 0:
            errosEncontrado['Elementos vazios na pagina'].append(f'=> {pagina}')

        if images < 1 :
            errosEncontrado['MPI sem imagens'].append(f'=> {pagina}')

        if len(h2) < 2 :
            errosEncontrado['MPI sem H2'].append(f'=> {pagina}')

        if not h2HasH1:
            errosEncontrado['H2 não foi mencionado em H1'].append(f'=> {pagina}')

        if pListErroCont > 0 :
            errosEncontrado['Alterar tag P para UL>li'].append(f'=> {pagina}')

        if len(sequentialList) > 0 :
            errosEncontrado['Sequência de UL'].append(f'=> {pagina}')

        if len(sequentialTitle) > 0 :
            errosEncontrado['Sequência de H2'].append(f'=> {pagina}')

        if descriptionNoTexto == 0:
            errosEncontrado['Description atual não foi encontrada no texto MPI'].append(f'=> {pagina}')

# gerar as listas
def generateError(url, status):

    import os.path

    log = False
    for erro in erroValidacao.keys():
        if len(erroValidacao[erro]) > 0:
            log = True
            break

    def writeProjects(url, status):
        # abre arquivo e escreve
        with open(f"projetos/{status}-{url}.txt", "a", -1, "utf-8") as arquivo:

            for errosItens in errosEncontrado.keys():
                if len(errosEncontrado[errosItens]) > 0:
                    arquivo.write(f'{errosItens}: \n')
                    for errosValores in errosEncontrado[errosItens]:
                        arquivo.write(f'{errosValores} \n')
                    arquivo.write('\n')
            if log:
                arquivo.write('Funções não executadas nas URL\n=> {}\n'.format(url))
                for errosItensValidacao in erroValidacao.keys():
                    if len(erroValidacao[errosItensValidacao]) > 0:
                        arquivo.write(f'{errosItensValidacao}: \n')

                        for errosValores in erroValidacao[errosItensValidacao]:
                            arquivo.write(f'{errosValores} \n')

                        arquivo.write('\n')

    def writeNot(url):
        if len(erroValidacao['Erro ao realizar validação']) > 0:
            with open(f'projetos/1-lista-nao-validados.txt', 'a', -1, 'utf-8') as arquivo:
                arquivo.write('[{}] \n=> {}\n'.format(date, url))
    
    if status:

        # verifica se existe pasta projetos
        if not os.path.exists('projetos'):
            try:
                os.makedirs('projetos')
                writeProjects(url, status)
            except OSError:
                print(Fore.RED)
                print('Não foi possível gerar lista de erros do projeto\n=> {}'.format(url), Style.RESET_ALL)
        else:
            writeProjects(url, status)
    else:
    # gera novo arquivo dos sites não validados 
        if not os.path.exists('projetos'):
            try:
                os.makedirs('projetos')
                writeNot(url)
            except OSError:
                print(Fore.RED)
                print('Não foi possível gerar lista de erros do projeto\n=> {}'.format(url), Style.RESET_ALL)
        else: 
            writeNot(url)

# Função para pegar todas as Urls que estão dentro do arquivo sites.txt
def Urls():      
    with open("sites.txt", "r+") as sites:
        arrayUrl = []
        linha = sites.readlines()
        if len(linha) > 0:
            for url in linha:
                arrayUrl.append(url.strip("\n").strip(" ").strip(","))
        else:
            arrayUrl = False
    return arrayUrl

urls = Urls()

try:
    for url in urls:
        root = urlBase(url)
        if root != False:
            print(Fore.YELLOW)
            print('=> {}'.format(url))
            print(Fore.GREEN)
            print('Rastreando e categorizando os links... Aguarde\n', Style.RESET_ALL)

            listaDeLinks = PegaLinksDoSite(url)

            if listaDeLinks != False:
                print(Fore.YELLOW)
                print('- Iniciando validações...\n', Style.RESET_ALL)
                try:
                    for pagina in tqdm(listaDeLinks['Todos']):

                        r = session.get(pagina)

                        VerificaW3C(pagina)
                        VerificaDescriptionH1(pagina, r)
                        VerificaAltTitle(pagina, r)
                        VerificaMapaDoSite(pagina)
                        VerificaImagem(pagina, r)


                        if pagina == url:
                            VerificaMenuHeaderFooter(pagina, r)
                            PageSpeed(pagina)

                        if pagina in listaDeLinks['Mapa Site']:
                            VerificaColunaLateral(pagina, r)

                        if pagina in listaDeLinks['MPI']: 
                            VerificaMPI(pagina, r)

                except:
                    print(Fore.RED)
                    print('Não foi possível realizar a validação do projeto\n=> {}'.format(url), Style.RESET_ALL)
                    erroValidacao['Erro ao realizar validação'].append(f'=> {url}')
                    if len(errosEncontrado) > 0: 
                        generateError(urlProjetoMpitemporario(url), 'ERRO')    
                    else:
                        generateError(urlProjetoMpitemporario(url), False)    
                else:

                    print(Fore.YELLOW)   

                    countErrors = 0
                    if len(errosEncontrado['W3C']) > 0:
                        print('- Erro(s) de W3C\n=> ( {} )'.format(len(errosEncontrado['W3C'])))
                        countErrors += len(errosEncontrado['W3C'])

                    if len(errosEncontrado['Description com números de caracteres incorretos']) > 0:    
                        print('- Description com números de caracteres incorretos\n=> ( {} )'.format(len(errosEncontrado['Description com números de caracteres incorretos'])))
                        countErrors += len(errosEncontrado['Description com números de caracteres incorretos'])

                    if len(errosEncontrado['Pagina com mais de um H1']) > 0: 
                        print('- Paginas com mais de um H1\n=> ( {} )'.format(len(errosEncontrado['Pagina com mais de um H1'])))
                        countErrors += len(errosEncontrado['Pagina com mais de um H1'])

                    if len(errosEncontrado['O H1 não foi encontrado na description']) > 0: 
                        print('- H1 não encontrado na description\n=> ( {} )'.format(len(errosEncontrado['O H1 não foi encontrado na description'])))
                        countErrors += len(errosEncontrado['O H1 não foi encontrado na description'])

                    if len(errosEncontrado['H2 iguais a H1']) > 0: 
                        print('- H2 iguais a H1\n=> ( {} )'.format(len(errosEncontrado['H2 iguais a H1'])))
                        countErrors += len(errosEncontrado['H2 iguais a H1'])

                    if len(errosEncontrado['H2 duplicado']) > 0: 
                        print('- H2 duplicados em MPI\n=> ( {} )'.format(len(errosEncontrado['H2 duplicado'])))
                        countErrors += len(errosEncontrado['H2 duplicado'])

                    if len(errosEncontrado['Parágrafos duplicados']) > 0: 
                        print('- Parágrafoss duplicados em MPI\n=> ( {} )'.format(len(errosEncontrado['Parágrafos duplicados'])))
                        countErrors += len(errosEncontrado['Parágrafos duplicados'])

                    if len(errosEncontrado['A descrição não mencionou H1']) > 0: 
                        print('- Descriptions sem H1 mencionado\n=> ( {} )'.format(len(errosEncontrado['A descrição não mencionou H1'])))
                        countErrors += len(errosEncontrado['A descrição não mencionou H1'])

                    if len(errosEncontrado['MPI sem strong']) > 0: 
                        print('- MPI sem strong no article\n=> ( {} )'.format(len(errosEncontrado['MPI sem strong'])))
                        countErrors += len(errosEncontrado['MPI sem strong'])

                    if len(errosEncontrado['H2 com strong']) > 0: 
                        print('- H2 de MPIs com strong\n=> ( {} )'.format(len(errosEncontrado['H2 com strong'])))
                        countErrors += len(errosEncontrado['H2 com strong'])

                    if len(errosEncontrado['Palavra chave sem Strong']) > 0: 
                        print('- Palavra chave sem strong no article\n=> ( {} )'.format(len(errosEncontrado['Palavra chave sem Strong'])))
                        countErrors += len(errosEncontrado['Palavra chave sem Strong'])

                    if len(errosEncontrado['Elementos vazios na pagina']) > 0: 
                        print('- Quantidade de paginas com elementos vazios\n=> ( {} )'.format(len(errosEncontrado['Elementos vazios na pagina'])))
                        countErrors += len(errosEncontrado['Elementos vazios na pagina'])

                    if len(errosEncontrado['MPI sem imagens']) > 0: 
                        print('- MPIs sem imagems na gallery\n=> ( {} )'.format(len(errosEncontrado['MPI sem imagens'])))
                        countErrors += len(errosEncontrado['MPI sem imagens'])

                    if len(errosEncontrado['MPI sem H2']) > 0: 
                        print('- MPIs sem H2 no article\n=> ( {} )'.format(len(errosEncontrado['MPI sem H2'])))
                        countErrors += len(errosEncontrado['MPI sem H2'])

                    if len(errosEncontrado['H2 não foi mencionado em H1']) > 0: 
                        print('- H2 não mencionado no H1\n=> ( {} )'.format(len(errosEncontrado['H2 não foi mencionado em H1'])))
                        countErrors += len(errosEncontrado['H2 não foi mencionado em H1'])

                    if len(errosEncontrado['Alterar tag P para UL>li']) > 0: 
                        print('- Alterar tag P para UL > LI\n=> ( {} )'.format(len(errosEncontrado['Alterar tag P para UL>li'])))
                        countErrors += len(errosEncontrado['Alterar tag P para UL>li'])

                    if len(errosEncontrado['Sequência de UL']) > 0: 
                        print('- Sequências de UL\n=> ( {} )'.format(len(errosEncontrado['Sequência de UL'])))
                        countErrors += len(errosEncontrado['Sequência de UL'])

                    if len(errosEncontrado['Sequência de H2']) > 0: 
                        print('- Sequências de H2\n=> ( {} )'.format(len(errosEncontrado['Sequência de H2'])))
                        countErrors += len(errosEncontrado['Sequência de H2'])

                    if len(errosEncontrado['Description atual não foi encontrada no texto MPI']) > 0: 
                        print('- Description atual não encontrada na MPI\n=> ( {} )'.format(len(errosEncontrado['Description atual não foi encontrada no texto MPI'])))
                        countErrors += len(errosEncontrado['Description atual não foi encontrada no texto MPI'])

                    if len(errosEncontrado['ALT/TITLE']) > 0: 
                        print('- ALT/TITLE\n=> ( {} )'.format(len(errosEncontrado['ALT/TITLE'])))
                        countErrors += len(errosEncontrado['ALT/TITLE'])

                    if len(errosEncontrado['Links duplicados na coluna lateral']) > 0: 
                        print('- Links duplicados na coluna lateral\n=> ( {} )'.format(len(errosEncontrado['Links duplicados na coluna lateral'])))
                        countErrors += len(errosEncontrado['Links duplicados na coluna lateral'])

                    if len(errosEncontrado['Imagens quebradas']) > 0: 
                        print('- Número de imagens quebradas\n=> ( {} )'.format(len(errosEncontrado['Imagens quebradas'])))
                        countErrors += len(errosEncontrado['Imagens quebradas'])

                    if len(errosEncontrado['Menu']) > 0: 
                        print('- Menu diferente do menu footer')
                        countErrors += len(errosEncontrado['Menu'])

                    # PageSpeed LOG
                    if len(errosEncontrado['PageSpeed']) > 0: 
                        print('\n- Notas de PageSpeed baixas\n')
                        for i, elem in enumerate(errosEncontrado['PageSpeed']):
                            print('=> '+elem)
                            if i == 2:
                                print('MPI\n')
                        print(Style.RESET_ALL)

                    if countErrors == 0:
                        print(Fore.GREEN)
                        print('Status: Aprovado de 1º', Style.RESET_ALL)

                    if countErrors <= 35:
                        print(Fore.YELLOW)
                        print('Status: MODERADO', Style.RESET_ALL)
                        nvl = 'MODERADO'
                    else:
                        print(Fore.RED)
                        print('Status: CRÍTICO', Style.RESET_ALL)
                        nvl = 'CRÍTICO'

                    # gera a lista antes de tudo
                    generateError(urlProjetoMpitemporario(url), nvl)

                    # Limpa memória
                    for values in errosEncontrado:
                        del errosEncontrado[values][:]

                    for values in erroValidacao:
                        del erroValidacao[values][:]

                    print(Fore.GREEN)
                    print('\nValidação do projeto finalizada com sucesso!\n=> {}'.format(url), Style.RESET_ALL)
except:
    getUrls()
# mensagem final 
input('\nA validação dos projetos foi finalizada. Aperte a tecla "ENTER" para encerrar\n')