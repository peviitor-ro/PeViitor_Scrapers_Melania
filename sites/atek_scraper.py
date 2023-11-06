#
#
# New scraper for -> AtekSoftware
# AtekSoftware job page -> https://atek.ro/career.html

#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def req_and_collect_data():
    """
    ... this func() make a simple requests
    and collect data from Atek API.
    """

    response = requests.get('https://atek.ro/career.html',
                            headers=DEFAULT_HEADERS)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='col-lg-6 col-md-12')

    lst_with_data = []
    for dt in soup_data:
        location = dt.find('ul', class_='job-info-list list-inline list-unstyled text-muted').text.strip().split('\n')
        for item in location:
            if 'românia' in item.lower() or 'romania' in item.lower():
                title = dt.find('h3').text
                link = dt.find('a')['href']
                lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": 'https://atek.ro/' + link,
                    "company": "AtekSoftware",
                    "country": "Romania",
                    "city": ', '.join(location).split(', ')[1::2]
                })

    job_links_existent = set()
    newlist_with_data = []

    for job in lst_with_data:

        if job['job_link'] not in job_links_existent:
            job_links_existent.add(job['job_link'])
            newlist_with_data.append(job)

    return newlist_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'AtekSoftware'  # add test comment
data_list = req_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('AtekSoftware',
                  'https://atek.ro/assets/img/logo.png'
                  ))
