#
#
#
# New scraper for -> LucaNet
# LucaNet page -> https://www.lucanet.com/en/careers/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#


def request_and_collect_data():
    """
    Collect Romania jobs from the LucaNet Greenhouse board.
    """

    response = requests.get(
        url='https://job-boards.eu.greenhouse.io/embed/job_board'
            '?for=lucanetgroup&_data=routes%2Fembed.job_board',
        headers=DEFAULT_HEADERS).json()['jobPosts']['data']

    lst_with_data = []

    for job in response:
        location = str(job.get('location') or '').lower()
        if not any(city in location for city in ('romania', 'bucure', 'bucharest')):
            continue

        link = job['absolute_url']
        title = job['title']

        lst_with_data.append({
            "job_title": title,
            "job_link": link,
            "company": "LucaNet",
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


if __name__ == '__main__':
    company_name = 'LucaNet'  # add test comment
    data_list = request_and_collect_data()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('LucaNet',
                      'https://www.lucanet.com/fileadmin/user_upload/Images_and_Graphics/Logos/LucaNet/logo-lucanet-ohne-claim-2020-rgb.png'
                      ))
