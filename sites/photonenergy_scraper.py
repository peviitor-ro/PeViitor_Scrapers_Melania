#
#
#
# New scraper for -> PhotonEnergyGroup
# PhotonEnergyGroup page -> https://www.photonenergy.com/en/career.html
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def req_and_collect_data_():
    """
    ... this func() make a simple requests
    and collect data from PhotonEnergyGroup API.
    """

    response = requests.get('https://www.photonenergy.com/en/career.html',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', class_='c-news__item')

    lst_with_data = []

    for dt in soup_data:
        location = dt.find('p', class_='u-color-grey-7 mb-0').text

        if 'romania' in location.lower():
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": dt.find('h2', class_='h4').text,
                "job_link": 'https://www.photonenergy.com/' + dt['href'],
                "company": "PhotonEnergyGroup",
                "country": "Romania",
                "city": location.split(', ')[0].split(' ')[0]
            })

        if 'remote' == location.lower():
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": dt.find('h2', class_='h4').text,
                "job_link": 'https://www.photonenergy.com/' + dt['href'],
                "company": "PhotonEnergyGroup",
                "country": "Romania",
                "remote": "remote",
                "city": " ",
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'PhotonEnergyGroup'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('PhotonEnergyGroup',
                  'https://www.photonenergy.com/assets/img/logo-inverse.svg?1696493727'
                  ))
