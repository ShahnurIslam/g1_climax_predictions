import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession, AsyncHTMLSession
import pandas as pd
import asyncio
import aiohttp
asession = AsyncHTMLSession()

url = 'https://www.cagematch.net/?id=2&nr=4324&view=&page=4&constellationType=Singles&worker=&promotion=7'
session = HTMLSession()

async def get_match():
    r = await asession.get(url,stream=True,headers={'Accept-Encoding': 'identity'})
    # content = r.raw.read()
    # soup = BeautifulSoup(content, 'html.parser')
    # sel = "body > div:nth-child(3) > div.LayoutOptionsAndBody > div.LayoutBody > div > div.Table > div.TableContents > table"
    # table = soup.select_one(sel)
    # print(table)
    # table_rows = table.findAll('tr')
    # for tr in table_rows:
    #     td = tr.find_all('td')
    #     row = [tr.text for tr in td]
    #     print(row)
  

async def main():
    headers = {'Accept-Encoding':'identity'}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")
            return html


def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    sel = "body > div:nth-child(3) > div.LayoutOptionsAndBody > div.LayoutBody > div > div.Table > div.TableContents > table"
    table = soup.select_one(sel)
    table_rows = table.findAll('tr')
    df = pd.DataFrame()
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
    return df
loop = asyncio.get_event_loop()
r = loop.run_until_complete(main())
print(clean_html(r))
# asyncio.run(get_match())


    
