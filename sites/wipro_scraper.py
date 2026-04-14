#
#
#
# New scraper for -> Wipro
# Wipro job page -> https://careers.wipro.com/go/Romania/9471155/

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import re
import requests


CAREERS_URL = 'https://careers.wipro.com/go/Romania/9471155/'
JOBS_URL = 'https://careers.wipro.com/services/recruiting/v1/jobs'
CATEGORY_ID = 9471155


def get_csrf_token():
    response = requests.get(CAREERS_URL,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()

    match = re.search(r'CSRFToken\s*=\s*"([^"]+)"', response.text)
    if not match:
        raise ValueError('Wipro CSRF token not found')

    return match.group(1)


def normalize_remote(title):
    title_lower = title.lower()

    if 'hybrid / remote' in title_lower or 'hybrid/remote' in title_lower:
        return ['Hybrid']
    if 'full remote' in title_lower or '(remote' in title_lower or '- remote' in title_lower:
        return ['Remote']
    if 'hybrid' in title_lower:
        return ['Hybrid']

    return ['on-site']


def request_and_collect_data():
    """
    Collect current Wipro jobs from the Romania category page.
    """

    csrf_token = get_csrf_token()
    headers = {
        **DEFAULT_HEADERS,
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrf_token,
    }

    lst_with_data = []
    page = 0
    total_jobs = None

    while total_jobs is None or len(lst_with_data) < total_jobs:
        response = requests.post(
            JOBS_URL,
            headers=headers,
            json={
                'locale': 'en_US',
                'pageNumber': page,
                'sortBy': 'recent',
                'keywords': '',
                'location': '',
                'facetFilters': {},
                'categoryId': CATEGORY_ID,
            },
            timeout=30)
        response.raise_for_status()

        data = response.json()
        total_jobs = data.get('totalJobs', 0)
        jobs = data.get('jobSearchResult', [])
        if not jobs:
            break

        for item in jobs:
            job = item['response']
            title = job['unifiedStandardTitle']
            slug = job.get('unifiedUrlTitle') or job.get('urlTitle')
            job_id = job['id']

            cities = []
            for raw_city in job.get('sfstd_jobLocation_obj', []):
                normalized_city = translate_city(raw_city.replace('-WSM1', '').strip())
                if normalized_city and normalized_city not in cities:
                    cities.append(normalized_city)

            if not cities:
                continue

            lst_with_data.append({
                'job_title': title,
                'job_link': f'https://careers.wipro.com/job/{slug}/{job_id}-en_US',
                'company': 'Wipro',
                'country': 'Romania',
                'city': cities,
                'county': get_county(cities),
                'remote': normalize_remote(title)
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
    company_name = 'Wipro'  # add test comment
    data_list = request_and_collect_data()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Wipro',
                      'https://cms.jibecdn.com/prod/wipro/assets/HEADER-NAV_LOGO-en-us-1632914985450.png'
                      ))
