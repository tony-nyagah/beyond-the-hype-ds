import pandas as pd
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

        # add the job summary and job description to the job dictionary
        job["job_summary"] = job_summary
        job["job_description"] = job_description

    return jobs_list


def check_for_keywords(jobs_list: list[dict], keywords: list[str]):
    # check if the job summary or job description contains the keywords
    # if it does, add the job to a new list
    # return the new list
    new_list = []
    for job in jobs_list:
        job_summary = job["job_summary"]
        job_description = job["job_description"]
        for keyword in keywords:
            if keyword in job_summary or keyword in job_description:
                new_list.append(job)
                break

    # turn the list of dictionaries into a pandas dataframe
    # save the dataframe as a csv file
    # only include the job title and the job link
    jobs_df = pd.DataFrame(new_list)
    jobs_df = jobs_df[["job_title", "job_link"]]
    jobs_df.to_csv("jobs.csv", index=False)


if __name__ == "__main__":
    scraped_data = job_scraper("https://www.myjobsinkenya.com/")
    job_info = inspect_jobs(scraped_data)
    keywords = [
        "python",
        "django",
        "flask",
        "data science",
        "data analyst",
        "data science",
        "software",
    ]
    keywords_jobs = check_for_keywords(job_info, keywords)
