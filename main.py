import os
import re

import requests
from bs4 import BeautifulSoup

def get_leaders():
    '''Get the leaders of the countries on 
    https://country-leaders.onrender.com, and store in dict'''
    root_url = 'https://country-leaders.onrender.com'
    cookies_url = '/cookie'
    countries_url = '/countries'
    leaders_url = '/leaders'
    cookies_req = requests.get(f'{root_url}{cookies_url}')
    cookies = cookies_req.cookies
    countries = requests.get(f'{root_url}{countries_url}', cookies=cookies)
    leaders_per_country = {}
    for country in countries.json():
        params = {'country': country}
        leaders = requests.get(f'{root_url}{leaders_url}', params=params,
                           cookies=cookies)
        leader_list = []
        for person in leaders.json():
            leader_list.append(person)
        leaders_per_country[country] = leader_list
    return leaders_per_country

def get_first_paragraph(wikipedia_url) -> str:
    '''Returns first true paragraph of a wiki page as text.
    param: requires wikipedia url'''
    url = requests.get(wikipedia_url)
    content = url.content
    soup = BeautifulSoup(content, 'html.parser')
    # looking for paragraphs
    paragraphs = soup.find_all('p')
    for idx, p in enumerate(paragraphs):
        if len(p) > 10:
            first_paragraph = paragraphs[idx].text  # could be shorter: just return this
            # Cleaning the phonetics (start with / and finish with ;):
            clean_paragraph = re.sub(r'\[.*?\]', "", first_paragraph)
            # Cleaning references (between [])
            clean_paragraph = re.sub(r'\(/.*?;\)', "",  clean_paragraph)
            # Together would be re.sub(r'\[.*?\]|\(/.*?;\)', "", first_paragraph)
            break
    return clean_paragraph


#get leaders return structure: {country: [{person1dict}, {person2dict}]}
# Storing the structure in a variable: -> my mistake of not doing this made me call the function a ton
# of times in the for loop
leaders_data = get_leaders()

# Open file in append mode for debugging
# But first checking if an existing file should be removed
if os.path.exists('first_paragraph.txt'):
    os.remove('first_paragraph.txt')
with open('first_paragraph.txt', 'a', encoding='utf-8') as file:


    # Looping over countries:
    for country in leaders_data:
        print(f'\nWorking on {country} leaders...')
        file.write(f'\nThe leaders of {country}:\n')    # DB
        # Looping over leaders
        for leader in leaders_data[country]:
            name = f"{leader['first_name']} {leader['last_name']}"
            wiki_url = leader['wikipedia_url']
            first_paragraph = get_first_paragraph(wiki_url)
            file.write(f"{name}: {wiki_url}\n{first_paragraph}\n")  # DB
            # storing wiki content


print(f'Finished')


# next priorities: 
# loop 


# handle different languages for output:
# maybe don't do language changing in main loop, cause info might be way shorter
# find english wiki for everybody -> trying a bit
# make function with leader and countryname as input, that gets paragraph
            # en_wiki_url = re.sub("//[\w].", "//en",  leader['wikipedia_url'])
            # wiki_request = requests.get(en_wiki_url)
            # if wiki_request.status_code != 200:
            #     print(f'{wiki_request.status_code} {name} wiki not available in English, switching to original...')
            #     wiki_request = requests.get(leader['wikipedia_url'])

# ------------Debugging tools--------------------------------------------------------
        # HTML STRUCTURE
# Storing the HTML structure in a HTML file, accounting for encoding error
# pretty_html = soup.prettify()  # -> used for debugging and stuff & finding paragraphs
# with open('pretty_html_output.html', 'w', encoding='utf-8') as file:
#     file.write(pretty_html)

# Open file in append mode for debugging
# But first checking if an existing file should be removed
# if os.path.exists('first_paragraph.txt'):
#     os.remove('first_paragraph.txt')
# with open('first_paragraph.txt', 'a', encoding='utf-8') as file:
# file.write(f"{name}: {leader['wikipedia_url']}{url.status_code}\n{paragraphs[idx].text}\n")
# ------------------------------------------------------------------------------------