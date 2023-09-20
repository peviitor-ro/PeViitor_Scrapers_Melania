#
#
#
# New scraper for -> Huf
# Huf page -> https://www.huf-group.com/en/career/job-vacancies
#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def req_and_collect_data_huf():
    """
    ... this func() make a simple requests
    and collect data from Acronis API.
    """

    response = requests.get(
        'https://www.huf-group.com/en/career/job-vacancies?title=&field_dd_job_category_target_id=All&field_dd_job_site_target_id_entityreference_filter',
        headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', class_='info-card')

    lst_with_data = []

    for dt in soup_data:
        location = dt.text.strip()
        title = dt.find('span').text
        link = dt['href']

        if 'rumänien' in location.lower():
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": 'https://www.huf-group.com/' + link,
                "company": "Huf",
                "country": "Romania",
                "city": location.split()[0]
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Huf'  # add test comment
data_list = req_and_collect_data_huf()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Huf',
                  'https://upload.wikimedia.org/wikipedia/commons/0/09/Huf_Group_Logo_RGB_2020.svg'
                  ))
