#
#
#
# New scraper for -> Worldline
# Worldline page -> https://jobs.worldline.com/search/?q=&locationsearch=&searchResultView=LIST&markerViewed=&carouselIndex=&facetFilters=%7B%22jobLocationCountry%22%3A%5B%22Romania%22%5D%7D&pageNumber=0

from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import requests
import urllib3


CAREERS_URL = 'https://jobs.worldline.com/search/?q=&locationsearch=&searchResultView=LIST&markerViewed=&carouselIndex=&facetFilters=%7B%22jobLocationCountry%22%3A%5B%22Romania%22%5D%7D&pageNumber=0'
JOBS_URL = 'https://jobs.worldline.com/services/recruiting/v1/jobs'


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def normalize_locations(location_values):
    cities = []
    has_remote_location = False

    for raw_location in location_values:
        cleaned = raw_location.strip()
        parts = [part.strip() for part in cleaned.split('-') if part.strip()]
        if len(parts) < 2:
            continue

        city = parts[-1]
        if city == 'Remote':
            has_remote_location = True
            continue

        normalized_city = translate_city(city)
        if normalized_city and normalized_city not in cities:
            cities.append(normalized_city)

    return cities, has_remote_location


def normalize_remote(work_modes, has_remote_location):
    work_mode = (work_modes[0] if work_modes else '').strip().lower()

    if work_mode == 'hybrid':
        return ['Hybrid']
    if work_mode == 'remote' or has_remote_location:
        return ['Remote']

    return ['on-site']


def req_and_collect_data_():
    """
    Collect current Romania jobs from the Worldline careers endpoint.
    """

    lst_with_data = []
    seen_links = set()
    page = 0
    while True:
        response = requests.post(
            JOBS_URL,
            json={
                'keywords': '',
                'locale': 'en_US',
                'location': '',
                'pageNumber': page,
                'sortBy': 'recent',
                'facetFilters': {
                    'jobLocationCountry': ['Romania']
                }
            },
            timeout=30,
            verify=False)
        response.raise_for_status()

        data = response.json()
        jobs = data.get('jobSearchResult', [])
        if not jobs:
            break

        for item in jobs:
            job = item['response']
            cities, has_remote_location = normalize_locations(job.get('jobLocationShort', []))
            if not cities:
                cities = ['Bucuresti']

            slug = job.get('unifiedUrlTitle') or job.get('urlTitle')
            job_id = job['id']
            job_link = f'https://jobs.worldline.com/job/{slug}/{job_id}-en_US'
            if job_link in seen_links:
                continue

            seen_links.add(job_link)
            lst_with_data.append({
                'job_title': job['unifiedStandardTitle'],
                'job_link': job_link,
                'company': 'Worldline',
                'country': 'Romania',
                'city': cities,
                'county': get_county(cities),
                'remote': normalize_remote(job.get('custWorkMode', []), has_remote_location)
            })

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
    company_name = 'Worldline'  # add test comment
    data_list = req_and_collect_data_()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Worldline',
                      'https://www.parking.net/upload/banners/Links/worldline/logoworldline1.png'
                      ))
