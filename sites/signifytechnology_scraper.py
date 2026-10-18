#
#
#
# New scraper for -> Signifytechnology
# Signifytechnology page -> https://www.signifytechnology.com/jobs

#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
from _county import get_county, translate_city
#
import time
from random import randint


SEARCH_URL = 'https://www.signifytechnology.com/_sf/api/v1/jobs/search.json'
BASE_URL = 'https://www.signifytechnology.com'
JOBS_PER_PAGE = 50


def collect_data_from_site(page: int) -> list:
    """
    Collect all data from site.
    """

    payload = {
        "job_search": {
            "query": "",
            "location": {},
            "filters": {},
            "commute_filter": {},
            "offset": (page - 1) * JOBS_PER_PAGE,
            "jobs_per_page": JOBS_PER_PAGE
        }
    }

    response = requests.post(
        url=SEARCH_URL,
        json=payload,
        headers=DEFAULT_HEADERS)

    if response.status_code != 200:
        return []

    data_jobs = response.json().get('results', [])

    lst_with_data = []

    for dt in data_jobs:
        job = dt.get('job', {})
        title = (job.get('title') or '').strip()
        slug = job.get('url_slug') or ''

        addresses = job.get('addresses') or []
        location = addresses[0] if addresses else (job.get('original_location') or '')
        city = translate_city(location.split(',')[0].strip())
        county = get_county(city)

        if not title or not slug:
            continue

        lst_with_data.append({
            "job_title": title,
            "job_link": f'{BASE_URL}/jobs/{slug}',
            "company": "Signifytechnology",
            "country": "Romania",
            "city": city,
            "county": county
        })

    for job in lst_with_data:
        if job['city'] == 'Sector 1':
            job['city'] = 'Bucuresti'

    return lst_with_data


def scrape_all_data_from_() -> list:
    """
    Scrap all data from , and return big list.
    """

    page = 1
    flag = True

    big_lst_jobs = []
    while flag:

        # collect data from site!
        data_site = collect_data_from_site(page)

        if data_site:
            big_lst_jobs.extend(data_site)

        else:
            flag = False

        page += 1
        time.sleep(randint(1, 2))

    return big_lst_jobs


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Signifytechnology'
data_list = scrape_all_data_from_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Signifytechnology',
                  'https://www.signifytechnology.com/logo/signify-logo.png'
                  ))
