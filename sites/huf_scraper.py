#
#
#
# New scraper for -> Huf
# Huf page -> https://jobs.huf-group.com/search/
# (portalul oficial de joburi Huf; vechea pagina www.huf-group.com/en/career/job-vacancies
#  nu mai este accesibila)
#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
import urllib3
from bs4 import BeautifulSoup
#
from _county import get_county, translate_city

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = 'https://jobs.huf-group.com'
JOBS_PAGE_URL = BASE_URL + '/search/?q=&pageNumber={page_number}'
REQUEST_TIMEOUT = 30
MAX_PAGES = 20
# codul de tara / denumirea din listele de joburi (ex: "Huf Romania, Arad, ..., RO")
ROMANIA_TAGS = ('ro', 'romania', 'rumänien')


def is_romania_location(location):
    """
    ... verifica daca locatia jobului este in Romania
    """

    parts = [part.strip() for part in location.split(',') if part.strip()]

    if any(part.lower() in ROMANIA_TAGS for part in parts):
        return True

    return any(tag in location.lower() for tag in ('romania', 'rumänien'))


def extract_city(location):
    """
    ... extrage orasul din locatie (ex: "Huf Romania, Arad, Huf Romania, Arad, RO")
    """

    parts = [part.strip() for part in location.split(',') if part.strip()]

    for part in parts:
        if re.fullmatch(r'[A-Z]{2,3}', part):
            continue

        if get_county(part):
            return part

    for part in parts:
        if re.fullmatch(r'[A-Z]{2,3}', part) or 'huf' in part.lower():
            continue

        return part

    return None


def get_rows_from_page(page_number):
    """
    ... ia pagina de joburi si returneaza randurile cu joburi
    """

    response = requests.get(
        JOBS_PAGE_URL.format(page_number=page_number),
        headers=DEFAULT_HEADERS,
        timeout=REQUEST_TIMEOUT,
        verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    return soup.select('table#searchresults tr.data-row')


def req_and_collect_data_huf():
    """
    ... this func() make a simple requests
    and collect data from Huf careers portal.
    """

    lst_with_data = []
    seen_links = set()

    for page_number in range(1, MAX_PAGES + 1):
        try:
            soup_data = get_rows_from_page(page_number)
        except requests.exceptions.RequestException as error:
            print(f'Huf jobs page not available: {error}')
            break

        if not soup_data:
            break

        for dt in soup_data:
            title_link = dt.select_one('a.jobTitle-link')
            location_node = dt.select_one('td.colLocation span.jobLocation')

            if not title_link:
                continue

            title = title_link.get_text(strip=True)
            link = title_link.get('href', '')
            location = location_node.get_text(' ', strip=True) if location_node else ''

            if not link or link in seen_links:
                continue

            seen_links.add(link)

            if not is_romania_location(location):
                continue

            city_name = extract_city(location)

            if not city_name:
                continue

            city = translate_city(city_name)
            county = get_county(city)

            lst_with_data.append({
                "job_title": title,
                "job_link": BASE_URL + link if link.startswith('/') else link,
                "company": "Huf",
                "country": "Romania",
                "city": city,
                "county": county
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Huf'  # add test comment
data_list = req_and_collect_data_huf()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Huf',
                  'https://upload.wikimedia.org/wikipedia/commons/0/09/Huf_Group_Logo_RGB_2020.svg'
                  ))
