
import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def load():
    options = Options()
    options.headless = True
    browser = webdriver.Chrome("C:/Users/lalpa/AppData/Local/Google/Chrome/Application/chromedriver.exe",chrome_options=options)
    browser.get('https://www.linkedin.com/uas/login')
    file = open('config.txt')
    lines = file.readlines()
    username = lines[0]
    password = lines[1]
    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)
    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)
    elementID.submit()

    return browser

def  scrap(browser,link):    
    browser.get(link)
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    for i in range(3):
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)
       
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')
      

    name_div = soup.find('div', {'class': 'flex-1 mr5'})
    name_loc = name_div.find_all('ul')
    name = name_loc[0].find('li').get_text().strip()
    loc = name_loc[1].find('li').get_text().strip()
    profile_title = name_div.find('h2').get_text().strip()
    connection = name_loc[1].find_all('li')
    connection = connection[1].get_text().strip()

    info = ["Not Mentioned"] * 11
    try:
        info[0]=link
    except:
        pass
    try:
        info[1]=name
    except:
        pass
    try:
        info[2]=profile_title
    except:
        pass
    try:
        info[3]=loc
    except:
        pass
    try:
        info[4]=connection
    except:
        pass
    try:
        exp_section = soup.find('section', {'id': 'experience-section'})
    except:
        pass

    try:
        exp_section = exp_section.find('ul')
        li_tags = exp_section.find('div')
        a_tags = li_tags.find('a')
    except:
        pass
    try:
        job_title = a_tags.find('h3').get_text().strip()
        job_title = job_title.replace("\n"," : ------- ")
    except:
        pass
    try:
        joining_date = a_tags.find_all('h4')[0].find_all('span')[1].get_text().strip()
        exp = a_tags.find_all('h4')[1].find_all('span')[1].get_text().strip()
    except:
        pass
    try:
        info[5]=job_title
    except:
        pass
    try:
        info[6]=joining_date
    except:
        pass
    try:
        info[7]=exp
    except:
        pass
    try:
        edu_section = soup.find('section', {'id': 'education-section'}).find('ul')
    except:
        pass

    try:
        college_name = edu_section.find('h3').get_text().strip()
        degree_name = edu_section.find('p', {'class': 'pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal'}).find_all('span')[1].get_text().strip()
        stream = edu_section.find('p', {'class': 'pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal'}).find_all('span')[1].get_text().strip()
        degree_year = edu_section.find('p', {'class': 'pv-entity__dates t-14 t-black--light t-normal'}).find_all('span')[1].get_text().strip()
    except:
        pass

    try:
        info[8]=college_name
    except:
        pass

    try:
        info[9]=degree_name
    except:
        pass

    try:
        info[10]=stream
    except:
        pass

    try:
       info[11]=degree_year
    except:
        pass

    return info

def close(browser):
    browser.close()

