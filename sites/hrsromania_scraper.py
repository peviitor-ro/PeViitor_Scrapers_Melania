#
#
#
#
#
# New scraper for -> HRSRomania
# HRSRomania page -> https://www.hrsro.com/job-listings
#
#
import requests
from bs4 import BeautifulSoup

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city


BASE_URL = 'https://www.hrsro.com'
LISTINGS_URL = BASE_URL + '/job-listings'
PAGINATION_PARAM = '1dd5eb8c_page'


def parse_remote(remote_text):
    remote_text = remote_text.strip().lower()

    if remote_text == 'remote':
        return ['Remote']
    if remote_text == 'hybrid':
        return ['Hybrid']

    return ['on-site']


def extract_detail_data(job_link):
    """
    Extract locations and remote mode from the job detail page.
    """

    response = requests.get(job_link,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    filters = soup.select('div.job-offer__left-description.hidden-tablet-below div.job-offer-description__filters')
    remote = ['on-site']

    for filter_block in filters:
        parts = [div.get_text(' ', strip=True) for div in filter_block.find_all('div', recursive=False)]
        if len(parts) < 2:
            continue

        if parts[0] == 'Работа от вкъщи':
            remote = parse_remote(parts[1])
            break

    location_collections = []
    for collection_name in ['Location', 'Location-two', 'Location-three', 'Location-four']:
        for collection in soup.find_all(attrs={'fs-cmsnest-collection': collection_name}):
            for city_tag in collection.select('div.p-body'):
                city = translate_city(city_tag.get_text(strip=True))
                if city and city not in location_collections:
                    location_collections.append(city)

    return location_collections, remote


def collect_page_jobs(page):
    """
    Collect jobs from one HRS listings page.
    """

    params = None if page == 1 else {PAGINATION_PARAM: page}
    response = requests.get(LISTINGS_URL,
                            headers=DEFAULT_HEADERS,
                            params=params,
                            timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = []

    for job_card in soup.select('div.job-listing__item'):
        title_tag = job_card.select_one('h2[fs-cmsfilter-field="Position"]')
        link_tag = job_card.select_one('a.link-block[href]')

        if not title_tag or not link_tag:
            continue

        job_link = link_tag['href']
        if not job_link.startswith('http'):
            job_link = BASE_URL + job_link

        cities, remote = extract_detail_data(job_link)
        if not cities:
            cities = ['Bucuresti']

        jobs.append({
            'job_title': title_tag.get_text(strip=True),
            'job_link': job_link,
            'company': 'HRSRomania',
            'country': 'Romania',
            'city': cities,
            'county': get_county(cities),
            'remote': remote
        })

    return jobs


def collect_data_hrs():
    """
    Collect all current HRS Romania jobs from the new listings pages.
    """

    jobs = []
    seen_links = set()
    page = 1

    while True:
        page_jobs = collect_page_jobs(page)
        if not page_jobs:
            break

        for job in page_jobs:
            if job['job_link'] in seen_links:
                continue
            seen_links.add(job['job_link'])
            jobs.append(job)

        page += 1

    return jobs


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'HRSRomania'  # add test comment
    data_list = collect_data_hrs()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('HRSRomania',
                      'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiTHQGg18vALX40onszHcHnc5kjPgPxtAKtHMMbN-uXQ&s'
                      ))
