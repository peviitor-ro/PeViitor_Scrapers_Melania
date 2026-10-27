#
#
#
# New scraper for -> Mondly
# Mondly page -> https://www.mondly.com/careers

#

from urllib.parse import urljoin

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo

import json

import requests
from bs4 import BeautifulSoup

from _county import get_county, translate_city


CAREERS_URL = 'https://www.mondly.com/careers'
DEFAULT_LOCATION = 'Brasov, Romania'


def _build_job(title, link, location):
    city = translate_city(location.split(',')[0].strip())
    county = get_county(city)

    return {
        "job_title": title,
        "job_link": link,
        "company": "Mondly",
        "country": "Romania",
        "city": city,
        "county": county
    }


def _job_link(job):
    link = job.get('pearsonURL') or job.get('pearsonUrl') or job.get('url')

    if link:
        return urljoin(CAREERS_URL, link)

    slug = job.get('slug')
    if slug:
        return urljoin(CAREERS_URL + '/', slug)

    return CAREERS_URL


def _jobs_from_page_data(soup):
    script = soup.find('script', id='__NEXT_DATA__')
    if script is None:
        return None

    try:
        page_data = json.loads(script.string or script.get_text())
    except (TypeError, json.JSONDecodeError):
        return None

    jobs = page_data.get('props', {}).get('pageProps', {}).get('jobs')
    if not isinstance(jobs, list):
        return None

    lst_with_data = []
    for job in jobs:
        if not isinstance(job, dict):
            continue

        title = (job.get('title') or '').strip()
        if not title:
            continue

        location = job.get('location') or DEFAULT_LOCATION
        lst_with_data.append(_build_job(title, _job_link(job), location))

    return lst_with_data


def _jobs_from_cards(soup):
    soup_data = soup.find_all(
        'a', class_='flex flex-col p-6 rounded-3lg shadow-5md bg-white')

    lst_with_data = []
    for dt in soup_data:
        location_tag = dt.find(
            'div', class_='text-2lg font-normal tracking-2small font-sans')
        title_tag = dt.find(
            'div', class_='text-mondly-darker-blue text-2xl font-medium underline font-sans')
        link = dt.get('href')

        if location_tag is None or title_tag is None or not link:
            continue

        location = location_tag.text.split(':', 1)[-1].strip()
        lst_with_data.append(
            _build_job(title_tag.text.strip(), urljoin(CAREERS_URL, link), location))

    return lst_with_data


def req_and_collect_data_():
    """
    ... this func() make a simple requests
    and collect data from Mondly careers page.
    """

    response = requests.get(CAREERS_URL, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = _jobs_from_page_data(soup)
    if jobs is not None:
        return jobs

    return _jobs_from_cards(soup)

# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Mondly'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Mondly',
                  'https://edge.mondly.com/blog/wp-content/themes/mondly/img/logo.svg.gzip'
                  ))
