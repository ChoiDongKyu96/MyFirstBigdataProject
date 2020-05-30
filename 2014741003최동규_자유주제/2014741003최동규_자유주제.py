import sys
from PyQt5.QtWidgets import QTextBrowser, QMainWindow,QLabel, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QHBoxLayout,QMessageBox , QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv
# -*- coding: utf-8 -*-
import os
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import re
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Data analysis'
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

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        self.label_2 = QLabel("검색어입력", self)

        # LineEdit
        self.lineEdit = QLineEdit("", self)


        self.label = QLabel(self)


        pixmap = QPixmap('logo.png')


        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        self.layout3.addWidget(self.label)





        self.resize(pixmap.width(), pixmap.height())


        self.text = QTextBrowser(self)
        #self.text.append("ㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎ")
        self.text2 = QTextBrowser(self)
        #self.text2.append("ㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎ")

        self.text3 = QTextBrowser(self)

        # Add tabs
        self.tabs.addTab(self.tab1, "검색어")


        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab2.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("조회")
        self.pushButton2 = QPushButton("상관관계 분석 ")
        self.pushButton1.clicked.connect(self.on_click)
        self.pushButton2.clicked.connect(self.on_click_comapre)
        self.layout2.addWidget(self.text)
        self.layout2.addWidget(self.text2)



        # self.tab1.layout.addWidget(self.pushButton2)
        self.tab1.layout.addLayout(self.layout3)

        self.tab1.layout.addLayout(self.layout2)
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.layout.addWidget(self.label_2)
        self.tab1.layout.addWidget(self.lineEdit)
        self.tab1.layout.addWidget(self.pushButton2)
        self.tab1.layout.addWidget(self.text3)
        self.tab1.setLayout(self.tab1.layout)


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click_comapre(self):
        global current_temp, current_date
        if current_temp != 350.0:
            try :
                # QMessageBox.about(self, "알림", self.lineEdit.text())
                plt.close()
                plt.close()
                plt.close()
                now = datetime.now()
                current_date = now.strftime('%m/%d')

                client_id = "rTYvYemnK7wtMerTYSvn"
                client_secret = "ZyjmLFSdpp"
                url = "https://openapi.naver.com/v1/datalab/search";
                # ,{\"groupName\":\"영어\",\"keywords\":[\"영어\",\"english\"]}
                keyword = self.lineEdit.text()
                body = "{\"startDate\":\"2018-01-01\",\"endDate\":\"2018-12-31\",\"timeUnit\":\"date\",\"keywordGroups\":[{\"groupName\":\"" + keyword + "\",\"keywords\":[\"" + keyword + "\"]}]}"

                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                request.add_header("Content-Type", "application/json")
                response = urllib.request.urlopen(request, data=body.encode("utf-8"))
                rescode = response.getcode()
                date = []
                ratio = []
                if (rescode == 200):
                    response_body = response.read()
                    str_response = str(response_body.decode('utf-8'))
                    str_response = str_response.split(',')
                    idx = 0
                    for i in str_response:
                        # if "period" in i :
                        #     print(i)
                        # if "ratio" in i :
                        #     print(i)
                        # print(i)
                        n = re.findall('\d+', i)
                        if idx >= 5:
                            if idx % 2 == 1:
                                date.append(n[1] +"/"+ n[2])

                            else:
                                pass
                                # ratio.append(float(n[0] +"."+ n[1]))
                                try:
                                    # print(n[0] +"."+ n[1])
                                    ratio.append(float(n[0] + "." + n[1]))
                                except:
                                    ratio.append(float(100))
                        idx += 1



                    f = open('temp.csv')
                    data = csv.reader(f)
                    header = next(data)
                    result = []
                    temp = []
                    for row in data:
                        # print(row )
                        temp.append(float(row[2]))
                    plt.figure(figsize=(10, 8))
                    plt.rc('font', family='Malgun Gothic')  # 맑은 고딕을 기본 글꼴로 설정
                    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
                    plt.rcParams["xtick.labelsize"] = 7
                    plt.title('데이터 분석 그래프')  # 제목 설정
                    plt.plot(date, ratio, 'black',
                             label="검색 비율 ")  # high 리스트에 저장된 값을 hotpink 색으로 그리고 레이블을 표시
                    # plt.set_xticks(date[::2])
                    plt.xticks(date[::10], rotation=45)
                    # plt.xticks(date, rotation=90)
                    # Pad margins so that markers don't get clipped by the axes
                    plt.margins(0.2)
                    # Tweak spacing to prevent clipping of tick-labels
                    plt.subplots_adjust(bottom=0.2)
                    plt.legend()  # 범례

                    x_maximums = []
                    x_compare = []
                    y_maximums = []
                    maxx = max(ratio)

                    for i in range(2, len(ratio) - 2):
                        if ratio[i] == maxx:
                            y_maximums.append(ratio[i])
                            x_maximums.append(date[i])
                            continue
                        if ratio[i - 2] < ratio[i - 1] and ratio[i - 1] < ratio[i] and ratio[i + 2] < ratio[i + 1] and \
                                ratio[i + 1] < ratio[i]:
                            y_maximums.append(ratio[i])
                            x_maximums.append(date[i])
                    plt.xlabel('날짜')
                    plt.ylabel('검색비율[%] / 온도 [℃]')
                    # plt.scatter(x_maximums, y_maximums, color='red',s = 5 )
                    plt.plot(x_maximums, y_maximums, color='red', label="추세선 ", marker="o", ms=3)
                    # for n in range(len(y_maximums)) :
                    #     if y_maximums[n] >= 0.4 :
                    #         x_compare.append(x_maximums[n])
                    flag = False
                    for n in range(len(date)) :

                        for n2 in range(len(y_maximums)):
                            if date[n] == x_maximums[n2] and y_maximums[n2] >= 40.0 and not flag :
                                flag = True
                            elif date[n] == x_maximums[n2] and y_maximums[n2] < 40.0and flag :
                                flag = False
                        if flag:
                            x_compare.append(date[n])
                    response_com ='<span style=\" color: #ff0000;\">%s</span>' %  "추천하지 않습니다."
                    print(np.corrcoef(temp, ratio))
                    corrr = np.corrcoef(temp, ratio)[0, 1]
                    print(corrr)



                    for n in x_compare :
                        if n == current_date :
                            response_com = '<span style=\" color: #1100ff;\">%s</span>' % "추천합니다"
                            break
                    if corrr > 0.3 and current_temp < 15:
                        response_com ='<span style=\" color: #ff0000;\">%s</span>' %  "추천하지 않습니다."
                    if corrr < -0.3 and current_temp > 15:
                        response_com ='<span style=\" color: #ff0000;\">%s</span>' %  "추천하지 않습니다."
                    self.text3.setText("온도와의 상관관계 : " + str(corrr))
                    self.text3.append("오늘의 날짜와 온도와 트렌드를 종합해 봤을때 " +  keyword + "(을)를 ")
                    self.text3.append(response_com)


                    plt.axvline(x=current_date, color='r', linestyle='--', linewidth=1, label='오늘의 날짜: ' + current_date)

                    plt.plot(date, temp, 'green',
                             label="평균온도 ")  # high 리스트에 저장된 값을 hotpink 색으로 그리고 레이블을 표시
                    # plt.set_xticks(date[::2])

                    # plt.xticks(date, rotation=90)
                    # Pad margins so that markers don't get clipped by the axes

                    plt.legend()  # 범례

                    plt.figure(figsize=(10, 8))
                    fp1 = np.polyfit(temp, ratio, 1)
                    f1 = np.poly1d(fp1)
                    plt.title('상관관계 분석')
                    plt.xlabel('온도')
                    plt.ylabel('검색횟수')
                    plt.plot(temp, f1(temp), lw=2, color='green', label='회귀직선')
                    plt.axvline(x=current_temp, color='r', linestyle='--', linewidth=1, label='오늘의 온도: ' + str(current_temp))
                    plt.scatter(temp, ratio)
                    plt.legend()
                    plt.show()

                else:
                    print("Error Code:" + rescode)
            except :
                print("ERROR")
                QMessageBox.about(self, "알림", "에러가 발생했습니다. 인터넷 연결이 끊겼거나 검색 데이터가 없는 단어입니다.")
                self.text3.setText("")
        else :
            print("ERROR")
            QMessageBox.about(self, "알림", "조회를 눌러주세요.")


    def on_click(self):
        global current_temp, current_date
        ## naver
        try:
            now = datetime.now()
            nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
            self.text.setText("")
            self.text2.setText("")
            self.text2.append("현재시간: " + nowDatetime)
            cloth_url = "https://search.shopping.naver.com/best100v2/detail/kwd.nhn?catId=50000000&kwdType=KWD"

            html = requests.get(cloth_url).text
            soup = BeautifulSoup(html, 'html.parser')

            cloth_list = soup.find_all('a',
                                      '_popular_srch_lst_rank')  # ol의 tag중 list_hotissue  class 중 a tag중  link_issue class 읽어오기

            d_word_list = []
            for title in cloth_list:
                d_word_list.append(title.text.strip())

            # 결과 확인
            i = 1
            for searchword in d_word_list:
                # print(searchword)
                self.text.append(str(i) + ". " + searchword)
                i += 1

            temp_url = "https://weather.naver.com/period/weeklyFcast.nhn"

            html = requests.get(temp_url).text
            soup = BeautifulSoup(html, 'html.parser')

            temp_list = soup.find("td", "line")  # ol의 tag중 list_hotissue  class 중 a tag중  link_issue class 읽어오기

            self.text2.append("["+'<span style=\" color: #ff0000;\">%s</span>' %"이번주 날씨"+"]\n")
            self.text2.append(temp_list.text)

            curtemp_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%ED%98%84%EC%9E%AC+%EB%82%A0%EC%94%A8"

            html = requests.get(curtemp_url).text
            soup = BeautifulSoup(html, 'html.parser')

            cur_list = soup.find("div", "main_info")  # ol의 tag중 list_hotissue  class 중 a tag중  link_issue class 읽어오기

            self.text2.append("[" + '<span style=\" color: #1100ff;\">%s</span>' % "현재 날씨" + "]\n")
            self.text2.append(cur_list.text)
            # 결과 확인
            current_temp = float(re.findall('\d+', cur_list.text)[0])
            print(current_temp)
        except:
            print("ERROR")
            QMessageBox.about(self, "알림", "에러가 발생했습니다. 인터넷 연결을 확인하고 다시 시도해주세요")




if __name__ == '__main__':
    current_temp = 350.0
    current_date = ""
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())