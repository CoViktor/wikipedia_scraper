import os
import re

import requests
from bs4 import BeautifulSoup

# Suggestion by gpt4 instead of writing this twice in my code
def update_cookie_check(root_url, url, params=None, cookies=None):
    response = requests.get(url, params=params, cookies=cookies)
    if response.status_code != 200:
        print(f'Status code: {response.status_code}... Refreshing cookies.')
        cookies_req = requests.get(f'{root_url}/cookie')
        new_cookies = cookies_req.cookies
        response = requests.get(url, params=params, cookies=new_cookies)
    return response

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
        print("Working on " , country, "... status code: ", countries.status_code)
        params = {'country': country}
        leaders = update_cookie_check(root_url, f'{root_url}{leaders_url}', params=params, cookies=cookies)
        # Detecting status code Error
        leader_dict = {}
        for person in leaders.json():
            # Defining key 'name' and value 'wiki_url' for leader_list dict:
            name = f"{person.get('first_name')} {person.get('last_name')}"
            # Issue here: MA names: 3 guys become Mohammed None? & get lost in the code -> catch with if/else
            wiki_url = person.get('wikipedia_url')
            leader_dict[name] = get_first_paragraph(wiki_url)
        leaders_per_country[country] = leader_dict
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


#get leaders return structure: {country: [{person1dict}, {person2dict}]}
# Storing the structure in a variable: -> my mistake of not doing this made me call the function a ton
# of times in the for loop

leaders_data = get_leaders()
print(f'data type leaders_data: {type(leaders_data)}')
# print(leaders_data) -> terminal can't handle characters

# Open file in append mode for debugging
# But first checking if an existing file should be removed
if os.path.exists('first_paragraph.txt'):
    os.remove('first_paragraph.txt')
with open('first_paragraph.txt', 'a', encoding='utf-8') as file:   # DB
    for country, leaders in leaders_data.items():
        file.write(f'The leaders of {country} are:\n') 
        for leader_name, leader_info in leaders.items():
            file.write(f'{leader_name} : {leader_info}')      

print(f'Finished')


# next priorities: 

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