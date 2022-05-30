import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
import openpyxl
import time
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# 토큰 값
token = '5315531917:AAHP327DA0psYL4LCUy6c0SxgP1c1P2s3yc'
# 채팅방 ID
id = 5278049092

# 텔레그램 봇 세팅
bot = telegram.Bot(token=token)
updates = bot.getUpdates()
updater = Updater(token=token, use_context=True)  # 봇에게 들어온 메시지가 있는지 체크
dispatcher = updater.dispatcher

# 리스트
all_lecs = list()       # 소프트웨어학과 개설된 모든 강의 리스트(초기)
all_lecs2 = list()      # 중복 과목 제거한 소프트웨어학과 모든 강의 리스트(최종)
taken_lecs = list()     # 수강완료된 강의 리스트(초기)
taken_lecs2 = list()    # 수강완료된 강의 리스트(초기)
taken_lecs3 = list()    # 수강완료된 강의 리스트(최종)
untaken_lecs = list()   # 수강하지 않은 강의 리스트
grades = list()         # 수강완료된 강의들의 학점 리스트(초기)
grades2 = list()        # 수강완료된 강의들의 학점 리스트(최종)
wanted_lecs = list()    # 가장 듣고 싶은 3가지 강의 리스트
importances = list()    # 중요도 1순위~5순위 리스트
columns = ["교수", "수업", "과제", "시험", "학점"]  # 교수, 수업, 과제, 시험, 학점 중요도 리스트

# 소프트웨어학과 강의시간표에서 중복 강의 제거한 모든 강의 추출
df3 = pd.read_excel("all_lecs.xlsx")
df3 = df3.iloc[:, [4]]  # 과목명 열 추출
df3 = df3.iloc[2:]  # 필요한 값만 추출
df3 = pd.DataFrame(df3)
df3.to_excel("all_lecs2.xlsx", index=False)  # 추출한 데이터프레임을 다시 저장
df4 = pd.read_excel("all_lecs2.xlsx")
all_lecs = df4.iloc[:, 0]
for i in all_lecs:
    if i not in all_lecs2:
        all_lecs2.append(i)


class command:
    def start(update, context):
        name = update.message.chat.first_name
        update.message.reply_text(
            "🇰🇷 안녕하세요 " + name + "님 13조 시간표 추천 서비스입니다\n먼저 본인의 기이수성적파일을 업로드 하세요.")

    def information_input(update, context):
        update.message.reply_text(
            "잠시만 기다려 주세요.")
        if ',' in update.message.text:
            wanted_lecs = update.message.text.split(', ')
            update.message.reply_text("가장 듣고 싶은 강의:")
            for i in wanted_lecs:
                update.message.reply_text(i)
        else:
            importances = list(update.message.text)
            for i, j in zip(importances, columns):
                update.message.reply_text(j + " : " + i + "순위")

    def file_downloader(update, context):
        context.bot.get_file(update.message.document).download('file.xlsx')
        # 받은 기이수성적파일에서 과목명이랑, 성적 추출
        df1 = pd.read_excel("file.xlsx")
        df1 = df1.iloc[:, [4, 10]]
        df1 = df1.iloc[3:]
        df1 = pd.DataFrame(df1)
        df1.to_csv("file.csv", index=False)  # 추출한 데이터프레임을 다시 저장
        df2 = pd.read_csv("file.csv")
        taken_lecs = df2.iloc[:, 0]
        grades = df2.iloc[:, 1]

        taken_lecs2 = list(taken_lecs)
        grades2 = list(grades)

        for i, j in zip(taken_lecs2, grades2):
            if j == 'F':
                continue    # 수강한 강의 중 F학점이 있다면 수강한 강의에 추가 X
            else:
                if i not in taken_lecs3:
                    taken_lecs3.append(i)  # F학점이 아니라면 추가

        # 수강하지 않은 과목 리스트
        untaken_lecs = [x for x in all_lecs2 if x not in taken_lecs3]

        update.message.reply_text("파일 업로드 완료")
        update.message.reply_text("듣지 않은 과목들:")
        j = 1
        for i in untaken_lecs:
            update.message.reply_text(str(j) + ". " + i)
            j = j + 1
        update.message.reply_text(
            "1. 듣지 않은 과목 중, 가장 듣고 싶은 과목 3개를 입력하세요.\n2. 교수, 수업, 과제, 시험, 학점 중에서 순서대로 1순위부터 5순위까지 입력해주세요.\n\n예시)\n멀티미디어프로그래밍, 가상현실, 패턴인식\n35421")

    def image_downloader(update, context):
        context.bot.get_file(
            update.message.photo[0].file_id).download('image.jpg')
        update.message.reply_text("이미지 업로드 완료")


dispatcher.add_handler(CommandHandler('start', command.start))

# MessageHandler
dispatcher.add_handler(MessageHandler(
    Filters.text, command.information_input))
dispatcher.add_handler(MessageHandler(
    Filters.document, command.file_downloader))
dispatcher.add_handler(MessageHandler(
    Filters.photo, command.image_downloader))

# 시작
updater.start_polling()
updater.idle()
