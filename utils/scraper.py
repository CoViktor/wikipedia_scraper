import json
import re

import requests
from bs4 import BeautifulSoup


class WikipediaScraper:
    '''Scraper object that allows to structurally retreive
    data from the API.
    Methods:
    -refresh_cookie(): Returns a new cookie if the cookie has expired
    -get_countries(): Returns a list of the countries supported by the API
    -get_leaders(country): Populates leader_data object with data retrieved
                            from api
    -get_first_paragraph(wikipedia_url): Returns first paragraph of a wiki page
    -to_json_file(filepath): Stores the data structure into a JSON file
    '''
    def __init__(self) -> None:
        self.base_url = 'https://country-leaders.onrender.com'
        self.country_endpoint = '/countries'
        self.leaders_endpoint = '/leaders'
        self.cookies_endpoint = '/cookie'
        self.leaders_data = {}
        self.cookie = (requests.get(f'{self.base_url}/cookie')).cookies

    def refresh_cookie(self):
        '''Replaces self.cookie with a new cookie if the cookie if the cookie has expired.'''

        self.cookie = (requests.get(f'{self.base_url}/cookie')).cookies
        print('Refreshed cookies')

    def get_countries(self):
        '''Returns a list of the countries supported by the API'''
        countries = requests.get(f'{self.base_url}{self.country_endpoint}',
                                 cookies=self.cookie)
        return countries.json()
    
    def get_leaders(self, country):
        '''Returns a dict that contains names and wiki url for each leader of 
        the country
        Param:
        country: country from the list returned by self.get_countries()'''
        params = {'country': country}
        leaders = requests.get(f'{self.base_url}{self.leaders_endpoint}',
                               params=params, cookies=self.cookie)
        leader_dict = {}
        for person in leaders.json():
            name = f"{person.get('first_name')} {person.get('last_name')}"
            wiki_url = person.get('wikipedia_url')
            wiki_content = self.first_paragraph(wiki_url)
            leader_dict[name] = wiki_content
        return leader_dict

    def first_paragraph(self, wikipedia_url):
        '''Returns the first paragraph of a wiki page that contains text.
        Additionaly, cleans out some of the noise in the paragraph.
        Param:
        wikipedia_url: str of a wikipedia url'''
        soup = BeautifulSoup((requests.get(wikipedia_url)).content, 'html.parser')
        paragraphs = soup.find_all('p')
        for idx, p in enumerate(paragraphs):
            if len(p) > 10:
                first_paragraph = paragraphs[idx].text
                # Cleaning out the references
                clean_paragraph = re.sub(r'\[.*?\]', "", first_paragraph)
                # Cleaning out the fonetics, very conveluted regex by courtesy of gpt-4
                clean_paragraph = re.sub(r'(\([^\)]*?)\/[^\s\)]+?[^\)]*?(\d{4}.*?\d{4})?[^\)]*?\)', lambda m: m.group(1) + m.group(2) + ')' if m.group(2) else '', clean_paragraph)
                clean_paragraph = re.sub(r'\s*uitspraakⓘ\s*', '', clean_paragraph)
                # Final cleanup of resulting double spaces & empty brackets
                clean_paragraph = re.sub(r'\s{2,}', ' ', clean_paragraph)
                clean_paragraph = re.sub(r'\(\s*\)', ' ', clean_paragraph)
                break
        return clean_paragraph

    def to_json_file(self, filepath='./leaders_data.json'):
        '''Stores the data as a json file.
        Param:
        filepath: str that contains the relative file pathing.'''
        countries = self.get_countries()
        all_countries_leaders = {}
        for country in countries:
            print(f'Working on {country}...')
            try:
                all_countries_leaders[country] = self.get_leaders(country)
            except AttributeError:
                self.refresh_cookie()
                all_countries_leaders[country] = self.get_leaders(country)
        with open(filepath, 'w', encoding='utf-8') as output:
            json.dump(all_countries_leaders, output, ensure_ascii=False, indent=4)