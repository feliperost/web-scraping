import requests
from bs4 import BeautifulSoup
import pprint

# request da frontpage
res = requests.get('https://news.ycombinator.com/news') 
# request da segunda página
res2 = requests.get('https://news.ycombinator.com/news?p=2') 

# criação de um "soup object", que pega as informações do site e converte para hmtl
# o segredo é inspecionar o código do site que vc vai retirar a informação, para saber a terminologia a ser usada e unir ao que a library diz
soup = BeautifulSoup(res.text, 'html.parser') 
soup2 = BeautifulSoup(res2.text, 'html.parser')


# soup.select pega uma parte da data do site com base no termo em css 
# grabs all the elements tagged with storylink (os links das noticias)
# grabs all the subtext (barrinha embaixo da noticia)
links = soup.select('.storylink') 
subtext = soup.select('.subtext') 
links2 = soup2.select('.storylink') 
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtext = subtext + subtext2

# função necessária para realizar a ordenação dos links de acordo com uma chave de um dicionário
def sort_stories_by_votes(hnlist):
	return sorted(hnlist, key = lambda k:k['votes'], reverse=True) 


# utilizamos enumerate nessa função pq estamos loopando por 2 listas (links e subtext)
# em ordem: a função pega o titulo da noticia, o link da notícia, pega os elementos com a tag .score, e pega notícias com votos acima de 100
def create_custom_hn(links, subtext):
	hn = []
	for idx, item in enumerate(links): 
		title = links[idx].getText() 
		href = links[idx].get('href', None) 
		vote = subtext[idx].select('.score') 
		if len(vote): 
			points = int(vote[0].getText().replace(' points', ''))
			if points > 99: 
				hn.append({'title': title, 'link': href, 'votes': points}) 
	return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(links, subtext))
