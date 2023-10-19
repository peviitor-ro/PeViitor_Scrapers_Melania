#
#
#
# New scraper for -> Everymatrix
# Everymatrix page -> https://everymatrix.teamtailor.com/jobs?location=Bucharest&query=

#

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
    and collect data from Everymatrix API.
    """

    response = requests.get('https://everymatrix.teamtailor.com/jobs?location=Bucharest&query=',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('li',
                              class_='transition-opacity duration-150 border rounded block-grid-item border-block-base-text border-opacity-15')

    lst_with_data = []

    for dt in soup_data:
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": dt.find('span', class_='text-block-base-link company-link-style').text,
            "job_link": dt.find('a')['href'],
            "company": "Everymatrix",
            "country": "Romania",
            "city": "Bucharest",
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Everymatrix'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Everymatrix',
                  'https://yt3.googleusercontent.com/ytc/APkrFKY4hNjWQM3qepDLxkwrM-YamC-fDU7dKqBTnXt3Gw=s900-c-k-c0x00ffffff-no-rj'
                  ))
