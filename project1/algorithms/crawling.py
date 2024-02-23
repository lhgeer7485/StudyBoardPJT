from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
import time
from .models import Problem, ProblemClass
from django.contrib.auth import get_user_model

rank_list = ['', 'B5', 'B4', 'B3', 'B2', 'B1', 'S5', 'S4', 'S3', 'S2', 'S1',  
            'G5', 'G4', 'G3', 'G2', 'G1', 'P5', 'P4', 'P3', 'P2', 'P1',
            'D5', 'D4', 'D3', 'D2', 'D1', 'R5', 'R4', 'R3', 'R2', 'R1']


rank_dic = {
    'Sprout' : 'B5','Unrated' : 'UR',
    'Bronze V' : 'B5', 'Bronze IV' : 'B4', 'Bronze III' : 'B3', 'Bronze II' : 'B2', 'Bronze I' : 'B1',
    'Silver V' : 'S5', 'Silver IV' : 'S4', 'Silver III' : 'S3', 'Silver II' : 'S2', 'Silver I' : 'S1',
    'Gold V' : 'G5', 'Gold IV' : 'G4', 'Gold III' : 'G3', 'Gold II' : 'G2', 'Gold I' : 'G1',
    'Platinum V' : 'P5', 'Platinum IV' : 'P4', 'Platinum III' : 'P3', 'Platinum II' : 'P2', 'Platinum I' : 'P1',
    'Diamond V' : 'D5', 'Diamond IV' : 'D4', 'Diamond III' : 'D3', 'Diamond II' : 'D2', 'Diamond I' : 'D1',
    'Ruby V' : 'R5', 'Ruby IV' : 'R4', 'Ruby III' : 'R3', 'Ruby II' : 'R2','Ruby I' : 'R1',
}


# 닉네임에 해당하는 유저 프로필에서 푼 문제들을 가져오는 크롤링
def solved_crawling(person):
    nickname = person.beakjoon_nickname
    url = f'https://www.acmicpc.net/user/{nickname}'
    
    # 크롤링으로 html 파일 전체 가져오기
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text

    # html파일에서 필요한 부분 파싱하기
    soup = BeautifulSoup(html, "html.parser")
    solved_list = soup.select_one(".problem-list")
    solved_list = solved_list.select("a")
    beakjoon_rank_tag = soup.select_one(".solvedac-tier")
    # beakjoon_rank = rank_list[int(beakjoon_rank_tag.get("src")[-5])]
    beakjoon_rank = rank_list[int(beakjoon_rank_tag.get("src").split('tier/')[-1].strip('.svg'))]
    solved_num_list = [link.get("href").lstrip('/problem/') for link in solved_list ]
    # print(rank_list[int(beakjoon_rank.get("src")[-5])])

    # 이를 활용하여 user DB에 데이터 추가
    person.beakjoon_rank = beakjoon_rank
    person.save()

    for solved_num in solved_num_list:
        try:
            problem = Problem.objects.get(problem_num=solved_num) 
        except:
            continue
        problem.solved_users.add(person)


# slove.ac에서 클릭을 활용해서 문제의 등급, 분류를 가져오는 크롤링
def problem_crawling(problem_num):
    url = f'https://solved.ac/search?query={problem_num}'

    driver = webdriver.Chrome()
    driver.get(url)

    # 분류목록을 보이게하는 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/table/tbody/tr[1]/td[2]/span/div/div[1]/span[2]/div/button').click()
    time.sleep(1)

    # 열린 페이지 소스를 받아오기
    html = driver.page_source

    # 필요한 정보 파싱
    soup = BeautifulSoup(html, "html.parser")
    rank = soup.select(".css-1vnxcg0")
    print(rank[5]['alt'])
    classifications = soup.select('.css-1rqtlpb')
    classifications_list = [classification.get_text().lstrip('#') for classification in classifications ]
    print(classifications_list)
    name = soup.select('.__Latex__')
    print(name[5].text)
    return name[5].text, rank[5]['alt'], classifications_list



# slove.ac에서 클릭을 활용해서 문제의 등급, 분류를 가져오는 크롤링
def problem_crawling(problem_num):
    url = f'https://solved.ac/search?query={problem_num}'

    driver = webdriver.Chrome()
    driver.get(url)

    # 분류목록을 보이게하는 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/table/tbody/tr[1]/td[2]/span/div/div[1]/span[2]/div/button').click()
    time.sleep(1)

    # 열린 페이지 소스를 받아오기
    html = driver.page_source

    # 필요한 정보 파싱
    soup = BeautifulSoup(html, "html.parser")
    rank = soup.select(".css-1vnxcg0")
    print(rank[5]['alt'])
    classifications = soup.select('.css-1rqtlpb')
    classifications_list = [classification.get_text().lstrip('#') for classification in classifications ]
    print(classifications_list)
    name = soup.select('.__Latex__')
    print(name[5].text)
    return name[5].text, rank[5]['alt'], classifications_list



def problem_crawling3(request, problem_num):
    name, rank, classifications_list = problem_crawling(problem_num)
    problem, a = Problem.objects.get_or_create(name=name, rank=rank_dic[rank],problem_num=problem_num)
    problem.save()
    for classification in classifications_list:
        classification, a = ProblemClass.objects.get_or_create(name=classification)
        classification.problems.add(problem)


# DB에 데이터를 넣기위한 다수의 문제를 크롤링하기
def problem_list_crawling(request):
    for i in range(100,101):
        url = f'https://www.acmicpc.net/problemset?sort=ac_desc&page={i}'
        
        # 크롤링으로 html 파일 전체 가져오기
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        
        # html파일에서 문제 번호들을 파싱하기
        problem_list = soup.select(".list_problem_id")
        problem_num_list = [link.get_text() for link in problem_list ]
        
        error_list = []
        # print(len(problem_num_list))

        # 위 리스트를 활용하여 user DB에 데이터 추가 
        for problem_num in problem_num_list:
            try:
                name, rank, classifications_list = problem_crawling(problem_num)
                problem, a = Problem.objects.get_or_create(name=name, rank=rank_dic[rank],problem_num=problem_num)
                problem.save()
                for classification in classifications_list:
                    classification, a = ProblemClass.objects.get_or_create(name=classification)
                    classification.problems.add(problem)
            except:
                error_list.append(problem_num)
        
        print(error_list)
        
        
# DB에 빠진 문제가 없는지 확인하고 없는 문제의 정보를 받아와 DB에 넣는 함수
def check(request):
    lst = []
    for i in range(1,101):
        url = f'https://www.acmicpc.net/problemset?sort=ac_desc&page={i}'
        
        # 크롤링으로 html 파일 전체 가져오기
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        
        # html파일에서 문제 번호들을 파싱하기
        problem_list = soup.select(".list_problem_id")
        problem_num_list = [link.get_text() for link in problem_list ]
        for problem_num in problem_num_list:
            if Problem.objects.filter(problem_num=problem_num).exists():
                pass
            else:
                lst.append(problem_num)
    for problem_num in lst:
            try:
                name, rank, classifications_list = problem_crawling(problem_num)
                problem, a = Problem.objects.get_or_create(name=name, rank=rank_dic[rank],problem_num=problem_num)
                problem.save()
                for classification in classifications_list:
                    classification, a = ProblemClass.objects.get_or_create(name=classification)
                    classification.problems.add(problem)
            except:
                pass


def classes_num(request):
    url = "https://www.acmicpc.net/problem/tags"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    tag_list = soup.select("td a")
    for tag in tag_list:
        if ProblemClass.objects.filter(name=tag.get_text()).exists():
            cl = ProblemClass.objects.get(name=tag.get_text())
            print(tag.get('href').strip('/problem/tag/'))
            cl.ProblemClass_num = int(tag.get('href').strip('/problem/tag/'))
            cl.save()
















# 실패
# 로그인 후 문제의 등급, 분류를 가져오는 크롤링() 
def XXXproblem_crawling(problem_num):
    # 로그인 정보
    url_login = "https://www.acmicpc.net/signin"

    # 세션 유지
    session = requests.session()

    # 로그인 요청
    login_info = {
        "login_user_id": 'ssafy1002123',
        "login_password": 'rlaTKvl123'
    }

    #POST로 데이터 보내기
    res = session.post(url_login, data=login_info , headers={"User-Agent": "Mozilla/5.0"})
    res.raise_for_status() #오류 발생하면 예외 발생

    if res.status_code == 200:
        print('로그인 성공')
    else:
        print('로그인 실패')

    # 크롤링 하기
    url = f'https://www.acmicpc.net/problem/{problem_num}'
    response = session.get(url, headers={"User-Agent": "Mozilla/5.0"})
    html = response.text

    # html파일 파싱하기
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())


# 실패
# 내 크롬 프로필을 가져와 내 프로필 쿠키로 자동 로그인 후 문제의 등급, 분류를 가져오는 크롤링 
def XXXproblem_crawling2(problem_num):
    url = f'https://www.acmicpc.net/problem/{problem_num}'

    # options = Options()
    # user_data = r"C:/Users/SSAFY/AppData/Local/Google/Chrome/User Data/Profile 15"
    # options.add_argument(f"user-data-dir={user_data}")

    # 내프로필을 드라이버의 옵션으로 설정
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=/Users/SSAFY/AppData/Local/Google/Chrome")
    options.add_argument("--profile-directory=Profile 15")

    # 웹드라이버로 get 요청
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # 열린 페이지 소스를 받아오기
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # result_stats = soup.select_one('#result-stats')
    print(soup.prettify())

    with open('soup.txt', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())


