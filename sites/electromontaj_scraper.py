#
#
# New scraper for -> Electromontaj
# Electromontaj page https://electromontaj.ro/cariere/
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import re
import requests


API_URL = 'https://mingle.ro/api/boards/careers-page/jobs?company=electromontaj'
JOB_URL = 'https://electromontaj.mingle.ro/ro/apply/'


def extract_cities(location_text):
    """
    Extract and normalize Romania cities from a location label.
    """

    split_cities = re.split(r',|\bsi\b|\bși\b|/|\|', location_text, flags=re.IGNORECASE)

    cities = []
    for city in split_cities:
        normalized_city = translate_city(city.strip(' .;:\n\t'))
        if not normalized_city:
            continue

        county = get_county(normalized_city)
        if county and normalized_city not in cities:
            cities.append(normalized_city)

    return cities


def request_and_collect_data():
    """
    Collect jobs from the Electromontaj public Mingle careers API.
    """

    response = requests.get(API_URL,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()
    jobs = response.json().get('data', {}).get('results', [])

    lst_with_data = []

    for job in jobs:
        location_labels = [location.get('label', '') for location in job.get('locations', [])]
        cities = []

        for label in location_labels:
            for city in extract_cities(label):
                if city not in cities:
                    cities.append(city)

        if not cities:
            continue

        lst_with_data.append({
            "job_title": job['title'].strip(),
            "job_link": JOB_URL + job['uid'],
            "company": "Electromontaj Scraper",
            "country": "Romania",
            "city": cities,
            "county": get_county(cities),
            "remote": ["on-site"]
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
    company_name = 'Electromontaj Scraper'  # add test comment
    data_list = request_and_collect_data()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Electromontaj',
                      'https://mla4lxcw4mmg.i.optimole.com/cb:7Jpy.32b98/w:391/h:184/q:mauto/ig:avif/f:best/https://electromontaj.ro/wp-content/uploads/2021/01/Logo-Electromontaj.svg'
                      ))
