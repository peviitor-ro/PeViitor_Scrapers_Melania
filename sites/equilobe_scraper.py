#
#
#
# New scraper for -> Equilobe
# Equilobe page -> https://www.equilobe.com/new-openings
# equilobe.com now redirects to Zitec's careers site -> https://careers.makeit.software/jobs

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import requests
from bs4 import BeautifulSoup


BASE_URL = 'https://careers.makeit.software'
JOBS_URL = BASE_URL + '/jobs'


def make_request(url):
    """
    Fetch a page, retrying a few times before giving up.
    """

    for attempt in range(3):
        try:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            if attempt == 2:
                return None

    return None


def collect_jobs_from_page(url):
    """
    Collect jobs from one Teamtailor jobs page.
    """

    response = make_request(url)
    if response is None:
        return [], None

    soup = BeautifulSoup(response.text, 'lxml')

    cards = soup.select('li.block-grid-item')

    if '/jobs/show_more' in url and soup.find('turbo-stream'):
        template_html = ''.join(template.decode_contents() for template in soup.find_all('template'))
        cards = BeautifulSoup(template_html, 'lxml').select('li.block-grid-item')

    page_jobs = []

    for card in cards:
        link_tag = card.find('a', href=True)
        if not link_tag:
            continue

        link = link_tag['href']
        if link.startswith('/'):
            link = BASE_URL + link

        title_tag = card.select_one('span.text-block-base-link.company-link-style')
        if not title_tag:
            continue

        job_title = title_tag.get('title') or title_tag.get_text(strip=True)
        if not job_title:
            continue

        meta_container = card.select_one('div[class*="text-md"]')
        location = meta_container.get_text(' ', strip=True) if meta_container else ''

        remote = ['on-site']
        if 'remote' in location.lower():
            remote = ['Remote']

        job_data = {
            "job_title": job_title,
            "job_link": link,
            "company": "Equilobe",
            "country": "Romania",
            "remote": remote,
        }

        if 'bucharest' in location.lower():
            city = translate_city('Bucharest')
            job_data['city'] = city
            job_data['county'] = get_county(city)

        page_jobs.append(job_data)

    next_page = None
    show_more_link = soup.find('a', href=lambda href: href and '/jobs/show_more' in href)
    if show_more_link:
        next_page = show_more_link['href']
        if not next_page.startswith('http'):
            next_page = BASE_URL + next_page

    return page_jobs, next_page


def req_and_collect_data_equilobe():
    """
    Collect current Equilobe openings from the careers page.
    """

    lst_with_data = []
    seen_links = set()
    next_page = JOBS_URL

    while next_page:
        page_jobs, next_page = collect_jobs_from_page(next_page)
        for job in page_jobs:
            if job['job_link'] in seen_links:
                continue
            seen_links.add(job['job_link'])
            lst_with_data.append(job)

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'Equilobe'  # add test comment
    data_list = req_and_collect_data_equilobe()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Equilobe',
                      'https://static.wixstatic.com/media/e97736_955059ac6cc24e819aead464d7cc24be~mv2.png/v1/fit/w_2500,h_1330,al_c/e97736_955059ac6cc24e819aead464d7cc24be~mv2.png'
                      ))
