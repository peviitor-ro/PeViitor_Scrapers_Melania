#
#
#
# New scraper for -> Moonstar
# Moonstar page -> https://moonstar.ai/careers/
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
    and collect data from Moonstar API.
    """

    response = requests.get('https://moonstar.ai/careers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='list_item lists_3 clearfix')

    lst_with_data = []

    for dt in soup_data:
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": dt.find('h4').text,
            "job_link": dt.find('a')['href'],
            "company": "Moonstar",
            "country": "Romania",
            "remote": "remote"
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Moonstar'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Moonstar',
                  'https://images.crunchbase.com/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/ktkt3kraqzveu9rmdrrk'
                  ))
