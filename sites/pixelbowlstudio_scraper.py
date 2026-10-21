#
#
#
# New scraper for -> PixelBowlStudio
# PixelBowlStudio page -> https://pixelbowlstudio.com/careers/
# (old /job-opening/ page redirects to /careers/)
# Jobs are listed in the "open positions" accordion on the careers page.

#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#

import requests
from bs4 import BeautifulSoup
#

CAREERS_URL = 'https://pixelbowlstudio.com/careers/'


def req_and_collect_data_():
    """
    ... this func() makes simple requests
    and collects data from PixelBowlStudio job pages.
    """

    response = requests.get(CAREERS_URL, headers=DEFAULT_HEADERS)
    page_soup = BeautifulSoup(response.text, 'lxml')

    open_positions = page_soup.find(id='open-positions')
    if not open_positions:
        return []

    lst_with_data = []

    for item in open_positions.find_all('div', class_='accordion-item'):
        title = item.find('button', class_='accordion-button')
        if not title:
            continue

        header = item.find('h2', class_='accordion-header')
        anchor = header.get('id') if header else None
        job_link = f"{CAREERS_URL}#{anchor}" if anchor else CAREERS_URL

        lst_with_data.append({
            "job_title": title.get_text(strip=True),
            "job_link": job_link,
            "company": "PixelBowlStudio",
            "country": "Romania",
            "city": "Bucuresti",
            "county": "Bucuresti"
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
