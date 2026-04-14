#
#
#
#
# New scraper for -> vidaXL
# vidaXL job page -> https://careers.vidaxl.com/vacancies/country/romania
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
#
import requests
from bs4 import BeautifulSoup


CAREERS_URL = 'https://careers.vidaxl.com/vacancies/country/romania'


def request_and_collect_data():
    """
    Collect current Romania jobs from the vidaXL careers page.
    """

    response = requests.get(url=CAREERS_URL,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    lst_with_data = []

    for job in soup.select('[data-vacancy-id]'):
        title_tag = job.select_one('a[href]')
        if not title_tag:
            continue

        lst_with_data.append({
            'job_title': title_tag.get_text(strip=True),
            'job_link': 'https://careers.vidaxl.com' + title_tag['href'],
            'company': 'vidaXL',
            'country': 'Romania',
            'city': 'Bucuresti',
            'county': 'Bucuresti',
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
    company_name = 'vidaXL'  # add test comment
    data_list = request_and_collect_data()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('vidaXL',
                      'https://careers.vidaxl.com/uploads/vidaXL_purple_111x51px-02.svg'
                      ))
