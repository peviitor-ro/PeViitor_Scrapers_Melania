#
#
#
# New scraper for -> PixelBowlStudio
# PixelBowlStudio page -> https://pixelbowlstudio.com/job-opening/
# Jobs are published as individual pages listed in the sitemap:
# https://pixelbowlstudio.com/page-sitemap.xml

#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import re

import requests
from bs4 import BeautifulSoup
#

SITEMAP_URL = 'https://pixelbowlstudio.com/page-sitemap.xml'


def req_and_collect_data_():
    """
    ... this func() makes simple requests
    and collects data from PixelBowlStudio job pages.
    """

    response = requests.get(SITEMAP_URL, headers=DEFAULT_HEADERS)
    page_urls = re.findall(r'<loc><!\[CDATA\[([^\]]+)\]\]></loc>',
                           response.text)

    lst_with_data = []

    for page_url in page_urls:
        page_response = requests.get(page_url, headers=DEFAULT_HEADERS)
        page_soup = BeautifulSoup(page_response.text, 'lxml')

        title = page_soup.find('h1',
                               class_='elementor-heading-title')
        location = page_soup.find('h5',
                                  class_='elementor-heading-title')

        if not title or not location:
            continue

        lst_with_data.append({
            "job_title": title.get_text(strip=True),
            "job_link": page_url,
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