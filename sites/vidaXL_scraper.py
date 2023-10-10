#
#
#
#
# New scraper for -> vidaXL
# vidaXL job page -> https://careers.vidaxl.com/vacancies/country/romania
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
        url='https://careers.vidaxl.com/api/vacancy/?filters%5BCountry%5D%5B%5D=Romania&sort=date&sortDir=desc',
        headers=DEFAULT_HEADERS).json()['vacancies']

    lst_with_data = []

    for job in response:
        job_id = job['id']
        slug = job['slug']
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": job['title'],
            "job_link": f'https://careers.vidaxl.com/vacancy/{job_id}/{slug}',
            "company": "vidaXL",
            "country": "Romania",
            "city": job['city']
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'vidaXL'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('vidaXL',
                  'https://careers.vidaxl.com/uploads/vidaXL_purple_111x51px-02.svg'
                  ))
