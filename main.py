import unicodedata
import json
import bs4
import requests
from fake_headers import Headers

def get_fake_headers():
    return Headers(browser="chrome", os="mac").generate()

def vacancies_list():
    parsed_data = []
    parsed_data_dollars = []
    for ind in range (0,40):
        link_hh = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={ind}'
        response = requests.get(link_hh, headers=get_fake_headers())
       
        main_page_data = bs4.BeautifulSoup(response.text,features='lxml')
        vacancies_tags = main_page_data.findAll('div', class_='vacancy-serp-item-body__main-info')
        for vacancies_tag in vacancies_tags:
            h3_tag = vacancies_tag.find('h3', class_='bloko-header-section-3')
            salary_tag = vacancies_tag.find('span',class_= 'bloko-header-section-2')
            if salary_tag == None:
                salary = 'Вилка зарплат не указана'
            else:
                salary = salary_tag.text.strip()
                salary = unicodedata.normalize('NFKD', salary)
            info_tag = vacancies_tag.find('div', class_='vacancy-serp-item__info')
            inf_result= info_tag.find_all('div', class_='bloko-text')
            company_name= inf_result[0].text.strip()
            company_name = unicodedata.normalize('NFKD', company_name)
            city = inf_result [1].text.strip()
            a_tag = h3_tag.find('a', class_='bloko-link')
            link = a_tag['href']
            title = a_tag.find('span').text.strip()
    
            if "Django" in title or "Flask" in title:
                parsed_data.append({
                    'company_name': company_name,
                    'city': city,
                    'title': title,
                    'salary': salary,
                    'link': link})
                if '$' in salary:
                    parsed_data_dollars.append({
                        'company_name': company_name,
                        'city': city,
                        'title': title,
                       'salary': salary,
                        'link': link})
    return parsed_data, parsed_data_dollars

if __name__ == '__main__':
    parsed_data, parsed_data_dollars = vacancies_list()  

    with open('vacancies.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))
    with open('vacancies$.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(parsed_data_dollars, ensure_ascii=False, indent=4))  
 