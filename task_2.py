import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


def scrape_job_links(url):
    try:
        site_data = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return []

    soup = bs(site_data.text, "html.parser")

    job_boxes = soup.find_all("div", class_="content flex-auto")

    jobs_list = []

    for item in job_boxes:
        try:
            job_title = item.find("a").text.strip()
            job_link = item.find("a")["href"]
        except (AttributeError, KeyError) as e:
            print(f"Error extracting job title/link: {e}")
            continue

        job = {"job_title": job_title, "job_link": job_link}
        jobs_list.append(job)

    return jobs_list


def inspect_jobs(jobs_list):
    for job in jobs_list:
        job_link = job["job_link"]
        try:
            job_data = requests.get(job_link)
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving job data: {e}")
            continue

        job_soup = bs(job_data.text, "html.parser")
        job_info_boxes = job_soup.find_all("div", class_="box-body p-3")

        if len(job_info_boxes) < 2:
            print("Error extracting job summary/description")
            continue

        job_summary = job_info_boxes[1].text.strip()
        job_description = job_info_boxes[0].text.strip()

        job["job_summary"] = job_summary
        job["job_description"] = job_description

    return jobs_list


def save_jobs_to_csv(jobs_list, filename):
    jobs_df = pd.DataFrame(
        jobs_list, columns=["job_title", "job_link", "job_summary", "job_description"]
    )
    jobs_df = jobs_df[["job_title", "job_link"]]
    jobs_df.to_csv(filename, index=False)


def check_for_keywords(jobs_list, keywords):
    new_list = []
    keywords_set = set(keywords)
    for job in jobs_list:
        job_summary = job["job_summary"].lower()
        job_description = job["job_description"].lower()
        if any(
            keyword in job_summary or keyword in job_description
            for keyword in keywords_set
        ):
            new_list.append(job)

    return new_list


if __name__ == "__main__":
    url = "https://www.myjobsinkenya.com/"
    scraped_data = scrape_job_links(url)
    job_info = inspect_jobs(scraped_data)
    keywords = {"python", "django", "flask", "data science", "data analyst", "software"}
    keywords_jobs = check_for_keywords(job_info, keywords)
    save_jobs_to_csv(keywords_jobs, "jobs.csv")
