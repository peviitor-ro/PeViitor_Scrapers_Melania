#
#
#
# New scraper for -> BNPParibas
# BNPParibas page -> https://group.bnpparibas/en/careers
#
from bs4 import BeautifulSoup

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid
#
import time
from random import randint


def collect_data_from_site(page: int) -> list:
    """
    Collect all data from site.
    """

    response = requests.get(url=f'https://group.bnpparibas/en/careers/all-job-offers/roumanie?page={page}',
                            headers=DEFAULT_HEADERS)

    soup = BeautifulSoup(response.text, 'lxml')

    data_jobs = soup.find_all('a', class_='card-link')

    lst_with_data = []
    for dt in data_jobs:
        location = dt.find('div', class_='offer-location')
        title = dt.find('h3', class_='title-4')

        if title:
            link = dt['href']

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title.text,
                "job_link": 'https://group.bnpparibas/' + link,
                "company": "BNPParibas",
                "country": "Romania",
                "city": location.text.split(',')[0].strip()
            })

    return lst_with_data


def scrape_all_data_from_() -> list:
    """
    Scrap all data from , and return big list.
    """

    page = 1
    flag = True

    big_lst_jobs = []
    while flag:

        # collect data from site!
        data_site = collect_data_from_site(page)

        if data_site:
            big_lst_jobs.extend(data_site)

        else:
            flag = False

        page += 1
        time.sleep(randint(1, 2))

    return big_lst_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'BNPParibas'
data_list = scrape_all_data_from_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('BNPParibas',
                  'https://logos-world.net/wp-content/uploads/2021/02/BNP-Paribas-Logo-700x394.png'
                  ))
