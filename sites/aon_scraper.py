#
#
#
#
# New scraper for -> Aon
# Aon job page -> https://www.aon.com/en/
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
#
import requests
import uuid


def request_and_collect_data():
    """
    ... this func() make a simple requests
    and collect data from API.
    """

    response = requests.get(
        url='https://jobs.aon.com/api/jobs?location=Romania&woe=12&stretchUnit=MILES&stretch=10&page=1&sortBy=relevance&descending=false&internal=false',
        headers=DEFAULT_HEADERS).json()['jobs']

    lst_with_data = []

    for job in response:
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": job['data']['title'],
            "job_link": job['data']['meta_data']['canonical_url'],
            "company": "Aon",
            "country": "Romania",
            "city": job['data']['city']
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Aon'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Aon',
                  'https://cms.jibecdn.com/prod/aon/assets/HEADER-LOGO_IMG-en-us-1630680205587.png'
                  ))
