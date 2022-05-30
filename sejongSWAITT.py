# 텔레그램 봇 모듈
import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# 토큰 값
TOKEN = '5315531917:AAHP327DA0psYL4LCUy6c0SxgP1c1P2s3yc'
# 채팅방 ID
now_id = 5278049092

# 텔레그램 봇 세팅
bot = telegram.Bot(token=TOKEN)
updates = bot.getUpdates()
updater = Updater(token=TOKEN, use_context=True)  # 봇에게 들어온 메시지가 있는지 체크


class command:
    def start(update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='🇰🇷 안녕하세요 13조 시간표 추천 서비스\n\n사용하고자 하는 것을 입력하세요\n/whoami: 소개\n/howtouse: 사용 방법\n')

    def whoami():
        pass

    def howtouse():  # 엑셀 파일 넣어주세요
        pass

    def user_input():
        pass

    def need_advice(update, context):   # 추가되는 부분
        pass

    def downloader(update, context):
        context.bot.get_file(update.message.document).download()
        # writing to a custom file
        with open("custom/file.doc", 'wb') as f:
            context.bot.get_file(update.message.document).download(out=f)


dispatcher = updater.dispatcher

# /start입력하면 command.start 실행
start_handler = CommandHandler('start', command.start)
#whoami_handler = CommandHandler('whoami', command.whoami)


updater.dispatcher.add_handler(MessageHandler(
    Filters.document, command.downloader))

dispatcher.add_handler(start_handler)

# 시작
updater.start_polling()
updater.idle()
