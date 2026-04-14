#
#
#
# New scraper for -> Webmarc
# Webmarc page -> https://webmarc.io/hiring
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup


CAREERS_URL = 'https://webmarc.io/hiring'


def req_and_collect_data_():
    """
    Collect current jobs from the Webmarc hiring page.
    """

    response = requests.get(CAREERS_URL,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    lst_with_data = []

    for dt in soup.select('div.jobcard_job-card-wrapper__TqKvb'):
        title_tag = dt.select_one('p.jobcard_job-card-title__mElbr')
        location_tag = dt.select_one('p.jobcard_job-card-subtitle__Yx_4O')
        card_id = dt.get('id')

        if not title_tag or not location_tag or not card_id:
            continue

        location_text = location_tag.get_text(strip=True)
        remote = ['Hybrid'] if 'Hybrid' in location_text else ['on-site']

        lst_with_data.append({
            'job_title': title_tag.get_text(strip=True),
            'job_link': f'{CAREERS_URL}#{card_id}',
            'company': 'Webmarc',
            'country': 'Romania',
            'city': 'Bucuresti',
            'county': 'Bucuresti',
            'remote': remote
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
    company_name = 'Webmarc'  # add test comment
    data_list = req_and_collect_data_()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Webmarc',
                      'https://webmarc.io/assets/icons/linkedin.svg'
                      ))
