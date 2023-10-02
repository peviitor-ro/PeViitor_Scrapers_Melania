#
#
#
# New scraper for -> Essensys
# Essensys page -> https://essensys.ro/careers/

#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def req_and_collect_data_():
    """
    ... this func() make a simple requests
    and collect data from Essensys API.
    """

    response = requests.get('https://essensys.ro/careers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div',
                              class_='fusion-column-wrapper fusion-column-has-shadow fusion-flex-justify-content-flex-start fusion-content-layout-column')

    lst_with_data = []

    for dt in soup_data:

        title = dt.find('h5')
        city = dt.find('span')
        link = dt.find('a')
        if title:
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title.text,
                "job_link": link['href'],
                "company": "Essensys",
                "country": "Romania",
                "city": city.text.split(' /')
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Essensys'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Essensys',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNhcDj_EgzQKN81Bed5LQdnzZ0fs_R11sXpzboL2zEhA&s'
                  ))
