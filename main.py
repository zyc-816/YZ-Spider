import json
from core import ExcelPipeline
import config
from core import DataSpider
from core import Authenticator
from utils import logger


# login = Authenticator()
# login.login("15371040816", "Zyc$0816")
# spider = DataSpider(login.session)
# data = spider.run("网络与信息安全")

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

excel = ExcelPipeline(data, 1, "11")
excel.run()