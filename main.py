from utils.scraper import WikipediaScraper

# Create a wikipedia scraper
wiki_scraper = WikipediaScraper()

# Have it store all leaders from https://country-leaders.onrender.com a json file
wiki_scraper.to_json_file()
