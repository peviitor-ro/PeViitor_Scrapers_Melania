#
#
#
# New scraper for -> Equilobe
# Equilobe page -> https://www.equilobe.com/new-openings

#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def req_and_collect_data_equilobe():
    """
    ... this func() make a simple requests
    and collect data from Acronis API.
    """

    response = requests.get('https://www.equilobe.com/new-openings',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='Zc7IjY')

    lst_with_data = []

    for dt in soup_data:
        title = dt.find('span').text
        link = dt.find('a')['href']
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Equilobe",
            "country": "Romania",
            "city": "Romania"
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Equilobe'  # add test comment
data_list = req_and_collect_data_equilobe()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Equilobe',
                  'https://static.wixstatic.com/media/e97736_955059ac6cc24e819aead464d7cc24be~mv2.png/v1/fit/w_2500,h_1330,al_c/e97736_955059ac6cc24e819aead464d7cc24be~mv2.png'
                  ))


