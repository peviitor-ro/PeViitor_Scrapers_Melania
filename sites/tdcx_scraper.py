#
#
#
# New scraper for -> TDCX
# TDCX job page -> https://www.tdcx.com/careers/jobs/

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests


API_URL = 'https://api.tdcx.com/jobs?page=1&limit=1000'
JOB_URL = 'https://jobs.tdcx.com/job-invite/'


def request_and_collect_data():
    """
    Collect Romania jobs from the live TDCX jobs API.
    """

    response = requests.get(url=API_URL,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()
    jobs = response.json()['jobs']

    lst_with_data = []

    for job in jobs:
        location_values = [item.get('value', '') for item in job.get('filter1', [])]
        if not any('romania' in value.lower() for value in location_values):
            continue

        lst_with_data.append({
            'job_title': job['title'],
            'job_link': f"{JOB_URL}{job['jobId']}/",
            'company': 'TDCX',
            'country': 'Romania',
            'city': 'Bucuresti',
            'county': 'Bucuresti',
            'remote': ['on-site']
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'TDCX'  # add test comment
    data_list = request_and_collect_data()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('TDCX',
                      'https://s28.q4cdn.com/548328440/files/design/logo.svg'
                      ))
