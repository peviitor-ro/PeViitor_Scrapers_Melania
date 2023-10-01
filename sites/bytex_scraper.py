#
#
#
# New scraper for -> Bytex
# Bytex  -> https://bytex.net/careers/

#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def bitex_request_and_collect_data():
    """
    ... this func() make a simple requests
    and collect data from Acronis API.
    """

    response = requests.get('https://bytex.net/careers/#current-openings',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', href=True)

    lst_with_data = []

    for dt in soup_data:

        link = dt['href']
        title = dt.find('h3')
        if title != None:
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title.text,
                "job_link": link,
                "company": "Bytex",
                "country": "Romania",
                "city": "Iasi",
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


company_name = 'Bytex'  # add test comment
data_list = bitex_request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Bytex',
                  'https://seeklogo.com/images/B/bytex-logo-3D33B6EF2A-seeklogo.com.png'
                  ))
