#
#
#
# New scraper for -> Lensa
# Lensa page -> https://lensa.ro/cariere/
#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def request_and_collect_data():
    """
    ... this func() make a simple requests
    and collect data from Lensa API.
    """

    response = requests.get(
        url='https://mingle.ro/api/boards/mingle/jobs?q=department~in~%22563%22!companyUid~eq~%22lensa%22&page=0&pageSize=30&sort=jobTitle~ASC',
        headers=DEFAULT_HEADERS).json()['data']

    lst_with_data = []

    for job in response['results']:
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": job['jobTitle'],
            "job_link": f"https://lensa.mingle.ro/ro/apply/{job['publicUid']}",
            "company": "Lensa",
            "country": "Romania",
            "city": job['locations'][0]['name']
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Lensa'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Lensa',
                  'https://lensa.ro/views/lensa/images/layout/logo.svg?v=1695798332'
                  ))
