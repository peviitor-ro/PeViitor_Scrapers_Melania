#
#
#
#
# New scraper for -> RaiffeisenBank
# RaiffeisenBank job page -> https://cariere.raiffeisen.ro/jobs
#
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import json
import subprocess


JOBS_URL = 'https://cariere.raiffeisen.ro/jobs/load'


def fetch_jobs_page(page):
    """
    Fetch one public jobs page from the Raiffeisen careers endpoint.
    """

    result = subprocess.run(
        ['curl', '-k', '-s', f'{JOBS_URL}?page={page}'],
        capture_output=True,
        text=True,
        check=True)

    return json.loads(result.stdout)


def normalize_remote(presence_name):
    presence_name = (presence_name or '').strip().lower()

    if presence_name == 'hybrid':
        return ['Hybrid']
    if presence_name == 'remote':
        return ['Remote']

    return ['on-site']


def request_and_collect_data():
    """
    Collect all public Raiffeisen jobs from the current careers endpoint.
    """

    first_page = fetch_jobs_page(1)['data']
    total_pages = first_page['pagination']['last']
    all_jobs = first_page['jobs']

    for page in range(2, total_pages + 1):
        all_jobs.extend(fetch_jobs_page(page)['data']['jobs'])

    lst_data = []
    job_links_seen = set()

    for job in all_jobs:
        job_link = job['url']
        if job_link in job_links_seen:
            continue

        cities = []
        for city in job.get('city', []):
            normalized_city = translate_city(city['name'])
            if normalized_city and normalized_city not in cities:
                cities.append(normalized_city)

        if not cities:
            cities = ['Bucuresti']

        presence = job.get('overview', {}).get('Presence', {})
        job_links_seen.add(job_link)
        lst_data.append({
            'job_title': job['title'],
            'job_link': job_link,
            'company': 'RaiffeisenBank',
            'country': 'Romania',
            'city': cities,
            'county': get_county(cities),
            'remote': normalize_remote(presence.get('name')),
        })

    return lst_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'RaiffeisenBank'  # add test comment
    data_list = request_and_collect_data()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('RaiffeisenBank',
                      'https://www.sun-plaza.ro/wp-content/uploads/2016/10/raiffeisen-bank-logo.jpg'
                      ))
