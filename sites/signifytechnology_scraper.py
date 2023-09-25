#
#
#
# New scraper for -> Signifytechnology
# Signifytechnology page -> https://www.signifytechnology.com/jobs

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

    response = requests.get(
        url=f'https://www.signifytechnology.com/jobs?page={page}&query=&selected_locations=798549&sort_type=relevance&submit=Search',
        headers=DEFAULT_HEADERS)

    soup = BeautifulSoup(response.text, 'lxml')

    data_jobs = soup.find_all('div', class_='job-details')

    lst_with_data = []

    for dt in data_jobs:
        title = dt.find('a')
        location = dt.find('li', class_="results-job-location").text
        link = dt.find('a')['href']
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title.text,
            "job_link": 'https://www.signifytechnology.com/' + link,
            "company": "Signifytechnology",
            "country": "Romania",
            "city": location
        })

    for job in lst_with_data:
        if job['city'] == 'Sector 1':
            job['city'] = 'Bucuresti'

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


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Signifytechnology'
data_list = scrape_all_data_from_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Signifytechnology',
                  'https://www.signifytechnology.com/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNXFuQlE9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--4bfcf25b1cc081a89f45ed3ebc205c06de9a1dfc/logo-h-grey1571762.png'
                  ))
