import requests
import sys
import config
import time
import json
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
            except Exception as e:
                logger.warning(
                    f"请求失败 [URL: {url}]，重试第 {attempt}/{config.MAX_RETRIES} 次: {e}"
                )
                if attempt == self.max_retries:
                    logger.critical(f"请求失败: {url}")
                    sys.exit(1)
        return None


    def run(self, key_word: str) -> List[Dict[str, Any]]:
        # search key_word
        try:
            search_payload = {
                "q": key_word,
                "_t": time.time_ns() // 1_000_000
            }
            search_response = self._request(url=config.SEARCH_URL, method="GET", params=search_payload)
            search_result = search_response.json()

            if len(search_result) == 0:
                logger.warning("关键词无对应专业")
                sys.exit(1)
            elif len(search_result) == 1:
                major_code = search_result[0].get("dm")
                major_name = search_result[0].get("mc")
                logger.info(f"已选专业：({major_code}) {major_name}")
            else:
                print("搜索结果：")
                for index, major in enumerate(search_result, start=0):
                    code = major.get("dm")
                    name = major.get("mc")
                    print(f"{index}：({code}) {name}")
                select = int(input("输入对应序号选择："))
                major_code = search_result[select].get("dm")
                major_name = search_result[select].get("mc")
                logger.info(f"已选专业：({major_code}) {major_name}")
        except Exception as e:
            logger.critical(f"获取专业失败：{e}")
            sys.exit(1)

        # get major detail
        try:
            logger.info("正在获取专业详情...")
            get_detail_payload = {
                "zydm": major_code,
                "zymc": major_name,
                "dwmc": "",
                "dwdm": "",
                "ssdm": "",
                "xxfs": "",
                "dwlxs[0]": "all",
                "tydxs": "",
                "jsggjh": "",
                "start": 0,
                "curPage": 1,
                "pageSize": 20,
                "totalPage": 0,
                "totalCount": 0
            }
            get_detail_response = self._request(url=config.SCHOOL_LIST_URL, method="POST", data=get_detail_payload)
            get_detail_json = get_detail_response.json()

            msg = get_detail_json.get("msg")
            page_size = msg.get("size")
            total_page = msg.get("totalPage")
            total_count = msg.get("totalCount")

            detail_content = msg.get("list")[0]
            xwlx = detail_content.get("xwlx")
            mldm = detail_content.get("mldm")
            mlmc = detail_content.get("mlmc")
            yjxkdm = detail_content.get("yjxkdm")
            yjxkmc = detail_content.get("yjxkmc")

            logger.info("获取专业详情成功")
        except Exception as e:
            logger.critical(f"获取专业详情失败：{e}")
            sys.exit(1)

        # update login status
        try:
            logger.info("正在刷新登录状态...")
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
            sign_response = self._request(url=config.SIGN_URL, method="POST", data=sign_payload)
            sign_json = sign_response.json()
            sign_list = sign_json.get("msg", {}).get("list", [])
            sign = sign_list[0].get("sign")
            sign2 = sign_list[0].get("sign2")
            logger.info("刷新登录状态完成")
        except Exception as e:
            logger.critical("刷新登录状态失败：{e}")
            sys.exit(1)

        # get main page
        try:
            logger.info("开始获取主页面...")
            main_page_payload = {
                "zydm": major_code,
                "zymc": major_name,
                "xwlx": xwlx,
                "mldm": mldm,
                "mlmc": mlmc,
                "yjxkdm": yjxkdm,
                "yjxkmc": yjxkmc,
                "xxfs": "",
                "tydxs": "",
                "jsggjh": "",
                "sign": sign
            }
            main_page_response = self._request(url=config.MAIN_URL, method="GET", params=main_page_payload)
            logger.info("获取主页面成功")
        except Exception as e:
            logger.critical(f"获取主页面失败: {e}")
            sys.exit(1)

        # get school list
        try:
            logger.info("开始获取学校列表...")
            school_list = []
            for p in range(0, total_page):
                school_list_page_payload = {
                    "zydm": major_code,
                    "zymc": major_name,
                    "dwmc": "",
                    "dwdm": "",
                    "ssdm": "",
                    "xxfs": "",
                    "dwlxs[0]": "all",
                    "tydxs": "",
                    "jsggjh": "",
                    "start": page_size * p,
                    "curPage": p + 1,
                    "pageSize": page_size,
                    "totalPage": total_page,
                    "totalCount": total_count
                }
                school_list_page_response = self._request(url=config.SCHOOL_LIST_URL, method="POST", data=school_list_page_payload)
                school_list_page = school_list_page_response.json().get("msg").get("list")
                school_list.extend(school_list_page)
                logger.info(f"获取第{p+1} / {total_page}页成功")

            # test
            file_path = "list.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(school_list, f, ensure_ascii=False, indent=2)

            logger.info("获取学校列表成功")
        except Exception as e:
            logger.critical(f"获取学校列表失败：{e}\n{school_list_page_response.json()}")
            sys.exit(1)

        # get school detail by school list
        school_detail_list = []
        try:
            for index, s in enumerate(school_list, start=1):
                school_detail_payload = {
                    "zydm": major_code,
                    "zymc": major_name,
                    "dwdm": s.get("dwdm"),
                    "xxfs": "",
                    "dwlxs[0]": "all",
                    "tydxs": "",
                    "jsggjh": "",
                    "start": 0,
                    "pageSize": 5,
                    "totalCount": 0
                }
                school_detail_response = self._request(url=config.SCHOOL_DETAIL_URL, method="POST", data=school_detail_payload)
                school_detail = school_detail_response.json().get("msg").get("list")         
                school_detail_list.extend(school_detail)
                logger.info(f"获取第{index} / {len(school_list)}个学校详情成功")

            logger.info("获取学校详情成功")
        except Exception as e:
            logger.critical("获取学校详情失败")
            sys.exit(1)

        # test
        file_path = "data.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(school_detail_list, f, ensure_ascii=False, indent=2)

        return school_detail_list