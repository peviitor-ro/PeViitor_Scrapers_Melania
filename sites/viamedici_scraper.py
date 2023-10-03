#
#
#
# New scraper for -> Viamedici
# Viamedici page -> https://www.viamedici.com/career/
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
    and collect data from Viamedici API.
    """

    response = requests.get('https://www.viamedici.com/career/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='wp-block-columns row_xxl')

    lst_with_data = []

    for dt in soup_data:
        location = dt.find('div', class_='wp-block-column is-vertically-aligned-center col-12 col-sm-auto')
        title = dt.find('div', class_='wp-block-column is-vertically-aligned-center col-12 col-sm-4')
        if title and 'Romania' in location.text or 'Remote' in str(location):
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title.text,
                "job_link": dt.find('a')['href'],
                "company": "Viamedici",
                "country": "Romania",
                "city": location.text.split('/')
            })

        for job in lst_with_data:
            if 'Remote' in job['city'][-1]:
                job['city'] = job['city'][0]
                job['remote'] = 'remote'

    # for jobs in cities of Romania, 'city' key and also 'remote' key are printed
    tari = ['Iasi', 'Bucuresti', 'Bucharest', 'Cluj']
    filtered_list = [job for job in lst_with_data if any(tara in job.get('city', '') for tara in tari)]

    return filtered_list


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Viamedici'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Viamedici',
                  'https://www.viamedici.com/wp-content/uploads/2023/07/cropped-cropped-Viamedici-Logo-Original-1.png'
                  ))
