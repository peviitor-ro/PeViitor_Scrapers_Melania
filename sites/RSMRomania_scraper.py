#
#
#
# New scraper for -> RSMRomania
# RSMRomania page -> https://www.rsm.global/romania/ro/campaign/joburi-disponibile
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
    and collect data from RSMRomania API.
    """

    response = requests.get('https://www.rsm.global/romania/ro/campaign/joburi-disponibile',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='d-lg-flex')

    lst_with_data = []

    for dt in soup_data:
        link = dt.find('a', class_='tab-button col-12 col-lg-11 py-4 px-3')['href']
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": dt.find('h2', class_='tab-pane--title').text,
            "job_link": 'https://www.rsm.global/' + link,
            "company": "RSMRomania",
            "country": "Romania",
            "city": "Bucuresti"
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'RSMRomania'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('RSMRomania',
                  'https://res.cloudinary.com/rsmglobal/image/fetch/t_default/f_auto/q_auto/https://www.rsm.global/romania/profiles/rsm_global_platform/themes/rsm_global_platform_2022/images/logo@2x.png'
                  ))
