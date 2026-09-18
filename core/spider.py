from urllib import response

import requests
import sys
import config
from typing import Dict, List, Any, Optional
from utils import logger
from utils import delay


class DataSpider:
    def __init__(self, session: requests.Session):
        self.session = session
        self.timeout = getattr(config, "TIMEOUT", 10)
        self.max_retries = getattr(config, "MAX_RETRIES", 3)

    def _request(
        self, url: str, method="POST", **kwargs
    ) -> Optional[requests.Response]:
        kwargs.setdefault("timeout", config.TIMEOUT)
        for attempt in range(1, config.MAX_RETRIES + 1):
            try:
                response = self.session.request(method=method, url=url, **kwargs)
                response.raise_for_status()
                delay()
                return response
            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"请求失败 [URL: {url}]，重试第 {attempt}/{config.MAX_RETRIES} 次: {e}"
                )
                if attempt == self.max_retries:
                    logger.critical(f"请求失败: {url}")
                    sys.exit(1)
        return None


    def run(self, major_code: str, major_name: str) -> List[Dict[str, Any]]:
        # get sign and sign2 value
        try:
            sign_payload = {
                "zydm": major_code,
                "zymc": major_name,
                "xwlx": "",
                "mldm": "",
                "yjxkdm": "",
                "xxfs": "",
                "tydxs": "",
                "jsggjh": "",
                "start": 0,
                "curPage": 1,
                "pageSize": 20,
                "totalPage": 0,
                "totalCount": 0
            }
            sign_respose = self._request(url=config.SIGN_URL, method="POST", data=sign_payload)
            sign_json = sign_respose.json()
            sign_list = sign_json.get("msg", {}).get("list", [])
            sign = sign_list[0].get("sign")
            sign2 = sign_list[0].get("sign2")
            print(sign)
            print(sign2)
        except Exception as e:
            logger.critical("获取sign失败：{e}")
            sys.exit(1)

        return []