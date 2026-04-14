#
#
#
# New scraper for -> PhotonEnergyGroup
# PhotonEnergyGroup page -> https://www.photonenergy.ro/current-vacancies
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import requests
from bs4 import BeautifulSoup


BASE_URL = 'https://www.photonenergy.ro'
CAREERS_URL = BASE_URL + '/current-vacancies'


def req_and_collect_data_():
    """
    Collect Romania vacancies from the current Photon Energy careers table.
    """

    response = requests.get(CAREERS_URL,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    lst_with_data = []

    for row in soup.select('table.js-datatables-job tbody tr'):
        cells = row.find_all('td')
        if len(cells) < 4:
            continue

        country = cells[3].get_text(strip=True)
        if country != 'RO':
            continue

        title_tag = cells[0].find('a', href=True)
        city = translate_city(cells[2].get_text(strip=True))

        if not title_tag or not city:
            continue

        job_link = title_tag['href']
        if not job_link.startswith('http'):
            job_link = BASE_URL + job_link

        lst_with_data.append({
            'job_title': title_tag.get_text(strip=True),
            'job_link': job_link,
            'company': 'PhotonEnergyGroup',
            'country': 'Romania',
            'city': city,
            'county': get_county(city),
            'remote': ['on-site']
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'PhotonEnergyGroup'  # add test comment
    data_list = req_and_collect_data_()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('PhotonEnergyGroup',
                      'https://www.photonenergy.com/assets/img/logo-inverse.svg?1696493727'
                      ))
