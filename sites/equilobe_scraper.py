#
#
#
# New scraper for -> Equilobe
# Equilobe page -> https://www.equilobe.com/new-openings

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county
#
import requests
from bs4 import BeautifulSoup


def req_and_collect_data_equilobe():
    """
    Collect current Equilobe openings from the careers page.
    """

    response = requests.get('https://www.equilobe.com/new-openings',
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    soup = BeautifulSoup(response.text, 'lxml')

    lst_with_data = []
    seen_links = set()

    for link_tag in soup.find_all('a', href=True):
        link = link_tag['href']

        if '/new-openings/' not in link or link.rstrip('/') == 'https://www.equilobe.com/new-openings':
            continue

        if link in seen_links:
            continue

        title_tag = link_tag.find_previous(['h1', 'h2', 'h3'])
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        if not title:
            continue

        seen_links.add(link)
        lst_with_data.append({
            "job_title": title,
            "job_link": link,
            "company": "Equilobe",
            "country": "Romania",
            "city": "Bucuresti",
            "county": get_county('Bucuresti'),
            "remote": ["on-site"]
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'Equilobe'  # add test comment
    data_list = req_and_collect_data_equilobe()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Equilobe',
                      'https://static.wixstatic.com/media/e97736_955059ac6cc24e819aead464d7cc24be~mv2.png/v1/fit/w_2500,h_1330,al_c/e97736_955059ac6cc24e819aead464d7cc24be~mv2.png'
                      ))
