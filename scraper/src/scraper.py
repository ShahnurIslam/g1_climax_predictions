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

async def main():
    headers = {'Accept-Encoding':'identity'}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            html = await response.text()
            return html


def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    sel = "body > div:nth-child(3) > div.LayoutOptionsAndBody > div.LayoutBody > div > div.Table > div.TableContents > table"
    table = soup.select_one(sel)
    table_rows = table.findAll('tr')
    rows = []
    for ix,tr in enumerate(table_rows):
        td = tr.find_all('td')
        if ix == 0:
            next
        else:
            row = [td[0].text,
                    td[1].text,
                    td[3].find('span', {'class' : 'MatchType'}).text if td[3].find('span', {'class' : 'MatchType'}) is not None else '',
                    td[3].find('div', {'class' : 'MatchEventLine'}).text,
                    td[3].find('span', {'class' : 'MatchCard'}).text]
            rows.append(row)
    df = pd.DataFrame(rows,columns=['index','date','matchtype','matchevent','matchcard'])
    return df
def check_win(matchcard:str, person: str) -> bool:
    return matchcard.split(' ')[0] == person

def clean_dataframe(df):
    df['time'] = df['matchcard'].str.extract(r'(\d+:\d+)') 
    df['win'] = df['matchcard'].apply(lambda x: check_win(x,'Kazuchika'))
    return df

def elo_rating(df):
    rating = 200 + df['win'].sum() * 10
    return rating


loop = asyncio.get_event_loop()
r = loop.run_until_complete(main())
clean_df = clean_html(r)
clean_df =clean_dataframe(clean_df)
print(elo_rating(clean_df))


