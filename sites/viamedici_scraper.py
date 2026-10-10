#
#
#
# New scraper for -> Viamedici
# Viamedici page -> https://www.viamedici.com/careers/
# (jobs are listed on the softgarden board embedded on that page)
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
from urllib.parse import urljoin
#
import requests
from bs4 import BeautifulSoup
#
from _county import get_county, translate_city


def req_and_collect_data_():
    """
    ... this func() make a simple requests
    and collect data from the Viamedici softgarden job board.
    """

    response = requests.get('https://viamedici.softgarden.io/en/vacancies',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='matchElement')

    lst_with_data = []

    for dt in soup_data:
        title = dt.find('div', class_='matchValue title')
        if not title:
            continue

        title_link = title.find('a')
        if not title_link:
            continue

        location = dt.find('div', class_='matchValue ProjectGeoLocationCity')
        location_text = ''
        if location:
            location_text = ' '.join(el.get_text(strip=True) for el in location.find_all('span', class_='location-view-item'))

        if 'Romania' not in location_text and 'Remote' not in location_text:
            continue

        is_remote = 'Remote' in location_text
        city = translate_city(location_text.replace('Remote', '').split(',')[0].strip())
        county = get_county(city)

        job = {
            "job_title": title_link.get_text(strip=True),
            "job_link": urljoin('https://viamedici.softgarden.io/', title_link.get('href')),
            "company": "Viamedici",
            "country": "Romania",
            "city": city,
            "county": county
        }
        if is_remote:
            job["remote"] = "remote"

        lst_with_data.append(job)

    # for jobs in cities of Romania, 'city' key and also 'remote' key are printed
    tari = ['Iasi', 'Bucuresti', 'Bucharest', 'Cluj']
    filtered_list = [job for job in lst_with_data if any(tara in job.get('city', '') for tara in tari)]

    return filtered_list


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Viamedici'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Viamedici',
                  'https://www.viamedici.com/wp-content/uploads/2024/02/cropped-cropped-Viamedici-Logo-Original-11.png'
                  ))