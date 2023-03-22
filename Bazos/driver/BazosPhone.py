from aiohttp_proxy import ProxyConnector
from aiohttp import ClientSession
from pyuseragents import random
from config.config import PROXY
from bs4 import BeautifulSoup

class BazosSkPhone:

	def __init__(self, token, link_phone):
		self.headers = {
			'Accept': '*/*',
			'Host': link_phone.split("/")[2],
			'User-Agent': random(),
			'Connection': 'keep-alive',
			}

		self.cookies = {
			'testcookie': 'ano',
			'bkod': f"{token}",
			'rek': 'ano',
			'vkm': 'k'
			}

		self.link_phone = link_phone


	async def ParserPhone(self, session):
		params = {
			"idi": f"{self.link_phone.split('=')[-2].split('&')[0]}",
			"idphone": f"{self.link_phone.split('=')[-1]}"
			}

		async with session.get(self.link_phone, params=params) as response:

			try:
				number = BeautifulSoup(await response.text(), "lxml").find("a", {"class": "teldetail"}).text
			except:
				number = "bkod not valid"

			return number


	async def LoggerParserPhone(self):
		async with ClientSession(headers = self.headers, cookies=self.cookies, connector=ProxyConnector.from_url(f'{PROXY}')) as session:
			number = await self.ParserPhone(session)
			return number
