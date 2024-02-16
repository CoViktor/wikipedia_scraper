#  :newspaper: wikipedia scraper :newspaper:
[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


## 🏢 Description

A script that takes an API containing an array of countries and their current and past leaders, and crawls wikipedia for the first paragraph of the wikipedia page of each of these leaders. The WikipediaScraper class has a method that saves all this data in a json file.

![wiki_img](https://i.insider.com/5fbd515550e71a001155724f?width=400)

## 📦 Repo structure

```
.
├── utils/
│   └── scraper.py
├── .gitignore
├── leaders_data.json
├── main.py
├── README.md
└── requirements.txt
```
# 🚧 Installation 

1. Clone the repository to your local machine.

2. To run the script, you can execute the `main.py` file from your command line:

    ```
    python main.py
    ```

3. The required dependencies are available in requirements.txt


## ✔️ Usage 



```python
# Create a wikipedia scraper
wiki_scraper = WikipediaScraper()

# Have it store all leaders from https://country-leaders.onrender.com a json file
wiki_scraper.to_json_file()
```

A sneakpeek inside the WikipediaScraper class and its methods:

```python
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

```

## ⏱️ Timeline

This project was finished over the timespan of 3 days.

## 📌 Personal Situation
This project was done as part of the AI Boocamp at [BeCode.org](https://becode.org/), where trainees are challenged to constantly grow their developer skillset in creative ways, through both individual projects and teamwork.

Connect with me on [LinkedIn](https://www.linkedin.com/in/viktor-cosaert/).

