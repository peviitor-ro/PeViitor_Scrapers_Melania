#
#
#
# New scraper for -> Smartree
# Smartree page -> https://www.smartree.com/cariere

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import subprocess


CAREERS_URL = 'https://smartree.com/cariere'
TRANSLATED_CAREERS_URL = (
    'https://smartree-com.translate.goog/cariere/'
    '?_x_tr_sl=ro&_x_tr_tl=en&_x_tr_hl=en-US'
)
JOB_SELECTOR = 'div.master-image-box h3.headline-2 a[href*="/cariere/"]'


def fetch_html(url):
    result = subprocess.run(
        ['curl', '--http1.1', '-A', DEFAULT_HEADERS['User-Agent'], '-L', '-s',
         '--retry', '3', '--retry-delay', '2', '--retry-all-errors', url],
        capture_output=True,
        text=True,
        check=True)
    return result.stdout


def canonical_job_link(href):
    parsed = urlsplit(href)
    if parsed.hostname and parsed.hostname.endswith('.translate.goog'):
        return f'https://smartree.com{parsed.path}'
    return href


def req_and_collect_data_smartree():
    """
    Collect current Smartree jobs from the careers page.
    """

    lst_with_data = []

    for url in (CAREERS_URL, TRANSLATED_CAREERS_URL):
        soup = BeautifulSoup(fetch_html(url), 'lxml')

        for job_box in soup.select(JOB_SELECTOR):
            title = job_box.get_text(strip=True)
            city = translate_city('Bucuresti')
            lst_with_data.append({
                'job_title': title,
                'job_link': canonical_job_link(job_box['href']),
                'company': 'Smartree',
                'country': 'Romania',
                'city': city,
                'county': get_county(city),
                'remote': ['on-site']
            })

        if lst_with_data:
            break

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'Smartree'  # add test comment
    data_list = req_and_collect_data_smartree()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Smartree',
                      'https://www.smartree.com/pages/tpl/front/assets/images/logo-new.png'
                      ))
