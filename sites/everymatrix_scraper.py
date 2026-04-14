#
#
#
# New scraper for -> Everymatrix
# Everymatrix page -> https://everymatrix.teamtailor.com/jobs?location=Bucharest&query=

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import requests
from bs4 import BeautifulSoup


BASE_URL = 'https://everymatrix.teamtailor.com'
JOBS_URL = BASE_URL + '/jobs?location=Bucharest&query='


def collect_page_jobs(url):
    """
    Collect Bucharest jobs from one Teamtailor jobs page.
    """

    response = requests.get(url,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()
    response_text = response.text
    soup = BeautifulSoup(response_text, 'lxml')

    lst_with_data = []
    soup_data = soup.select('li.block-grid-item')

    if '/jobs/show_more' in url and soup.find('turbo-stream'):
        template_html = ''.join(template.decode_contents() for template in soup.find_all('template'))
        soup_data = BeautifulSoup(template_html, 'lxml').select('li.block-grid-item')

    for dt in soup_data:
        link_tag = dt.find('a', href=True)
        if not link_tag:
            continue

        href = link_tag['href']
        title_tag = dt.select_one('span.text-block-base-link.company-link-style')
        meta_container = dt.select_one('div.mt-1.text-md')
        if not title_tag:
            continue

        job_title = title_tag.get('title') or title_tag.get_text(strip=True)
        if not job_title:
            continue

        meta_items = []
        if meta_container:
            meta_text = meta_container.get_text(' ', strip=True)
            meta_items = [item.strip() for item in meta_text.split(' · ') if item.strip()]

        city = ''
        remote = ['on-site']

        for item in meta_items:
            if item in {'Hybrid', 'Fully Remote', 'No Remote Work', 'Temporarily Remote'}:
                if item == 'Hybrid':
                    remote = ['Hybrid']
                elif item == 'Fully Remote':
                    remote = ['Remote']
                continue

            if 'Bucharest' in item:
                city = translate_city('Bucharest')

        if not city:
            continue

        lst_with_data.append({
            "job_title": job_title,
            "job_link": href if href.startswith('http') else BASE_URL + href,
            "company": "Everymatrix",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": remote,
        })

    show_more_link = soup.find('a', href=lambda href: href and '/jobs/show_more' in href)
    next_page = None
    if show_more_link and '/jobs/show_more' in show_more_link['href']:
        next_page = show_more_link['href']
        if not next_page.startswith('http'):
            next_page = BASE_URL + next_page

    return lst_with_data, next_page


def req_and_collect_data_():
    """
    Collect all Bucharest jobs from EveryMatrix Teamtailor pages.
    """

    data_list = []
    seen_links = set()
    next_page = JOBS_URL

    while next_page:
        page_jobs, next_page = collect_page_jobs(next_page)
        for job in page_jobs:
            if job['job_link'] in seen_links:
                continue
            seen_links.add(job['job_link'])
            data_list.append(job)

    return data_list


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'Everymatrix'  # add test comment
    data_list = req_and_collect_data_()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Everymatrix',
                      'https://yt3.googleusercontent.com/ytc/APkrFKY4hNjWQM3qepDLxkwrM-YamC-fDU7dKqBTnXt3Gw=s900-c-k-c0x00ffffff-no-rj'
                      ))
