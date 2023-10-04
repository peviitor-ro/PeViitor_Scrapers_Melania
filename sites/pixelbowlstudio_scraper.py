#
#
#
# New scraper for -> PixelBowlStudio
# PixelBowlStudio page -> https://pixelbowlstudio.com/job-opening/

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
    and collect data from PixelBowlStudio API.
    """

    response = requests.get('https://pixelbowlstudio.com/job-opening/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='elementor-cta__content')

    lst_with_data = []

    for dt in soup_data:
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": dt.find('h2',
                                 class_='elementor-cta__title elementor-cta__content-item elementor-content-item elementor-animated-item--grow').text,
            "job_link": dt.find('a', class_='elementor-cta__button elementor-button elementor-size-sm')['href'],
            "company": "PixelBowlStudio",
            "country": "Romania",
            "city": "Bucharest"
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'PixelBowlStudio'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('PixelBowlStudio',
                  'https://pixelbowlstudio.com/wp-content/uploads/2022/11/logo1-1536x331.jpg'
                  ))
