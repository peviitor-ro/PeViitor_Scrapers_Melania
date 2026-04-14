#
#
#
# New scraper for -> LucaNet
# LucaNet page -> https://jobs.lucanet.com/job-list/?office=Romania
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
        url=' https://job-boards.eu.greenhouse.io/embed/job_board?for=lucanetgroup&validityToken=kKTGIxXexN70T3-wgwzogB5kausGvMv_vLPSAgCpxwNlf7B6349E8CaY1eetMfffiultyzu5cGe3yoBB8ThHznchJ-qJ3IVFNHQ7tRQxZOa8WN5s05jGIF2RySbogvxvHq8TmU8sz1EmKX3UgwGct0_uEwSC24cA9NDz-CmVMe1EdcC_yuhbqWzO-Ys70HZnBfmp3Ao0CZFKNTzTtXmS07XccNWw74w5QMiswLnqwQw_rPJcPL-SF0MZenvXf5lmw3mB-GVRYZrWOdSJpUMhOq6vbueM0VMnF2c_6o0LJ-bJBQkQJxvzpzw-GFiOTLTeRgCcTSkPEg7HOQjwh1rhnw%3D%3D&offices%5B%5D=4015222101&_data=routes%2Fembed.job_board',
        headers=DEFAULT_HEADERS).json()['jobPosts']['data']

    lst_with_data = []

    for job in response:
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
