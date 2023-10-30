#
#
#
# New scraper for -> BDORomania
# BDORomania page -> https://www.bdo.ro/ro-ro/cariere/posturi-libere
#
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
    and collect data from BDO API.
    """

    response = requests.get('https://www.bdo.ro/ro-ro/cariere/posturi-libere',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='SearchResult padded-content border-bottom')

    lst_with_data = []

    for dt in soup_data:
        location = dt.find('div', class_='date').text.strip().split(' ')
        index = location.index('BDO')
        result_location = location[index + 1:]
        while 'BDO' in result_location:
            result_location.remove('BDO')
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": dt.find('span').text,
            "job_link": 'https://www.bdo.ro/' + dt.find('a', class_='url')['href'],
            "company": "BDORomania",
            "country": "Romania",
            "city": ' '.join(result_location)
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'BDORomania'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('BDORomania',
                  'https://www.bdo.ro/bdokit/assets/img/BDO_logo_150dpi_RGB_290709.jpg'
                  ))

