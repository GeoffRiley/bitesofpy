from collections import Counter

import bs4
import requests

COMMON_DOMAINS = ("https://bites-data.s3.us-east-2.amazonaws.com/"
                  "common-domains.html")
TARGET_DIV = {"class": "middle_info_noborder"}


def get_common_domains(url=COMMON_DOMAINS):
    """Scrape the url return the 100 most common domain names"""
    # div.middle_info_noborder > center > table
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    email_rows = soup.find('div', class_='middle_info_noborder').find_all('tr')
    return [row.find_all('td')[2].text for row in email_rows]


def get_most_common_domains(emails, common_domains=None):
    """Given a list of emails return the most common domain names,
       ignoring the list (or set) of common_domains"""
    if common_domains is None:
        common_domains = set(get_common_domains())

    c = Counter([em for e in emails if (em := e.split('@')[-1]) not in common_domains])
    return c.most_common()
