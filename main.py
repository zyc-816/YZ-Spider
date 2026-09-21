import getpass

from core import Authenticator, DataSpider, ExcelPipeline
from utils import logger

# login
account = input("账户：")
password = getpass.getpass("密码：")
login = Authenticator()
login.login(account, password)

# select major
major = input("专业：")
spider = DataSpider(login.session)
data, major_code, major_name = spider.run(major)

# output
excel = ExcelPipeline(data, major_code, major_name)
excel.run()