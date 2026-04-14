#
#
#
# New scraper for -> BGS
# BGS page -> https://bgs.ro/recrutare
#

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#


API_URL = 'https://bgs.ro/api/jobs'
DEFAULT_CITY = 'Bucuresti'
DEFAULT_COUNTY = 'Bucuresti'
KNOWN_CITIES = {
    'Bucuresti': 'Bucuresti',
    'București': 'Bucuresti',
    'Timisoara': 'Timisoara',
    'Timișoara': 'Timisoara',
    'Galati': 'Galati',
    'Galați': 'Galati',
    'Braila': 'Braila',
    'Brăila': 'Braila',
    'Ploiesti': 'Ploiesti',
    'Ploiești': 'Ploiesti',
    'Bistrita': 'Bistrita',
    'Bistrița': 'Bistrita'
}


def get_city_from_title(title: str) -> str:
    normalized_title = title.replace('–', '-').replace('—', '-')

    if ' - ' in normalized_title:
        possible_city = normalized_title.rsplit(' - ', 1)[-1].strip()
        if possible_city in KNOWN_CITIES:
            return KNOWN_CITIES[possible_city]

    return DEFAULT_CITY


def req_and_collect_data_():
    """
    Collect active jobs from the new BGS jobs API.
    """

    response = requests.get(API_URL,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()

    jobs = response.json()
    lst_with_data = []

    for job in jobs:
        if not job.get('isActive'):
            continue

        city = get_city_from_title(job['title'])
        lst_with_data.append({
            "job_title": job['title'],
            "job_link": 'https://bgs.ro/recrutare',
            "company": "BGS",
            "country": "Romania",
            "city": city,
            "county": DEFAULT_COUNTY
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
    company_name = 'BGS'  # add test comment
    data_list = req_and_collect_data_()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('BGS',
                      'https://bgs.ro/image/cachewebp/catalog/logo-400x152.webp'
                      ))
