#
#
#
# New scraper for -> REEVO
# REEVO page -> https://reevotech.com/careers/

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import requests
from bs4 import BeautifulSoup


CAREERS_URL = 'https://reevotech.com/careers/'


def normalize_location(location_text):
    """
    Normalize the REEVO location label to city and remote fields.
    """

    location_text = location_text.strip()
    location_lower = location_text.lower()

    if location_lower == 'remote':
        return None, None, ['Remote']

    if 'hybrid' in location_lower:
        city_name = location_text.split('(')[0].strip()
        city = translate_city(city_name)
        if city:
            return city, get_county(city), ['Hybrid']

    city = translate_city(location_text)
    if city:
        return city, get_county(city), ['on-site']

    return None, None, ['on-site']


def req_and_collect_data_():
    """
    Collect current REEVO jobs from the careers page.
    """

    response = requests.get(CAREERS_URL,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    lst_with_data = []

    for dt in soup.select('a.awsm-job-item'):
        title_tag = dt.select_one('h2.awsm-job-post-title')
        location_tag = dt.select_one('.awsm-job-specification-job-location .awsm-job-specification-term')

        if not title_tag or not location_tag:
            continue

        city, county, remote = normalize_location(location_tag.get_text(strip=True))
        job_data = {
            'job_title': title_tag.get_text(strip=True),
            'job_link': dt['href'],
            'company': 'REEVO',
            'country': 'Romania',
            'remote': remote
        }

        if city:
            job_data['city'] = city
            job_data['county'] = county

        lst_with_data.append(job_data)

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'REEVO'  # add test comment
    data_list = req_and_collect_data_()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('REEVO',
                      'https://reevotech.com/wp-content/uploads/2023/06/cropped-REEVO_LogotypeMonogram_Red_RGB.png'
                      ))
