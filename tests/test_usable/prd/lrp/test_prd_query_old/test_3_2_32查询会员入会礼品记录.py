from middleware.middle_prd.middle_query import handler_middle
from common.handler_requests import visit
import unittest
import pytest
import allure
import json
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_query_common

cases = excel.read_data("query_member_gift_record")


@pytest.mark.lrp
@ddt.ddt
class TestQueryMemberGiftRecord(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lancome"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler.headers(brand_code=cls.brand)

        # 从配置文件读取test_member_data
        cls.conf_member_data = handler_middle.Handler.yml_conf["test_member_data"][cls.brand]

        # 调用会员注册接口
        cls.register_member = handler_middle.register_member(cls.brand, headers=cls.headers)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用会员退会接口
        handler_middle.quit_member(cls.brand, value=cls.register_member["data"]["union_code"], headers=cls.headers)

    @allure.step("查询会员入会礼品记录")
    @pytest.mark.query
    @pytest.mark.query_member_gift_record
    @ddt.data(*cases)
    def test_query_member_gift_record(self, data_info):
        allure.dynamic.title(str(data_info['title']))
        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的union_code
        data_info = re.sub("&union_code&", self.conf_member_data["union_code"], data_info)
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中没有入会礼品的union_code
        data_info = re.sub(r"&not_gift_union_code&", self.register_member["data"]["union_code"], str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 转化数据格式
        data_info = eval(data_info)
        data = eval(data_info["data"])
# --------------------------------------------------------------------------------------------------------------------
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler_middle.Handler.yml_conf["host"] + data_info["url"],
                       method="post",
                       json=data,
                       headers=self.headers)
        print(actual)

        expect_response = json.loads(data_info["{}_expect_response".format(self.brand)])

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():

                if self.k in "data" and actual["code"] == 0:
                    for self.key, self.value in self.v.items():
                        # print(self.value, actual[self.k][self.key])
                        self.assertEqual(self.value, actual[self.k][self.key])

                else:
                    # print(self.v, actual[self.k])
                    self.assertTrue(self.v == actual[self.k])

            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))

        except AssertionError as err:
            self.result = "fail"
            logger.error("data: {}".format(data))
            logger.error("response: {}".format(actual))
            logger.error("第{}条用例失败..Fail...Expected, Actual{}".format(data_info["case_id"], err))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()

