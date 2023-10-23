#
#
#
# New scraper for -> BGS
# BGS page -> https://bgs.ro/recrutare-securitate
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
    and collect data from BGS API.
    """

    response = requests.get('https://bgs.ro/recrutare-securitate',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='col-lg-4 mb-20')

    lst_with_data = []

    for dt in soup_data:
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": dt.find('a', class_='bucata-link-job').text,
            "job_link": dt.find('a', class_='bucata-link-job')['href'],
            "company": "BGS",
            "country": "Romania",
            "city": ""
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'BGS'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('BGS',
                  'https://bgs.ro/image/cachewebp/catalog/logo-400x152.webp'
                  ))
