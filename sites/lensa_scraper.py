#
#
#
# New scraper for -> Lensa
# Lensa page -> https://lensa.mingle.ro/ro/apply?tab=showroom
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import requests


API_URL = 'https://mingle.ro/api/boards/careers-page/jobs'
JOB_URL = 'https://lensa.mingle.ro/ro/apply/'
PAGE_SIZE = 50


def extract_cities(locations):
    """
    Keep only normalized city values that map to Romanian counties.
    """

    cities = []

    for location in locations:
        raw_city = location.get('label', '').strip()
        if not raw_city:
            continue

        normalized_city = translate_city(raw_city.title())
        if not normalized_city:
            continue

        county = get_county(normalized_city)
        if county and normalized_city not in cities:
            cities.append(normalized_city)

    return cities


def request_and_collect_data():
    """
    Collect Lensa showroom jobs from the public Mingle careers API.
    """

    lst_with_data = []
    seen_links = set()
    page = 0

    while True:
        response = requests.get(
            url=API_URL,
            headers=DEFAULT_HEADERS,
            params={
                'company': 'lensa',
                'category': 'showroom',
                'page': page,
                'pageSize': PAGE_SIZE,
            },
            timeout=30)
        response.raise_for_status()

        data = response.json()['data']
        jobs = data.get('results', [])
        if not jobs:
            break

        for job in jobs:
            cities = extract_cities(job.get('locations', []))

            if not cities:
                cities = ['Bucuresti']

            job_link = JOB_URL + job['uid']
            if job_link in seen_links:
                continue

            seen_links.add(job_link)
            lst_with_data.append({
                'job_title': job['title'],
                'job_link': job_link,
                'company': 'Lensa',
                'country': 'Romania',
                'city': cities,
                'county': get_county(cities),
                'remote': ['on-site']
            })

        pagination = data.get('pagination', {})
        if not pagination.get('hasNext'):
            break

        page += 1

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'Lensa'  # add test comment
    data_list = request_and_collect_data()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Lensa',
                      'https://lensa.ro/views/lensa/images/layout/logo.svg?v=1695798332'
                      ))
