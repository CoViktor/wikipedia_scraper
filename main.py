import os
import re
import json

import requests  # -> request.Session is in here
from bs4 import BeautifulSoup

# Suggestion by gpt4 instead of writing this twice in my code
def update_cookie_check(root_url, url, session, params=None): 
    # asks root to make root/cookie, and normal to implement on any total url str 
    # + session to import existing session from where it is called
    response = session.get(url, params=params)
    if response.status_code != 200:
        print(f'Status code: {response.status_code}... Refreshing cookies.')
        cookies_req = session.get(f'{root_url}/cookie')
        new_cookies = cookies_req.cookies
        response = session.get(url, params=params, cookies=new_cookies)
    return response

def get_first_paragraph(wikipedia_url, session) -> str:
    '''Returns first true paragraph of a wiki page as text.
    param wikipedia_url: requires wikipedia url
    param session: takes session as param to import the existing session from where the function is called'''
    response= session.get(wikipedia_url)
    content = response.content
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

def get_leaders():
    '''Get the leaders of the countries on 
    https://country-leaders.onrender.com, and store in dict'''
    root_url = 'https://country-leaders.onrender.com'
    session = requests.Session()  # Calling initial session object for persistent connection
    # Cookies: (can be done with cookies = session.get(f'{root_url}/cookie').cookies for short)
    cookies_url = '/cookie'
    cookies_req = session.get(f'{root_url}{cookies_url}')
    cookies = cookies_req.cookies
    # Countries: 
    countries_url = '/countries'
    countries = update_cookie_check(root_url, f'{root_url}{countries_url}', session)
    # Leaders:
    leaders_url = '/leaders'
    leaders_per_country = {}
    for country in countries.json():  # Not calling it as countries.json() anymore?
        print("Working on ", country, "... status code: ", countries.status_code)
        params = {'country': country}  # -> could be put in line below instead of params = params for shorter code
        leaders = update_cookie_check(root_url, f'{root_url}{leaders_url}', session, params=params)
        # Detecting status code Error
        leader_dict = {}
        for person in leaders.json():
            # Defining key 'name' and value 'wiki_url' for leader_list dict:
            name = f"{person.get('first_name')} {person.get('last_name')}"
            # Issue here: MA names: 3 guys become Mohammed None? & get lost in the code -> catch with if/else
            wiki_url = person.get('wikipedia_url')
            leader_dict[name] = get_first_paragraph(wiki_url, session)
        leaders_per_country[country] = leader_dict
    return leaders_per_country

def save(data):
    with open('data.json', 'w', encoding='utf-8') as output:
        json.dump(data, output)

# get leaders return structure: {country: [{person1dict}, {person2dict}]}
leaders_data = get_leaders()

save(leaders_data)

# with open('leaders.json') as input:
#     original_dict = json.load(input)

# Open file in append mode for debugging
# But first checking if an existing file should be removed
# if os.path.exists('first_paragraph.txt'):
#     os.remove('first_paragraph.txt')
# with open('first_paragraph.txt', 'a', encoding='utf-8') as file:   # DB
#     for country, leaders in leaders_data.items():  # -> this is how to access a dict in a dict: cal the first dict as a dict instead of just as an object
#         file.write(f'The leaders of {country} are:\n') 
#         json.dump(leaders, file, indent=4)  # -> json doens't take encoding from with open call...
#         file.write('\n\n')

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