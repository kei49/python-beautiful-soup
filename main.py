import requests
import numpy as np
from bs4 import BeautifulSoup

sort_label = {
    2: "総合評価",
    3: "待遇面の満足度",
    4: "社員の士気",
    5: "風通しの良さ",
    6: "社員の相互尊重",
    7: "20代成長環境",
    8: "人材の長期育成",
    9: "法令遵守意識",
    10: "人事評価の適正感"}

ua_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
           'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
           ]


def check_title(txt, sort_num):
    assert txt == sort_label[sort_num]
    print(txt)
    return None


def get_bs(url):
    ua = ua_list[np.random.randint(0, len(ua_list))]
    response = requests.get(url, headers={"User-Agent": ua})
    bs = BeautifulSoup(response.content, "html.parser")
    return bs


def provide_url(sort_num, category="company_list"):
    # oepnwork = "https://www.vorkers.com/company_list?field=&pref=&src_str=&sort=2"
    assert category == "company_list"
    base = "https://www.vorkers.com/"
    query = "?field=&pref=&src_str=&sort=" + str(sort_num)

    return base + category + query


def parse_test_company(bs):
    test_company = bs.find("ul", attrs={"class": "testCompanyList"})
    companies = test_company.find_all("li", attrs={"class", "box-15"})

    companies_data = []

    for company in companies:
        company_info = {}

        h3 = company.find("h3")
        rank = h3.find("span", attrs={"class": "rankingCount"})
        company_info["rank"] = int(rank.get_text())
        company_name = h3.find("a")
        company_info["url"] = company_name["href"]
        company_info["name"] = company_name.get_text()

        img = company.find("img", attrs={"class": "companyLogoImage"})
        company_info["img_src"] = img["src"]
        company_info["img_alt"] = img["alt"]

        total_evaluation = company.find(
            "p", class_="totalEvaluation_item fs-15 fw-b").get_text()
        company_info["total_evaluation"] = float(total_evaluation)

        category_evaluation = company.find(
            "dd", attrs={"class", "d-i"}).get_text()
        company_info["category_evaluation"] = float(category_evaluation)

        field = company.find("p", class_="gray mt-5").get_text()
        company_info["field"] = field

        employee_reviews_li = company.find_all(
            "li", attrs={"class": "list-dashed_item"})[0]
        company_info["employee_review"] = int(employee_reviews_li.find(
            "span", class_="fs-14 fw-b").get_text())

        companies_data.append(company_info)

    print(companies_data)


def main():
    query_sort = 3
    openwork = provide_url(sort_num=query_sort)
    bs = get_bs(url=openwork)

    title_elem = bs.find("h2", attrs={"id": "mainTitle"})
    title_text = title_elem.get_text()[: -5]
    check_title(title_text, query_sort)

    parse_test_company(bs)


if __name__ == "__main__":
    main()
