#
#
#
#
# New scraper for -> Accessgroup
# Accessgroup page -> https://theaccessgroup.wd103.myworkdayjobs.com/Access_Group_External_Careers
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import requests


WORKDAY_URL = 'https://theaccessgroup.wd103.myworkdayjobs.com/wday/cxs/theaccessgroup/Access_Group_External_Careers/jobs'
WORKDAY_REFERER = 'https://theaccessgroup.wd103.myworkdayjobs.com/Access_Group_External_Careers'
ROMANIA_LOCATION_SLUGS = {
    'Timisoara': 'Timisoara',
    'Romania-Remote': '',
    'Romania-Home': ''
}


def custom_headers() -> dict:
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'https://theaccessgroup.wd103.myworkdayjobs.com',
        'Referer': WORKDAY_REFERER,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }


def get_city_and_remote(external_path: str) -> tuple[str, list[str]]:
    location_slug = external_path.split('/job/')[1].split('/')[0]
    city = ROMANIA_LOCATION_SLUGS.get(location_slug, '')

    if 'Remote' in location_slug or 'Home' in location_slug:
        return city, ['Remote']

    return city, ['on-site']


def collect_data_from_site(offset: int) -> tuple[list, int]:
    """
    Collect Romania jobs from Access Group Workday API.
    """

    response = requests.post(
        url=WORKDAY_URL,
        headers=custom_headers(),
        json={
            'appliedFacets': {
                'locationCountry': ['f2e609fe92974a55a05fc1cdc2852122']
            },
            'limit': 20,
            'offset': offset,
            'searchText': ''
        },
        timeout=30)
    response.raise_for_status()

    data_jobs = response.json()['jobPostings']
    lst_with_data = []

    for job in data_jobs:
        external_path = job['externalPath']
        location_slug = external_path.split('/job/')[1].split('/')[0]

        if location_slug not in ROMANIA_LOCATION_SLUGS:
            continue

        city, remote = get_city_and_remote(external_path)
        city = translate_city(city)

        lst_with_data.append({
            "job_title": job['title'],
            "job_link": 'https://theaccessgroup.wd103.myworkdayjobs.com/en-US/Access_Group_External_Careers' + external_path,
            "company": "Accessgroup",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": remote
        })

    return lst_with_data, len(data_jobs)


def scrape_all_data_from_() -> list:
    """
    Scrap all Romania data and return big list.
    """

    offset = 0
    big_lst_jobs = []

    while True:
        data_site, raw_jobs_count = collect_data_from_site(offset)

        if data_site:
            big_lst_jobs.extend(data_site)

        if raw_jobs_count < 20:
            break

        offset += 20

    return big_lst_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'Accessgroup'  # add test comment
    data_list = scrape_all_data_from_()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Accessgroup',
                      'https://seeklogo.com/images/T/the-access-group-logo-3BF0ABEC34-seeklogo.com.png'
                      ))
