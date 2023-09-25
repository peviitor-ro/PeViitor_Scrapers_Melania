#
#
#
# New scraper for -> DLAPiper
# DLAPiper page -> https://careers.dlapiper.com/job-search/
#
#
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
    and collect data from DLA Piper API.
    """

    response = requests.get(
        'https://careers.dlapiper.com/job-search/?submit=1&offset=0&sort_by=most-recent&search_text=&location=romania&job_function=',
        headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='job-result-box')

    lst_with_data = []

    for dt in soup_data:
        location = dt.find('p', class_='location').text
        title = dt.find('h3', class_='title').text
        link = dt.find('a', class_='button-link')['href']
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "DLAPiper",
            "country": "Romania",
            "city": location.split(',')[0]
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'DLAPiper'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('DLAPiper',
                  'https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/DLA_Piper_logo.svg/300px-DLA_Piper_logo.svg.png'
                  ))
