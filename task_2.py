import requests
from bs4 import BeautifulSoup as bs


def job_scraper(url) -> list[dict]:
    site_data = requests.get(url)
    soup = bs(site_data.text, "html.parser")

    job_boxes = soup.find_all("div", class_="content flex-auto")

    jobs_list = []

    # create a dictionary containing the job title and the job link
    # append the dictionary to the jobs_list list
    for item in job_boxes:
        job_title = item.find("a").text
        job_link = item.find("a")["href"]
        job = {"job_title": job_title, "job_link": job_link}
        jobs_list.append(job)

    return jobs_list


def inspect_jobs(jobs_list: list[dict]):
    # go into the job link and inspect the job description
    for job in jobs_list:
        job_link = job["job_link"]
        job_data = requests.get(job_link)
        job_soup = bs(job_data.text, "html.parser")
        # the summary is has a h6 tag f class m-0
        # the summary is in a div tag with class box-title border-bottom p-3
        job_info_boxes = job_soup.find_all("div", class_="box-body p-3")
        job_description = job_info_boxes[0].text
        job_summary = job_info_boxes[1].text

        # print(job_description)
        # print(job_summary)
        if "The role" in job_summary:
            print("This is a good job")


if __name__ == "__main__":
    scraped_data = job_scraper("https://www.myjobsinkenya.com/")
    job_info = inspect_jobs(scraped_data)
