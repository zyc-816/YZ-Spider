import sys
import requests
import config
from utils import logger
from utils import delay
from bs4 import BeautifulSoup


class Authenticator:
    def __init__(self):
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        self.session.headers.update({
            "User-Agent": config.UA,
            "Referer": config.LOGIN_URL,
            "Origin": config.ROOT_URL
        })

    def login(self, account = config.ACCOUNT, password = config.PASSWORD) -> None:
        logger.info("尝试获取登录页面...")
        try:
            page = self.session.get(config.LOGIN_URL, timeout=10)
            page.raise_for_status()
            delay()
        except Exception as e:
            logger.critical("登录页面无法访问")
            sys.exit(1)
        try:
            soup = BeautifulSoup(page.text, "html.parser")
            lt = soup.select_one('input[name="lt"]').get("value")
            logger.info("lt: {lt}")
            execution = soup.select_one('input[name="execution"]').get("value")
            logger.info("execution: {excution}")
        except Exception as e:
            logger.critical("无法解析页面")
            sys.exit(1)

        logger.info("开始登录...")
        try:
            payload = {
                "username": account,
                "password": password,
                "lt": lt,
                "execution": execution,
                "_eventId": "submit"
            }
            login = self.session.post(
                url=config.LOGIN_URL,
                data=payload,
                timeout=10
            )
            login.raise_for_status()
            if "您输入的用户名或密码有误" in login.text:
                logger.error("账号或密码有误")
                sys.exit(1)
            else:
                logger.info("登录成功")
            delay()
        except Exception as e:
            logger.critical("登录请求失败")
            sys.exit(1)