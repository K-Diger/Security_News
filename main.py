# coding=<utf-8>
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import requests
import re
from datetime import datetime
from pytz import timezone
import csv
import calendar

class security_news:
    def __init__(self):
        self.security_keyword_list = (
                                        "랜섬웨어", "딥웹","긴급","유출",
                                        "스팸","피싱","스미싱","크래킹",
                                        "해킹","공격","악성코드","취약점",
                                        "제로데이","바이러스","위협",
                                        "정보보호","정보보안","보안","테러"
                                        "CERT","침해대응","Dos","DDos"
                                        "웜","SQL","관리자","접근권한"
                                        "IPS","IDS","방화벽","APT"
                                        "VPN","DLP","서버","패스워드"
                                        "위장", "피싱" ,"AI", "블록체인"
                                        "보안", "해킹", "메일", "접근통제"
                                        "컨설팅", "일반", "ICBM", "관리체계"
                                        "전망", "추세"
                                    )
        self.final_link = []
        self.final_txt = []
        self.yes_token = int(0)
        self.no_token = int(0)

        self.kst = datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")

        print(u"날짜를 직접 입력하시겠습니까? (Y/N): ", end="")
        self.input_date = input()

        if "Y" in self.input_date or "y" in self.input_date:
            print("===========================")
            print(u"아래의 양식에 맞추어 날짜를 입력")
            print("===========================")
            print(u"XXXX년 XX월 XX일")
            print("===========================")

            self.time_format = input()

            #self.cmp_time1 = str(self.kst[0:4] + self.kst[5:7] + self.kst[8:10])
            #self.cmp_time2 = str(self.time_format[0:4] + self.time_format[6:8] + self.time_format[10:12])

            print("------------------------------------------------------------------")
            print("[*] " + self.time_format + u"에 해당하는 보안뉴스를 불러옵니다. (최대 50페이지까지 검색 중) [*]")
            self.yes_token += 1
            print("------------------------------------------------------------------")

        elif "n" in self.input_date or "N" in self.input_date:
            self.time_format = self.kst[0:4] + "년 ", self.kst[5:7] + "월 ", self.kst[8:10] + "일 "
            self.time_format = self.time_format[0] + self.time_format[1] + self.time_format[2]

            print("------------------------------------------------------------------")
            print(u"[*] 오늘 키워드에 해당하는 보안뉴스를 불러옵니다. (최대 50페이지까지 검색 중) [*]")
            print("                 <현재시각>")
            print("            ", self.kst)
            print("------------------------------------------------------------------")
            self.no_token += 1
        else:
            print("입력값 오류")
            exit()

    def print_calendar(self):
        if self.yes_token == int(1):
            print("입력한 월의 달력을 불러옵니다. (주말에는 기사가 나오지 않음)")
            print("------------------------------------------------------------------")
            self.tf = int(self.time_format[0:4])
            self.tf_2 = int(self.time_format[7:8])
            calendar.prmonth(self.tf, self.tf_2)
            print("------------------------------------------------------------------")
        else:
            print("입력한 월의 달력을 불러옵니다. (주말에는 기사가 나오지 않음)")
            print("------------------------------------------------------------------")
            self.tf = int(self.time_format[0:4])
            self.tf_2 = int(self.time_format[7:8])
            calendar.prmonth(self.tf, self.tf_2)
            print("------------------------------------------------------------------")

    def get_News(self):
        for page in tqdm(range(1, 51)):
            url = "https://www.boannews.com/media/t_list.asp?Page="+str(page)+"&kind="
            self.txt = []  # 뉴스제목을 중복 제거한 집합을 하나씩 받아줄 리스트
            self.re_ex = re.compile("^/media/view")
            url_req = requests.get(url)
            soup = bs(url_req.text, "html.parser")

            self.news_title_txt = []
            self.news_title_area = soup.find_all("span", {"class": "news_txt"})
            self.news_writer_area = soup.find_all("span", {"class": "news_writer"})
            self.news_link_area = soup.find_all("div", {"class": "news_list"})
            self.link_add = "https://www.boannews.com/" # Base URL -> 링크 파싱한 것과 합칠 URL임

            self.title_bundle = [] # 뉴스기사 제목을 받을 리스트
            self.writer_bundle = [] # 뉴스기사 작성자를 받을 리스트
            self.link_bundle = [] # 뉴스기사 링크를 받을 리스트

            self.overlap_discard_txt = [] # 중복제거 한 값을 받기 위한 리스트
            self.overlap_discard_link = [] # 중복제거 한 링크를 받기 위한 리스트

            for title in self.news_title_area:
                self.title_bundle.append(title.get_text()) # title_bundle는 뉴스 제목을 하나씩 넣은 리스트임

            for writer in self.news_writer_area:
                self.writer_bundle.append(" | " + writer.get_text()) # writer_bundle는 뉴스 작성자를 하나씩 넣은 리스트임

            for i in range(len(self.writer_bundle)):
                for keyword in self.security_keyword_list: # 키워드 리스트 만큼 반복
                    if keyword in self.title_bundle[i] and self.time_format in self.writer_bundle[i]: # writer_bundle에 들어있는 날짜와 오늘 날짜와 같고, 키워드에 포함되면
                        self.filtered_content = (self.title_bundle[i] + self.writer_bundle[i]) # 기사제목과 작성기자, 날짜
                        self.news_title_txt.append(self.filtered_content)
                        self.link_bundle.append(self.news_link_area[i].find("a")["href"])

            for x in self.news_title_txt: # 뉴스 타이틀 중복 제거
                if x not in self.overlap_discard_txt:
                    self.overlap_discard_txt.append(x)

            for y in self.link_bundle: # 뉴스 링크 중복 제거
                if y not in self.overlap_discard_link:
                    self.overlap_discard_link.append(y)

            for j in range(len(self.overlap_discard_txt)):  # 최종 내용을 담을 리스트에 정리
                self.final_link.append(self.link_add + self.overlap_discard_link[j])
                self.final_txt.append(self.overlap_discard_txt[j])

    def crwal_to_csv(self):
        self.file = open(u"보안뉴스.csv", 'w', encoding="utf-8", newline="")
        self.csvfile = csv.writer(self.file)
        for z in range(len(self.final_txt)):  # csv파일로 추출
            self.csvfile.writerow(["[ " + str(z + 1) + " ]"])
            self.csvfile.writerow([self.final_txt[z]])
            self.csvfile.writerow([self.final_link[z]])
        self.file.close()

    def print_crwal(self):
        for j in range(len(self.final_txt)):  # 파싱내용 출력
            print(str([j + 1]), self.final_txt[j])
            print(self.final_link[j])
            print("---")
        print("\n※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※")
        if self.no_token == 1:
            print(u"금일 " + self.time_format + self.kst[11:19] + u" 기준")
            print(u"총 " + str(len(self.final_txt)) + u"개의 기사를 불러왔습니다.")
            print("※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※")
        else:
            print(u"지정날짜인 " + self.time_format + u" 기준")
            print(u"총 " + str(len(self.final_txt)) + u"개의 기사를 불러왔습니다.")
            print("※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※")

if __name__ == "__main__":
    parse = security_news()
    parse.print_calendar()
    parse.get_News()
    parse.crwal_to_csv()
    parse.print_crwal()