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
    print(cookies_req.status_code)
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


wiki_request = requests.get(get_leaders()['be'][5]['wikipedia_url'])
print(f'Statuscode: {wiki_request.status_code}')
content = wiki_request.content
soup = BeautifulSoup(content, 'html.parser')
# print(soup.get_text())  => bouncing on error due to unknown characters.. 
# solution below by gpt:
# print(soup.get_text().encode('utf-8', errors='replace'))

# Storing the HTML structure in a HTML file, accounting for encoding error
pretty_html = soup.prettify()  # -> used for debugging and stuff
with open('pretty_html_output.html', 'w', encoding='utf-8') as file:
    file.write(pretty_html)

# Storing the paragaphs in a txt file, accounting for encoding error
paragraphs = soup.find_all('p')  # -> storing all paragraphs in a variable
with open('paragraphs.txt', 'w', encoding='utf-8') as file:
    for paragr in paragraphs:
        file.write(paragr.text)

# Printing each paragraph text -> won't work due to terminal not handling the encoding
# for p in paragraphs:
#     print(p.text)

# Calling specific paragraph text, accounting for unicodeencodeerror requires writing it in a file
# I think terminal can't handle it
with open('first_paragraph.txt', 'w', encoding='utf-8') as file:
    file.write(paragraphs[1].text)

