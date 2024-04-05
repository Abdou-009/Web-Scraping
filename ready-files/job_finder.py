import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_jobs(url):
    job_offers = []
    
    response = requests.get(url)
    print("The status is:", response.status_code)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    job_announcements = soup.find_all('div', class_='job-announcement')
    
    threshold_date = datetime.now() - timedelta(days=2)
    
    for announcement in job_announcements:
        date_string = announcement.find(class_='date').get_text(strip=True)
        
        if 'before' in date_string:
            days_ago = int(date_string.split()[1])
            announcement_date = datetime.now() - timedelta(days=days_ago)
        else:
            announcement_date = datetime.strptime(date_string, '%d/%m/%Y')
        
        if announcement_date >= threshold_date:
            job_title = announcement.find('h2').get_text(strip=True)
            job_description = announcement.find('p').get_text(strip=True)
            job_offers.append({'title': job_title, 'description': job_description, 'date': announcement_date})
    
    return job_offers

url = 'https://tawothifdz.com/?s=hse'
qhse_job_offers = scrape_jobs(url)

for offer in qhse_job_offers:
    print(f"Title: {offer['title']}")
    print(f"Description: {offer['description']}")
    print(f"Date: {offer['date']}")
    print()
