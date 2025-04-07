import requests
from bs4 import BeautifulSoup

def fetch_concordia_info():
    url = "https://www.concordia.ca/academics/graduate/computer-science.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    text = soup.get_text(separator="\n")
    return text[:1000]