#
#
#
# New scraper for -> Mondly
# Mondly page -> https://www.mondly.com/careers

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

    response = requests.get('https://www.mondly.com/careers',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', class_='flex flex-col p-6 rounded-3lg shadow-5md bg-white')

    lst_with_data = []

    for dt in soup_data:
        location = dt.find('div', class_='text-2lg font-normal tracking-2small font-sans').text.split(':')[1].strip()
        title = dt.find('div', class_='text-mondly-darker-blue text-2xl font-medium underline font-sans').text
        link = dt['href']
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": 'https://www.mondly.com' + link,
            "company": "Mondly",
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


company_name = 'Mondly'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Mondly',
                  'https://edge.mondly.com/blog/wp-content/themes/mondly/img/logo.svg.gzip'
                  ))