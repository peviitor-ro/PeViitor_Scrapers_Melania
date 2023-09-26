#
#
#
# New scraper for -> REEVO
# REEVO page -> https://reevotech.com/careers/

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
    and collect data from REEVO API.
    """

    response = requests.get('https://reevotech.com/careers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='jet-engine-listing-overlay-wrap')

    lst_with_data = []

    for dt in soup_data:
        location = dt.find('div', class_='jet-listing jet-listing-dynamic-terms').text
        title = dt.find('div', class_='jet-listing-dynamic-field__content').text
        link = dt['data-url']
        if 'romania' in location.lower():
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "REEVO",
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


company_name = 'REEVO'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('REEVO',
                  'https://reevotech.com/wp-content/uploads/2023/06/cropped-REEVO_LogotypeMonogram_Red_RGB.png'
                  ))
