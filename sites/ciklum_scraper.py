#
#
#
# New scraper for -> Ciklum
# Ciklum page -> https://jobs.ciklum.com/jobs/
#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def req_and_collect_data_ciklum():
    """
    ... this func() make a simple requests
    and collect data from Acronis API.
    """

    response = requests.get('https://jobs.ciklum.com/jobs/?country=remote-ro&location=&category=',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', class_='vacancy-card__link')

    lst_with_data = []

    for dt in soup_data:
        title = dt.text
        link = dt['href']
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Ciklum",
            "country": "Romania",
            "remote": "remote"
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Ciklum'  # add test comment
data_list = req_and_collect_data_ciklum()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Ciklum',
                  'https://jobs.ciklum.com/wp-content/webpc-passthru.php?src=https://jobs.ciklum.com/wp-content/uploads/2017/11/Ciklum_Horizontal_Logo_RGB.png&nocache=1'
                  ))
