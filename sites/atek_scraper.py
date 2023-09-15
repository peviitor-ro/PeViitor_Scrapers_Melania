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
    and collect data from Acronis API.
    """

    response = requests.get('https://atek.ro/career.html',
                            headers=DEFAULT_HEADERS)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='col-lg-6 col-md-12')

    lst_with_data = []
    for dt in soup_data:
        location = dt.find('ul', class_='job-info-list list-inline list-unstyled text-muted').find_all('li', class_='list-inline-item')[1].text.strip()
  
        if 'românia' in location.lower() or 'romania' in location.lower():
            title = dt.find('h3').text
            link = dt.find('a')['href']
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": 'https://atek.ro/' + link,
                "company": "AtekSoftware",
                "country": "Romania",
                "city": location.split(',')[0].strip()
            })

    return lst_with_data


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
