#DON'T FORGET PIP INSTALL BS4!
from bs4 import BeautifulSoup
import urllib.request
from datetime import date
import os

class hhparcer:
    page = 0
    index = 1
    now = date.today()
    dir_name = './' + str(now.day) + str(now.strftime("%b")) + '/'

    def __init__(self, vacancy):
        self.vacancy = vacancy

    def create_directory(self):
        os.makedirs(self.dir_name, exist_ok=True)

    def url_mods(self):
        jobtitle = self.vacancy.split()
        self.job_urn = self.job_url_overhead = self.filename_src = jobtitle[0]

        for i in range(1,len(jobtitle)):
            self.job_urn += "+" + jobtitle[i]
            self.job_url_overhead += "%20" + jobtitle[i]
            self.filename_src += "_" + jobtitle[i]

        self.filename = self.dir_name + self.filename_src + "_" + str(self.now.day) + "_" + str(self.now.month) + ".txt"

    def create_request(self):
        req = urllib.request.urlopen(f"https://hh.ru/search/vacancy?clusters=true&area=1&search_field=name&no_magic=true&enable_snippets=true&salary=&st=searchVacancy&text={self.job_urn}&page={self.page}")
        self.html = req.read()

    def items_create(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        self.items = soup.find_all('div', class_='vacancy-serp-item')

    def parsing(self):
        self.results = []
        self.searching = []
        
        for item in self.items:
            title = item.find('a', class_='bloko-link HH-LinkModifier').get_text()
            salarySearch = item.find('div', class_='vacancy-serp-item__sidebar').get_text()
            if salarySearch:
                salary = salarySearch
            else:
                salary = "Not specified"
            employer = item.find('div', class_='vacancy-serp-item__meta-info').get_text()
            vacancyURL = item.a.get('href').replace(f"?query={self.job_url_overhead}", "")
            
            self.results.append({
                'title': title,
                'salary': salary,
                'employer': employer,
                'vacancyURL': vacancyURL,
            })

            self.searching.append(vacancyURL)

    def result_to_file(self):
        f = open(f"{self.filename}", "w", encoding="utf-8" )
        for item in self.results:
            f.write(

f"""Vacancy #{self.index}

Job title: {item['title']}
Salary: {item['salary']}
Employer: {item['employer']}
URL: {item['vacancyURL']}
#############################################################
    
"""
            )
            self.index += 1
        f.close()
        
        fl = open(f"{self.filename}".replace(".txt", "_search.txt"), "w", encoding="utf-8" )
        for url in self.searching:
            fl.write(f"{url}\n")
        fl.close()

    def append_result(self):
        f = open(f"{self.filename}", "a+", encoding="utf-8" )
        for item in self.results:
            f.write(

f"""Vacancy #{self.index}

Job title: {item['title']}
Employer: {item['employer']}
Salary: {item['salary']}
URL: {item['vacancyURL']}
#############################################################

"""
            )
            self.index += 1
        f.close()
        
        fl = open(f"{self.filename}".replace(".txt", "_search.txt"), "a+", encoding="utf-8" )
        for url in self.searching:
            fl.write(f"{url}\n")
        fl.close()

    def main(self):
        self.create_directory()
        self.url_mods()
        self.create_request()
        self.items_create()
        self.parsing()
        self.result_to_file()

    def main_next(self):
        self.url_mods()
        self.create_request()
        self.items_create()
        self.parsing()
        self.append_result()

if __name__ == "__main__":
    pass