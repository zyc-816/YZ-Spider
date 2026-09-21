import sys

import requests
from bs4 import BeautifulSoup

import config
from utils import delay, logger


class Authenticator:
    def __init__(self):
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        self.session.headers.update({
            "User-Agent": config.UA,
            # "Referer": config.LOGIN_URL,
            "Origin": config.ROOT_URL
        })

    def login(self, account = config.ACCOUNT, password = config.PASSWORD) -> None:
        # get session
        logger.info("尝试获取登录页面...")
        try:
            page = self.session.get(config.LOGIN_URL, timeout=config.TIMEOUT)
            page.raise_for_status()
            delay()
        except Exception as e:
            logger.critical("登录页面无法访问：{e}")
            sys.exit(1)

        # parse lt and execution value
        try:
            soup = BeautifulSoup(page.text, "html.parser")
            lt = soup.select_one('input[name="lt"]').get("value")
            execution = soup.select_one('input[name="execution"]').get("value")
        except Exception as e:
            logger.critical("无法解析页面：{e}")
            sys.exit(1)

        # login
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
                timeout=config.TIMEOUT
            )
            login.raise_for_status()
            if "您输入的用户名或密码有误" in login.text:
                logger.error("账号或密码有误")
                sys.exit(1)
            else:
                logger.info("登录成功")
            delay()
        except Exception as e:
            logger.critical("登录请求失败：{e}")
            sys.exit(1)