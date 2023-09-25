#
#
#
# New scraper for -> LucaNet
# LucaNet page -> https://jobs.lucanet.com/job-list/?office=Romania
#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def request_and_collect_data():
    """
    ... this func() make a simple requests
    and collect data from Acronis API.
    """

    response = requests.get(
        url='https://api.jobs.lucanet.com/jobs/?office=Romania&limit=50',
        headers=DEFAULT_HEADERS).json()['rows']

    lst_with_data = []

    for job in response:
        link = job['slug']
        title = job['name']
        city = job['office']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": 'https://jobs.lucanet.com/job/' + link,
            "company": "LucaNet",
            "country": "Romania",
            "city": city
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'LucaNet'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('LucaNet',
                  'https://www.lucanet.com/fileadmin/user_upload/Images_and_Graphics/Logos/LucaNet/logo-lucanet-ohne-claim-2020-rgb.png'
                  ))
