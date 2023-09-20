#
#
#
# New scraper for -> Smartree
# Smartree page -> https://www.smartree.com/cariere

#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def req_and_collect_data_smartree():
    """
    ... this func() make a simple requests
    and collect data from Acronis API.
    """

    response = requests.get('https://www.smartree.com/cariere',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='jlbox')

    lst_with_data = []

    for dt in soup_data:
        location = dt.text.split()[-3]
        title = dt.find('a').text
        link = dt.find('a')['href']
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Smartree",
            "country": "Romania",
            "city": location
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Smartree'  # add test comment
data_list = req_and_collect_data_smartree()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Smartree',
                  'https://www.smartree.com/pages/tpl/front/assets/images/logo-new.png'
                  ))
