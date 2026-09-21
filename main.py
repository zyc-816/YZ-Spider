import config
from core import DataSpider
from core import Authenticator
from utils import logger

login = Authenticator()
login.login("15371040816", "Zyc$0816")
spider = DataSpider(login.session)
spider.run("网络与信息安全")