#
#
#
#
# New scraper for -> RaiffeisenBank
# RaiffeisenBank job page -> https://www.ejobs.ro/company/raiffeisen/4779
#
#
from random import randint

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#

from bs4 import BeautifulSoup
import time
import requests
import uuid


def request_and_collect_data(page):
    """
    ... this func() make a simple requests
    and collect data from API.
    """

    response = requests.get(url=f'https://www.ejobs.ro/company/raiffeisen/4779/{page}',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    soup_data = soup.find_all('div', attrs={'class': 'JobCard'})

    lst_data = []

    for job in soup_data:
        lst_data.append({
            "id": str(uuid.uuid4()),
            "job_title": job.find('h2', attrs={'class': 'JCContentMiddle__Title'}).find('a').text,
            "job_link": 'https://www.ejobs.ro' + job.find('h2', attrs={'class': 'JCContentMiddle__Title'}).find('a')[
                'href'],
            "company": "RaiffeisenBank",
            "country": "Romania",
            "city": job.find('span', attrs={'class': 'JCContentMiddle__Info'}).text.strip(),
        })

    job_links_seen = set()
    final_lst_data = []
    for data in lst_data:
        job_link = data['job_link']
        if job_link not in job_links_seen:
            job_links_seen.add(job_link)
            final_lst_data.append(data)

    return final_lst_data


def scrape_all_data_from_() -> list:
    """
    Scrap all data from , and return big list.
    """

    page = 1
    flag = True

    big_lst_jobs = []
    while flag:

        # collect data from site!
        data_site = request_and_collect_data(page)

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


company_name = 'RaiffeisenBank'  # add test comment
data_list = scrape_all_data_from_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('RaiffeisenBank',
                  'https://www.sun-plaza.ro/wp-content/uploads/2016/10/raiffeisen-bank-logo.jpg'
                  ))
