#
#
#
# New scraper for -> Druid
# Druid page -> https://www.druidai.com/careers

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
    and collect data from Druid API.
    """

    response = requests.get('https://www.druidai.com/careers',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='kl-offer-01__content')

    lst_with_data = []

    for dt in soup_data:
        location = dt.find('p').text.split(',')[1]
        link = dt.find('a')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": dt.find('h3').text,
            "job_link": link,
            "company": "Druid",
            "country": "Romania",
            "city": location
        })

        # if 'Romania' is found in location, return only the dictionaries that respect this criteria
        jobsRo = None
        for data in lst_with_data:
            if 'Romania' in data['city']:
                jobsRo = data
                data['city'] = data['city'].strip().split(' ')[0]
                break
        if jobsRo:
            return (jobsRo)


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Druid'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Druid',
                  'https://www.druidai.com/hubfs/druid-logo-dark.svg'
                  ))