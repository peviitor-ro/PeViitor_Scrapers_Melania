#
#
#
#
# New scraper for -> Accessgroup
# Accessgroup page -> https://careers.theaccessgroup.com/jobs?source=google.com
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


def custom_heders():
    res = requests.head('https://careers.theaccessgroup.com/jobs/romania?source=google.com').headers['Set-Cookie']

    headers = {
        'authority': 'careers.theaccessgroup.com',
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': f'google_cid=; {res}',
        'referer': 'https://careers.theaccessgroup.com/jobs?source=google.com',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-pjax': 'true',
        'x-pjax-container': '#pjax-content',
        'x-requested-with': 'XMLHttpRequest',
    }

    return headers


def collect_data_from_site(page: int) -> list:
    """
    Collect all data from site.
    """

    response = requests.get(
        url=f'https://careers.theaccessgroup.com/jobs/romania?_pjax=%23pjax-content&page={page}&_pjax=%23pjax-content',
        headers=custom_heders())

    soup = BeautifulSoup(response.text, 'lxml')

    data_jobs = soup.find_all('div', class_='job-details')

    lst_with_data = []
    for dt in data_jobs:
        city = dt.find('li').text
        title = dt.find('a').text
        link = dt.find('a')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": 'https://careers.theaccessgroup.com/' + link,
            "company": "Accessgroup",
            "country": "Romania",
            "city": city
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

        #
        time.sleep(randint(1, 2))

    return big_lst_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Accessgroup'  # add test comment
data_list = scrape_all_data_from_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Accessgroup',
                  'https://seeklogo.com/images/T/the-access-group-logo-3BF0ABEC34-seeklogo.com.png'
                  ))
