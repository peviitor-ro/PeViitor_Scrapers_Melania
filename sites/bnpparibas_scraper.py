#
#
#
# New scraper for -> BNPParibas
# BNPParibas page -> https://group.bnpparibas/en/careers
#
from bs4 import BeautifulSoup

from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
import subprocess
#
from _county import get_county, translate_city
#
import time
from random import randint
from math import ceil
from urllib.parse import urljoin

JOBS_URL = 'https://group.bnpparibas/en/careers/all-job-offers/roumanie'

# The careers site sits behind Akamai and rejects the TLS fingerprint of
# python-requests with 403, so pages are fetched with curl and browser-like
# headers (this is the same approach used by raiffeisenbank_scraper.py).
CURL_ARGS = [
    'curl', '-s', '--compressed', '-L', '--max-time', '60',
    '-A', 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    '-H', 'Accept-Language: en-US,en;q=0.9',
]


def fetch_page_html(page: int) -> str:
    """
    Fetch one page of job offers, retrying with backoff while the
    site temporarily rate-limits the client.
    """

    command = CURL_ARGS + [f'{JOBS_URL}?page={page}']

    for attempt in range(6):
        try:
            result = subprocess.run(command, capture_output=True,
                                    text=True, timeout=70)
        except subprocess.TimeoutExpired:
            result = None

        html = result.stdout if result else ''
        if result and result.returncode == 0 \
                and 'Access Denied' not in html \
                and len(html.strip()) > 1000:
            return html

        # blocked or failed: wait for the rate limit to cool down
        time.sleep(15 * (attempt + 1))

    raise RuntimeError(f'Could not fetch page {page} from the BNPParibas careers site.')


def extract_jobs_from_soup(soup):
    """
    Extract the job offers from one listing page.
    """

    data_jobs = soup.find_all('a', class_='card-link')

    lst_with_data = []
    for dt in data_jobs:
        location = dt.find('div', class_='offer-location')
        title = dt.find('h3', class_='title-4')

        if title and location:
            link = dt['href']
            city = translate_city(location.text.split(',')[0].strip())
            county = get_county(city)

            lst_with_data.append({
                "job_title": title.text.strip(),
                "job_link": urljoin('https://group.bnpparibas/', link),
                "company": "BNPParibas",
                "country": "Romania",
                "city": city,
                "county": county
            })

    return lst_with_data


def collect_data_from_site(page: int):
    """
    Collect all data from site.
    """

    soup = BeautifulSoup(fetch_page_html(page), 'lxml')

    return extract_jobs_from_soup(soup)


def scrape_all_data_from_():
    """
    Scrap all data from , and return big list.
    """

    soup = BeautifulSoup(fetch_page_html(1), 'lxml')
    try:
        pages = soup.find('span', class_='nb-total spanGreen').text

        pege_count = ceil(int(pages) / 10)
    except Exception as e:
        pege_count = 1

    big_lst_jobs = extract_jobs_from_soup(soup)

    for page in range(2, pege_count + 1):

        # collect data from site!
        data_site = collect_data_from_site(page)

        big_lst_jobs.extend(data_site)

        time.sleep(randint(5, 10))

    return big_lst_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'BNPParibas'
data_list = scrape_all_data_from_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('BNPParibas',
                  'https://logos-world.net/wp-content/uploads/2021/02/BNP-Paribas-Logo-700x394.png'
                  ))
