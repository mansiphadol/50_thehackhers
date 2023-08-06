import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flask import Flask, render_template, request
from googletrans import Translator
import os
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')
def get_translated_text(text, target_lang):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_lang)
    return translated_text.text

def scrape_teamlease_jobs(maids, location, lang_choice):
    base_url = f"https://www.teamlease.com/{maids}-jobs-in-{location}"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    job_display_section = soup.find_all("div", class_="main-job-div")
    jobs_data = []

    if not job_display_section:
        return jobs_data

    for job in job_display_section:
        job_title_tag = job.find("b", class_="job_title")
        company_name_tag = job.find("div", class_="company-name padding-left-16")
        location_tag = job.find("span", class_="loc")
        salary_tag = job.find("div", class_="salary-section")
        job_desc_tag = job.find("span", class_="job-desc")
        quick_apply_btn = job.find("div", class_="quick_apply_btn div-apply applied_job_429596 fkj")
        job_url_tag = job.find("a", class_="job-url")

        if job_url_tag:
            job_url = urljoin(base_url, job_url_tag["href"])
        else:
            job_url = "N/A"

        job_title = job_title_tag.text.strip() if job_title_tag else ""
        company_name = company_name_tag.text.strip() if company_name_tag else ""
        location = location_tag.text.strip() if location_tag else ""
        salary = salary_tag.text.strip() if salary_tag else ""
        job_desc = job_desc_tag.text.strip() if job_desc_tag else ""


        if lang_choice == "2":  # Hindi
            job_title = get_translated_text(job_title, "hi")
            company_name = get_translated_text(company_name, "hi")
            location = get_translated_text(location, "hi")
            salary = get_translated_text(salary, "hi")
            job_desc = get_translated_text(job_desc, "hi")
        elif lang_choice == "3":  # Marathi
            job_title = get_translated_text(job_title, "mr")
            company_name = get_translated_text(company_name, "mr")
            location = get_translated_text(location, "mr")
            salary = get_translated_text(salary, "mr")
            job_desc = get_translated_text(job_desc, "mr")

        job_data = {
            "job_title": job_title,
            "company_name": company_name,
            "location": location,
            "salary": salary,
            "job_desc": job_desc,
            "job_url": job_url
        }

        jobs_data.append(job_data)

    return jobs_data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        maids_input = request.form["job_title"]
        location_input = request.form["location"]
        lang_choice = request.form["lang_choice"]

        jobs_data = scrape_teamlease_jobs(maids_input, location_input, lang_choice)

        # Replace 'N/A' with empty strings
        for job in jobs_data:
            for key in job:
                if job[key] == 'N/A':
                    job[key] = ''

        return render_template("index.html", jobs_data=jobs_data)  # Pass jobs_data to the template

    return render_template("index.html")  # This line should be outside the if block
