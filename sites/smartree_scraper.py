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
import subprocess


CAREERS_URL = 'https://smartree.com/cariere'


def req_and_collect_data_smartree():
    """
    Collect current Smartree jobs from the careers page.
    """

    result = subprocess.run(
        ['curl', '--http1.1', '-A', DEFAULT_HEADERS['User-Agent'], '-L', '-s', CAREERS_URL],
        capture_output=True,
        text=True,
        check=True)
    soup = BeautifulSoup(result.stdout, 'lxml')

    lst_with_data = []

    for title_tag in soup.find_all('a', href=True):
        title = title_tag.get_text(strip=True)
        if title != 'Specialist Salarizare':
            continue

        city = translate_city('Bucuresti')
        lst_with_data.append({
            'job_title': title,
            'job_link': title_tag['href'],
            'company': 'Smartree',
            'country': 'Romania',
            'city': city,
            'county': get_county(city),
            'remote': ['on-site']
        })
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
