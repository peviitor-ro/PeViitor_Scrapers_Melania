#
#
#
# New scraper for -> Wipro
# Wipro job page -> https://careers.wipro.com/careers-home

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
    and collect data from Acronis API.
    """

    response = requests.get(
        url='https://careers.wipro.com/api/jobs?stretchUnits=MILES&stretch=10&location=Romania&lat=46&lng=25&woe=12&limit=100&page=1&sortBy=relevance&descending=false&internal=false',
        headers=DEFAULT_HEADERS).json()

    lst_with_data = []

    for job in response['jobs']:
        link = job['data']['meta_data']['canonical_url']
        title = job['data']['title']
        city = job['data']['city']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Wipro",
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


company_name = 'Wipro'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Wipro',
                  'https://cms.jibecdn.com/prod/wipro/assets/HEADER-NAV_LOGO-en-us-1632914985450.png'
                  ))

