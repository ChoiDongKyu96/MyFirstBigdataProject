import sys
from PyQt5.QtWidgets import QTextBrowser, QMainWindow,QLabel, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QHBoxLayout,QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import matplotlib.pyplot as plt
import re
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'big_data_project'
        self.left = 0
        self.top = 0
        self.width = 1300
        self.height = 1000
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout2 = QHBoxLayout(self)
        self.layout3 = QHBoxLayout(self)
        self.layout4 = QHBoxLayout(self)
        self.layout5 = QHBoxLayout(self)
        self.layout6 = QHBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        self.label = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)
        self.label6 = QLabel(self)
        pixmap = QPixmap('naver.png')
        pixmap2 = QPixmap('google.png')
        pixmap3 = QPixmap('daum.png')
        pixmap4 = QPixmap('naver.png')
        pixmap5 = QPixmap('daum.png')
        pixmap6 = QPixmap('google.png')
        self.label.setPixmap(pixmap)
        self.label2.setPixmap(pixmap2)
        self.label3.setPixmap(pixmap3)
        self.label4.setPixmap(pixmap4)
        self.label5.setPixmap(pixmap5)
        self.label6.setPixmap(pixmap6)
        self.layout3.addWidget(self.label)
        self.layout3.addWidget(self.label3)
        self.layout3.addWidget(self.label2)

        self.layout4.addWidget(self.label4)
        self.layout4.addWidget(self.label5)
        self.layout4.addWidget(self.label6)

        self.resize(pixmap.width(), pixmap.height())
        self.resize(pixmap2.width(), pixmap2.height())
        self.resize(pixmap3.width(), pixmap3.height())
        self.resize(pixmap4.width(), pixmap4.height())
        self.resize(pixmap5.width(), pixmap5.height())
        self.resize(pixmap6.width(), pixmap6.height())

        self.text = QTextBrowser(self)
        #self.text.append("ㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎ")
        self.text2 = QTextBrowser(self)
        #self.text2.append("ㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎ")
        self.text3 = QTextBrowser(self)
        #self.text3.append("ㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎ")
        self.text4 = QTextBrowser(self)
        self.text5 = QTextBrowser(self)
        self.text6 = QTextBrowser(self)
        self.text7 = QTextBrowser(self)
        self.text8 = QTextBrowser(self)
        # Add tabs
        self.tabs.addTab(self.tab1, "검색어")
        self.tabs.addTab(self.tab2,  "순위차이")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab2.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("조회")
        self.pushButton2 = QPushButton("상관관계 분석 ")
        self.pushButton1.clicked.connect(self.on_click)
        self.pushButton2.clicked.connect(self.on_click_comapre)
        self.layout2.addWidget(self.text)
        self.layout2.addWidget(self.text2)
        self.layout2.addWidget(self.text3)
        self.layout5.addWidget(self.text4)
        self.layout5.addWidget(self.text5)
        self.layout5.addWidget(self.text6)
        self.layout6.addWidget(self.text7)
        self.layout6.addWidget(self.text8)

        # self.tab1.layout.addWidget(self.pushButton2)
        self.tab1.layout.addLayout(self.layout3)
        self.tab2.layout.addLayout(self.layout4)
        self.tab2.layout.addLayout(self.layout5)
        self.tab2.layout.addLayout(self.layout6)
        self.tab1.layout.addLayout(self.layout2)
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.layout.addWidget(self.pushButton2)
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click_comapre(self):
        global naver_list, n_word_list, d_word_list ,g_word_list
        if len(naver_list):
            try :
                news_word_list = []
                news_word_list2 = []
                for searchword in n_word_list:
                    naver_url = "https://search.naver.com/search.naver?where=news&query="
                    add_url = "&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=4&ds=&de=&docid=&nso=so%3Ar%2Cp%3A1d%2Ca%3Aall&mynews=0&refresh_start=0&related=0"
                    name = searchword
                    full_url = naver_url + name + add_url
                    html = requests.get(full_url).text
                    soup = BeautifulSoup(html, 'html.parser')
                    # print(soup)
                    naver_list = soup.find_all('div', 'title_desc all_my')  # span tag중  ah_k class 읽어오기
                    for title in naver_list:
                        tmp_string = title.text.split('/')
                        numbers = re.findall("\d+", tmp_string[1])
                        news_word_list.append(int(numbers[0]))
                #


                plt.rc('font', family='Malgun Gothic')  # 맑은 고딕을 기본 글꼴로 설정
                plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
                plt.rcParams["xtick.labelsize"] = 10
                plt.title('네이버')  # 제목 설정
                plt.plot(n_word_list, news_word_list, 'green',
                         label="1일 이내 뉴스 키워드 언급 횟수 ")  # high 리스트에 저장된 값을 hotpink 색으로 그리고 레이블을 표시
                plt.xticks(n_word_list, rotation=90)
                # Pad margins so that markers don't get clipped by the axes
                plt.margins(0.2)
                # Tweak spacing to prevent clipping of tick-labels
                plt.subplots_adjust(bottom=0.3)
                plt.legend()  # 범례
                # plt.show()  # 그래프 나타내기
                news_word_list.clear()
                for searchword in d_word_list:
                    naver_url = "https://search.naver.com/search.naver?where=news&query="
                    add_url = "&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=4&ds=&de=&docid=&nso=so%3Ar%2Cp%3A1d%2Ca%3Aall&mynews=0&refresh_start=0&related=0"
                    name = searchword
                    full_url = naver_url + name + add_url
                    html = requests.get(full_url).text
                    soup = BeautifulSoup(html, 'html.parser')
                    # print(soup)
                    naver_list = soup.find_all('div', 'title_desc all_my')  # span tag중  ah_k class 읽어오기
                    for title in naver_list:
                        tmp_string = title.text.split('/')
                        numbers = re.findall("\d+", tmp_string[1])
                        news_word_list.append(int(numbers[0]))

                #
                plt.figure(2)
                plt.rc('font', family='Malgun Gothic')  # 맑은 고딕을 기본 글꼴로 설정
                plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
                plt.rcParams["xtick.labelsize"] = 10
                plt.title('다음')  # 제목 설정
                plt.plot(d_word_list, news_word_list, 'blue',
                         label="1일 이내 뉴스 키워드 언급 횟수 ")  # high 리스트에 저장된 값을 hotpink 색으로 그리고 레이블을 표시
                plt.xticks(d_word_list, rotation=90)
                # Pad margins so that markers don't get clipped by the axes
                plt.margins(0.2)
                # Tweak spacing to prevent clipping of tick-labels
                plt.subplots_adjust(bottom=0.3)
                plt.legend()  # 범례
                # plt.show()  # 그래프 나타내기

                news_word_list.clear()
                for searchword in g_word_list:
                    naver_url = "https://search.naver.com/search.naver?where=news&query="
                    add_url = "&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=4&ds=&de=&docid=&nso=so%3Ar%2Cp%3A1d%2Ca%3Aall&mynews=0&refresh_start=0&related=0"
                    name = searchword
                    full_url = naver_url + name + add_url
                    html = requests.get(full_url).text
                    soup = BeautifulSoup(html, 'html.parser')
                    # print(soup)
                    naver_list = soup.find_all('div', 'title_desc all_my')  # span tag중  ah_k class 읽어오기
                    for title in naver_list:
                        tmp_string = title.text.split('/')
                        numbers = re.findall("\d+", tmp_string[1])
                        news_word_list.append(int(numbers[0]))
                plt.figure(3)
                plt.rc('font', family='Malgun Gothic')  # 맑은 고딕을 기본 글꼴로 설정
                plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
                plt.rcParams["xtick.labelsize"] = 10
                plt.title('구글')  # 제목 설정
                plt.plot(g_word_list, news_word_list, 'red',
                         label="1일 이내 뉴스 키워드 언급 횟수 ")  # high 리스트에 저장된 값을 hotpink 색으로 그리고 레이블을 표시
                plt.xticks(g_word_list, rotation=90)
                # Pad margins so that markers don't get clipped by the axes
                plt.margins(0.2)
                # Tweak spacing to prevent clipping of tick-labels
                plt.subplots_adjust(bottom=0.3)
                plt.legend()  # 범례
                plt.show()  # 그래프 나타내기
            except :
                print("ERROR")
                QMessageBox.about(self, "알림", "에러가 발생했습니다. 인터넷 연결을 확인하고 다시 시도해주세요.")

    def on_click(self):
        global naver_list, n_word_list, d_word_list ,g_word_list
        ## naver
        try:
            naver_url = "http://www.naver.com"
            naver_up = ""
            naver_down = ""
            daum_up = ""
            daum_down = ""
            google_up = ""
            google_down = ""
            html = requests.get(naver_url).text
            soup = BeautifulSoup(html, 'html.parser')
            naver_list = soup.find("div", "ah_roll PM_CL_realtimeKeyword_rolling_base").find_all('span','ah_k') # span tag중  ah_k class 읽어오기
            n_word_list.clear()
            d_word_list.clear()
            g_word_list.clear()
            self.text.setText("")
            self.text2.setText("")
            self.text3.setText("")

            i = 1
            for title in naver_list:
                n_word_list.append(title.text)
            for searchword in n_word_list:
                # print(searchword)
                self.text.append(str(i)+". " + searchword)
                i +=1


                ### daum
            naver_up = n_word_list[0]
            naver_down = n_word_list[19]
            daum_url = "https://www.daum.net"

            html = requests.get(daum_url).text
            soup = BeautifulSoup(html, 'html.parser')

            daum_list = soup.find("ol", "list_hotissue issue_row list_mini").find_all('a',
                                                                                      'link_issue')  # ol의 tag중 list_hotissue  class 중 a tag중  link_issue class 읽어오기

            d_word_list = []
            i = 1
            for title in daum_list:
                d_word_list.append(title.text)

            # 결과 확인
            for searchword in d_word_list:

                self.text2.append(str(i) + ". " + searchword)
                i += 1
            ii = 1
            daum_up = d_word_list[0]
            daum_down = d_word_list[9]

            google_url = "https://trends.google.com/trends/?geo=KR"
            driver = webdriver.Chrome('driver/chromedriver')
            driver.get("https://trends.google.com/trends/?geo=KR")
            sido_list_raw = driver.find_element_by_xpath(
                """/html/body/div[2]/div[2]/div/div/ng-include/div/recently-trending/div/div[3]""")

            sido_list = sido_list_raw.find_elements_by_tag_name("div")

            sido_names_values = [option.text for option in sido_list]

            driver.close()
            tmp_string = sido_names_values[0].split('\n')

            g_word_list = []
            g_rank_list = []

            for i in range(0, 10):

                g_word_list.append(tmp_string[2 * i])
                self.text3.append(str(ii) + ". " + tmp_string[2 * i])
                ii += 1
                ttemp = tmp_string[2 * i + 1]
                s = ""
                for j in ttemp:
                    if j == '천':
                        g_rank_list.append(1000 * int(s))
                        break
                    elif j == '만':
                        g_rank_list.append(10000 * int(s))
                        break
                    else:
                        s += j
            google_up = g_word_list[0]
            google_down = g_word_list[9]

            self.text4.setText("네이버 1위 검색어\n")
            self.text4.append("["+'<span style=\" color: #ff0000;\">%s</span>' %naver_up+"]\n")
            self.text4.append("연관검색어 [")
            naver_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query="
            name = naver_up
            full_url = naver_url + name
            html = requests.get(full_url).text
            soup = BeautifulSoup(html, 'html.parser')
            naverr_list = soup.find_all('ul', '_related_keyword_ul')  # span tag중  ah_k class 읽어오기
            r_word_list = []

            for title in naverr_list:
                self.text4.append(title.text)
            self.text4.append("]\n\n")
            self.text4.append("네이버 20위 검색어\n")
            self.text4.append("[" + '<span style=\" color: #0000ff;\">%s</span>' %naver_down + "]\n")
            self.text4.append("연관검색어 [")
            naver_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query="
            name = naver_down
            full_url = naver_url + name
            html = requests.get(full_url).text
            soup = BeautifulSoup(html, 'html.parser')
            naverr_list = soup.find_all('ul', '_related_keyword_ul')  # span tag중  ah_k class 읽어오기
            r_word_list = []

            for title in naverr_list:
                self.text4.append(title.text)
            self.text4.append("]\n\n")
            self.text5.setText("")

            self.text5.setText("다음 1위 검색어\n")
            self.text5.append("[" + '<span style=\" color: #ff0000;\">%s</span>' %daum_up + "]\n")
            self.text5.append("연관검색어 [")
            naver_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query="
            name = daum_up
            full_url = naver_url + name
            html = requests.get(full_url).text
            soup = BeautifulSoup(html, 'html.parser')
            naverr_list = soup.find_all('ul', '_related_keyword_ul')  # span tag중  ah_k class 읽어오기
            r_word_list = []

            for title in naverr_list:
                self.text5.append(title.text)
            self.text5.append("]\n\n")
            self.text5.append("다음 10위 검색어\n")
            self.text5.append("[" + '<span style=\" color: #0000ff;\">%s</span>' %daum_down + "]\n")
            self.text5.append("연관검색어 [")
            naver_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query="
            name = daum_down
            full_url = naver_url + name
            html = requests.get(full_url).text
            soup = BeautifulSoup(html, 'html.parser')
            naverr_list = soup.find_all('ul', '_related_keyword_ul')  # span tag중  ah_k class 읽어오기
            r_word_list = []

            for title in naverr_list:
                self.text5.append(title.text)
            self.text5.append("]\n\n")

            self.text6.setText("")

            self.text6.setText("구글 1위 검색어\n")
            self.text6.append("[" + '<span style=\" color: #ff0000;\">%s</span>' %google_up + "]\n")
            self.text6.append("연관검색어 [")
            naver_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query="
            name = google_up
            full_url = naver_url + name
            html = requests.get(full_url).text
            soup = BeautifulSoup(html, 'html.parser')
            naverr_list = soup.find_all('ul', '_related_keyword_ul')  # span tag중  ah_k class 읽어오기
            r_word_list = []

            for title in naverr_list:
                self.text6.append(title.text)
            self.text6.append("]\n\n")
            self.text6.append("구글 10위 검색어\n")
            self.text6.append("[" + '<span style=\" color: #0000ff;\">%s</span>' %google_down + "]\n")
            self.text6.append("연관검색어 [")
            naver_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query="
            name = google_down
            full_url = naver_url + name
            html = requests.get(full_url).text
            soup = BeautifulSoup(html, 'html.parser')
            naverr_list = soup.find_all('ul', '_related_keyword_ul')  # span tag중  ah_k class 읽어오기
            r_word_list = []

            for title in naverr_list:
                self.text6.append(title.text)
            self.text6.append("]\n\n")
            self.text7.setText("포털사이트 2개 검출된키워드")
            self.text8.setText("포털사이트 3개 검출된키워드")
            ni=1

            for searchword_n in n_word_list:
                di = 1
                for searchword_d in d_word_list:
                    if searchword_n[0] == searchword_d[0] and searchword_n[1] == searchword_d[1]:
                        self.text7.append('<span style=\" color: #009900;\">%s</span>' %"네이버"+": " + searchword_n +" ("+str(ni)+"위) && " +    '<span style=\" color: #0000ff;\">%s</span>' %"다음"+": " + searchword_d +" ("+str(di) +"위)")
                    di += 1
                di = 1
                for searchword_g in g_word_list:
                    if searchword_n[0] == searchword_g[0] and searchword_n[1] == searchword_g[1]:
                        self.text7.append(
                            '<span style=\" color: #009900;\">%s</span>' % "네이버" + ": " + searchword_n + " (" + str(
                                ni) + "위) && " + '<span style=\" color: #ff0000;\">%s</span>' % "구글" + ": " + searchword_g + " (" + str(
                                di) + "위)")
                    di += 1
                ni += 1
            ni = 1
            for searchword_d in d_word_list:
                di =1
                for searchword_g in g_word_list:
                    if searchword_d[0] == searchword_g[0] and searchword_d[1] == searchword_g[1]:
                        self.text7.append(
                            '<span style=\" color: #0000ff;\">%s</span>' % "다음" + ": " + searchword_d + " (" + str(
                                ni) + "위) && " + '<span style=\" color: #ff0000;\">%s</span>' % "구글" + ": " + searchword_g + " (" + str(
                                di) + "위)")
                    di +=1
                ni += 1
            ni = 1
            gi =1
            for searchword_n in n_word_list:
                di = 1
                for searchword_d in d_word_list:
                    gi = 1
                    if searchword_n[0] != searchword_d[0] or searchword_n[1] != searchword_d[1]:
                        di += 1
                        continue
                    for searchword_g in g_word_list:
                        if searchword_n[0] == searchword_g[0] and searchword_n[1] == searchword_g[1] and searchword_n[0] == searchword_d[0] and searchword_n[1] == searchword_d[1] :
                            self.text8.append(
                                '<span style=\" color: #009900;\">%s</span>' % "네이버" + ": " + searchword_n + " (" + str(
                                    ni) + "위) &&  "+'<span style=\" color: #0000ff;\">%s</span>' % "다음" + ": " + searchword_d + " (" + str(
                                    di) + "위) &&"+ '<span style=\" color: #ff0000;\">%s</span>' % "구글" + ": " + searchword_g + " (" + str(
                                    gi) + "위)")
                        gi +=1
                    di += 1

                ni += 1
        except:
            print("ERROR")
            QMessageBox.about(self, "알림", "에러가 발생했습니다. 인터넷 연결을 확인하고 다시 시도해주세요")




if __name__ == '__main__':
    naver_list = []
    n_word_list= []
    d_word_list= []
    g_word_list= []
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())