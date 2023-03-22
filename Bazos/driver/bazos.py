from datetime import timedelta, datetime, timezone
from aiohttp_proxy import ProxyConnector
from aiohttp import ClientSession
from pyuseragents import random
from config.config import PROXY
from bs4 import BeautifulSoup

class ParserBazosSK:

	def __init__(self, link, count_dataNewPost, min_price, max_price, view, items):

		self.PatchBlockPeople = "data/BlockPeople.txt"

		self.headers = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Encoding": "gzip, deflate, br",
			"Host": f"{link.split('/')[2]}",
			"User-Agent": random(),
			"Connection": "keep-alive"
			}

		self.headers_person = headers_person = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Host": "www.bazos.sk",
			"User-Agent": random(),
			"Accept-Encoding": "gzip, deflate, br",
			"Connection": "keep-alive"
			}

		self.link = link
		self.count_dataNewPost = count_dataNewPost
		self.filter_url = f"?hledat=&hlokalita=&humkreis=25&cenaod={min_price}&cenado={max_price}&order=?vkm=k"
		self.view = view
		self.items = items

		self.dateNow = datetime.now(tz=timezone(timedelta(hours=1)))

	async def Parser(self, session):
		dataNewPost,blockPeople,count = [],[],0
		datePaginator = f"{self.dateNow.day}.{self.dateNow.month}.{self.dateNow.year}"

		with open(self.PatchBlockPeople, 'r', encoding='utf-8') as file:
			blockPeople = [line.rstrip("\n") for line in file]

		while len(dataNewPost) < self.count_dataNewPost:

			async with session.get(f"{self.link}{count}/{self.filter_url}") as response:
				blocks = BeautifulSoup(await response.text(), "lxml").find_all("div", {"class": "inzeraty inzeratyflex"})
			
			for block in blocks:
				try:
					if not block.find("span", {"class": "ztop"}):
						if datePaginator in block.find("span", {"class": "velikost10"}).text.replace(" ", ""):
							if int(block.find("div", {"class":"inzeratyview"}).text[:-2]) <= self.view:
								linkPerson = block.find('div', {"class": 'inzeratyakce'}).find_all('a')[2].get('href')
								if linkPerson not in blockPeople:
									blockPeople+=[linkPerson]
									async with session.get(f"{linkPerson}&vkm=k", headers=self.headers_person) as responsePerson:
										itemsOnSale = int(BeautifulSoup(await responsePerson.text(), "lxml").findAll("div", {"class": "listainzerat inzeratyflex"})[-1].find("div",class_="inzeratynadpis").text.split("(")[-1][:-2])
										if itemsOnSale <= self.items:
											if len(dataNewPost) == self.count_dataNewPost:
												return dataNewPost

											else:
												link_poduct = f'{self.link[:-1]}{block.find("a").get("href")}'
												name_product = block.find("h2" ,{"class": "nadpis"}).get_text()
												price_product = int(block.find("div", {"class": "inzeratycena"}).b.text[:-1].replace(' ', ''))
												locate_product = ''.join([x for x in block.find("div", {"class": "inzeratylok"}).get_text() if not x.isdigit()]) 
												description_product = block.find("div", {"class": "popis"}).get_text()
												link_photo = block.find("div", {"class": "inzeratynadpis"}).find("img").get("src").replace("1t","1")
												number_person = f"{self.link}detailtel.php?idi={linkPerson.split('=')[1][:-8]}&idphone={linkPerson.split('=')[2][:-6]}"
												view_product = int(block.find("div", {"class":"inzeratyview"}).text[:-2])
												
												dataNewPost += [[name_product, datePaginator, price_product, locate_product, description_product, link_poduct, link_photo, linkPerson, itemsOnSale, view_product, number_person]]

												with open(self.PatchBlockPeople, 'a', encoding='utf-8') as file:
													file.write(linkPerson + "\n")
						else:
							return dataNewPost
				except:
					pass							
			count += 20
		return dataNewPost

	async def LogerParser(self):
		async with ClientSession(headers = self.headers, connector = ProxyConnector.from_url(f'{PROXY}')) as session:
			dataSourche = await self.Parser(session)
			return dataSourche
