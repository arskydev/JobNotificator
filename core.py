from hhparcer import hhparcer
from datetime import date, timedelta

import smtplib
from secrets import EMAIL_ADDRESS, EMAIL_PASSWORD, DESTINATION_EMAIL
from email.mime.text import MIMEText
from email.header    import Header
import os


def run(vacancy_input):
    h = hhparcer(vacancy_input)
    h.main()
    now = hhparcer.now
    yesterday  = now - timedelta(days=1)
    yesterday_dir_name = './' + str(yesterday.day) + str(yesterday.strftime("%b")) + '/'
    yesterday_file_name = yesterday_dir_name + h.filename_src + "_" + str(yesterday.day) + "_" + str(yesterday.month) + ".txt"
    tdy_vacancy_list=[]
    tdy_links_list = []

    tdy_vacancy_list.append(h.results)
    tdy_links_list.append(h.searching)

    while "pager-next" in str(h.html):
        h.page += 1
        h.main_next()
        tdy_vacancy_list.append(h.results)
        tdy_links_list.append(h.searching)


    today_vacancy_list = []
    for i in tdy_vacancy_list:
        for j in i:
            today_vacancy_list.append(j)

    today_links_list = []
    for i in tdy_links_list:
        for j in i:
            today_links_list.append(j)

    yesterday_links_list = []

    try:
        f = open(f"{yesterday_file_name}".replace(".txt", "_search.txt"), "r", encoding="utf-8")
    except FileNotFoundError:
        os.makedirs(yesterday_dir_name, exist_ok=True)
        f = open(f"{yesterday_file_name}".replace(".txt", "_search.txt"), "w", encoding="utf-8")
        f.close()
    except UnboundLocalError:
        os.mkdir(yesterday_dir_name, exist_ok=True)
        f = open(f"{yesterday_file_name}".replace(".txt", "_search.txt"), "w", encoding="utf-8")
        f.close()
    else:
        a = f.read().splitlines()
        for urls in a:
            yesterday_links_list.append(urls)
        f.close()   
        

    f = open(f"{h.filename}".replace(".txt", "_new_vacancies.txt"), "w", encoding="utf-8" )
    i = 1
    for link in today_links_list:
        if link not in yesterday_links_list:
            for vacancy in today_vacancy_list:
                if vacancy["vacancyURL"] == link:
                    # print("new vacancy")
                    # print(vacancy["title"], vacancy['employer'], vacancy['salary'], vacancy['vacancyURL'])
                    f.write(
f"""Vacancy #{i}

Job title: {vacancy['title']}
Employer: {vacancy['employer']}
Salary: {vacancy['salary']}
URL: {vacancy['vacancyURL']}
#############################################################

"""
                        )
                    i += 1

    f.close()
    return "done"

def send(file_name):

    f = open(f"{file_name}", "r", encoding="utf-8")
    text = f.read()
    f.close()

    message = MIMEText(f'{text}', 'plain', 'utf-8')
    message['Subject'] = Header('New vacancies ' + str(date.today().day) + " " + str(date.today().strftime("%b")), 'utf-8')
    message['From'] = EMAIL_ADDRESS
    message['To'] = DESTINATION_EMAIL


    email = EMAIL_ADDRESS
    password = EMAIL_PASSWORD

    server = smtplib.SMTP('smtp.yandex.ru', 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)

    destdy_email = DESTINATION_EMAIL

    # server.setdy_debuglevel(1)
    server.sendmail(message['From'], destdy_email, message.as_string())
    server.quit()