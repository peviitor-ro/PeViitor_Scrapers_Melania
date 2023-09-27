#
#
#
#
# New scraper for -> RaiffeisenBank
# RaiffeisenBank job page -> https://www.ejobs.ro/company/raiffeisen/4779
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

    response = requests.get(url='https://api.ejobs.ro/companies/4779?jobsPageNo=1&jobsPageSize=100',
                            headers=DEFAULT_HEADERS).json()['jobs']

    lst_with_data = []

    for job in response:
        jobId = job['id']
        link = str(job['slug']) + '/' + str(jobId)
        title = job['title']
        city = job['locations'][0]

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": 'https://www.ejobs.ro/user/locuri-de-munca/' + link,
            "company": "RaiffeisenBank",
            "country": "Romania",
            "city": city
        })

    for job in lst_with_data:

        if 'address' in job['city']:
            job['city'] = job['city']['address'].split(',')[0]
        else:
            job['city'] = 'Romania'

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'RaiffeisenBank'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('RaiffeisenBank',
                  'https://content.ejobs.ro/img/logos/4/4779.jpg'
                  ))
