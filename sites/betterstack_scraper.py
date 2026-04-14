#
#
#
# New scraper for -> BetterStack
# BetterStack page -> https://betterstack.com/careers

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#


def normalize_title(title: str) -> str:
    if title == '/^Full-?stack Engineer$/i':
        return 'Full-stack Engineer'

    return title


def req_and_collect_data_():
    """
    Collect BetterStack jobs from the current careers page.
    """

    response = requests.get('https://betterstack.com/careers',
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('button', attrs={'data-role': True})

    lst_with_data = []
    seen_titles = set()

    for dt in soup_data:
        title_tag = dt.find('p', class_='text-white font-medium text-[15px] leading-[121%] w-full text-start')
        if not title_tag:
            continue

        title = normalize_title(title_tag.text.strip())
        if not title or title in seen_titles:
            continue

        seen_titles.add(title)
        role_slug = dt['data-role']
        lst_with_data.append({
            "job_title": title,
            "job_link": f'https://betterstack.com/careers#{role_slug}',
            "company": "BetterStack",
            "country": "Romania",
            "remote": ["Remote"]
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
    company_name = 'BetterStack'  # add test comment
    data_list = req_and_collect_data_()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('BetterStack',
                      'https://betterstack.com/assets/v2/better-stack-logo-0dd586683a61184ea953948d207470eeec73c76d81d57cd8af24bf56b36a90db.svg'
                      ))
