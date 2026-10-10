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
from _county import get_county, translate_city
#
#
import requests


API_URL = 'https://careers.vidaxl.com/api/vacancy/'
BASE_URL = 'https://careers.vidaxl.com'


def request_and_collect_data():
    """
    Collect current Romania jobs from the vidaXL careers API.
    """

    response = requests.get(url=API_URL,
                            params={'filters[Country][]': 'Romania'},
                            headers={**DEFAULT_HEADERS,
                                     'X-Requested-With': 'XMLHttpRequest'},
                            timeout=30)
    response.raise_for_status()

    lst_with_data = []

    for job in response.json().get('vacancies', []):
        city = translate_city(job.get('city'))

        lst_with_data.append({
            'job_title': job.get('title'),
            'job_link': f"{BASE_URL}/vacancy/{job['id']}/{job['slug']}",
            'company': 'vidaXL',
            'country': 'Romania',
            'city': city,
            'county': get_county(city),
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
    company_name = 'vidaXL'  # add test comment
    data_list = request_and_collect_data()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('vidaXL',
                      'https://careers.vidaxl.com/uploads/vidaXL_purple_111x51px-02.svg'
                      ))