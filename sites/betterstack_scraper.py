#
#
#
# New scraper for -> BetterStack
# BetterStack page -> https://betterstack.com/careers

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
    and collect data from Softelligence API.
    """

    response = requests.get('https://betterstack.com/careers',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a',
                              class_='block pl-8 pr-6 py-5 hover:bg-neutral-800 flex justify-between items-center bg-[#1a202f]')

    lst_with_data = []

    for dt in soup_data:
        title = dt.find('div', class_='truncate').text.strip()
        if title != 'My role is not listed here':
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": 'https://betterstack.com/' + dt['href'],
                "company": "BetterStack",
                "country": "Romania",
                "remote": "remote"
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'BetterStack'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('BetterStack',
                  'https://betterstack.com/assets/v2/better-stack-logo-0dd586683a61184ea953948d207470eeec73c76d81d57cd8af24bf56b36a90db.svg'
                  ))



