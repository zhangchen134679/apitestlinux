from middleware.middle_pre_back.middle_query import handler_middle
from common.handler_requests import visit
import unittest
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_kie

cases = excel.read_data("query_offline_trade_count")


@ddt.ddt
class TestQueryOfflineTradeCount(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["kie"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"]["kie"]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"]["kie"]["password"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

    @ddt.data(*cases)
    def test_query_offline_trade_count(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的value值
        data_info = handler_middle.Handler().replace_data(self.brand, str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])
# --------------------------------------------------------------------------------------------------------------------
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler_middle.Handler.yml_conf["host"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in eval(data_info["expect_response"]).items():
                # print(self.v, actual[self.k])
                self.assertTrue(self.v == actual[self.k])

            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))

        except Exception as err:
            self.result = "fail"

            logger.warning("data: {}".format(data))
            logger.warning("response: {}".format(actual))
            logger.error("第{}条用例失败, 预期结果: {}, 实际结果: {}".format(data_info["case_id"], self.v, actual[self.k]))

            print("data: {}".format(data))
            print("response: {}".format(actual))
            print("第{}条用例失败, 预期结果: {}, 实际结果: {}".format(data_info["case_id"], self.v, actual[self.k]))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()



