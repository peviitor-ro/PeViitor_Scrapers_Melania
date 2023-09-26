#
#
#
# New scraper for -> TDCX
# TDCX job page -> https://www.tdcx.com/careers/jobs/

#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def request_and_collect_data():
    """
    ... this func() make a simple requests
    and collect data from API.
    """

    response = requests.get(
        url='https://api.tdcx.com/jobs?page=1&limit=1000',
        headers=DEFAULT_HEADERS).json()['jobs']

    lst_with_data = []

    for job in response:
        jobID = job['jobId']
        title = job['title']
        city = job['filter1'][0]['value']
        if 'romania' in city.lower():
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": 'https://www.tdcx.com/careers/details/?jobId=' + jobID,
                "company": "TDCX",
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


company_name = 'TDCX'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('TDCX',
                  'https://s28.q4cdn.com/548328440/files/design/logo.svg'
                  ))
