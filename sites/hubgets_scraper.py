#
#
#
# New scraper for -> Hubgets
# Hubgets page -> https://www.hubgets.com/jobs/

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
    and collect data from Acronis API.
    """

    response = requests.get('https://www.hubgets.com/jobs/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('tr')

    lst_with_data = []

    for dt in soup_data:
        title = dt.find('h2')
        location = dt.find('h3', class_="pull-right")
        link = dt.find('div', class_='row clickable')
        if title:
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title.text,
                "job_link": 'https://www.hubgets.com/jobs/#job-' + link['data-job-id'],
                "company": "Hubgets",
                "country": "Romania",
                "city": location.text.split('/')[1].strip()
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Hubgets'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Hubgets',
                  'https://www.hubgets.com/media/images/logo-hubgets-simple@2x.png'
                  ))
