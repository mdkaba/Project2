import requests
from bs4 import BeautifulSoup


def fetch_concordia_info(urls):
    data = {}
    
    for url in urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text(separator="\n")
        data[url] = text[:1000]  # Store first 1000 characters from each URL

    return data

# Example usage
urls = [
    "https://www.concordia.ca/academics/graduate/computer-science.html",
    "https://www.concordia.ca/academics/undergraduate.html",
    "https://www.concordia.ca/admissions/undergraduate/programs.html",
    "https://www.concordia.ca/ginacody/computer-science-software-eng/programs/computer-science/mcompsc.html", 
    "https://www.concordia.ca/academics/undergraduate/health-life-sciences.html", 
    "https://www.concordia.ca/ginacody/computer-science-software-eng/programs/computer-science/mapcompsc.html", 
    "https://www.concordia.ca/admissions/undergraduate/programs-with-additional-requirements.html",
    "https://www.concordia.ca/ginacody/programs/undergraduate.html",
    "https://www.concordia.ca/ginacody/computer-science-software-eng/programs/computer-science/bachelor.html",
    "https://www.concordia.ca/academics/undergraduate/calendar/current/section-81-faculty-of-fine-arts/section-81-90-department-of-design-and-computation-arts/admission-to-the-specialization-and-minor-in-computation-arts-the-joint-major-in-computation-arts-and-computer-science-and-the-minor-in-game-design.html",
    "https://www.concordia.ca/academics/undergraduate/calendar.html",
    "https://www.concordia.ca/students/undergraduate/undergraduate-academic-dates.html",
    "https://www.concordia.ca/academics/undergraduate/calendar/current.html",
    "https://www.concordia.ca/academics/graduate/calendar/current/academic-calendar/current-academic-calendar-dates.html",
    "https://www.concordia.ca/academics/undergraduate/calendar/current/section-71-gina-cody-school-of-engineering-and-computer-science/section-71-70-department-of-computer-science-and-software-engineering/section-71-70-2-degree-requirements-bcompsc-.html",

]
info = fetch_concordia_info(urls)
for url, content in info.items():
    print(f"URL: {url}")
    print(f"Content: {content}\n")
