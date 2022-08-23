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

cases = excel.read_data("query_wechat_ba_bind")


@pytest.mark.lrp
@ddt.ddt
class TestQueryWechatBaBind(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lancome"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler.headers(brand_code=cls.brand)

        # 从配置文件读取店员ba_code
        cls.ba_code = handler_middle.Handler.yml_conf["crm_employee"][cls.brand]

        # 从配置文件读取店员ba_userid
        cls.ba_userid = handler_middle.Handler.yml_conf["crm_wechat"]["ba_userid"]

        # 调用会员注册接口
        cls.register_member = handler_middle.register_member(cls.brand, headers=cls.headers)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用会员退会接口
        handler_middle.quit_member(cls.brand, value=cls.register_member["data"]["union_code"], headers=cls.headers)

    @allure.step("企业微信BA绑定查询")
    @pytest.mark.query
    @pytest.mark.query_wechat_ba_bind
    @ddt.data(*cases)
    def test_query_wechat_ba_bind(self, data_info):
        allure.dynamic.title(str(data_info['title']))
        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中没有绑定企业微信的union_code
        data_info = re.sub(r"&not_wechat_union_code&", self.register_member["data"]["union_code"], str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的ba_code
        data_info = re.sub(r"&BACODE&", self.ba_code, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的ba_userid
        data_info = re.sub(r"&BAUSERID&", self.ba_userid, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的value值
        data_info = handler_middle.Handler.replace_data(self.brand, str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])
# --------------------------------------------------------------------------------------------------------------------
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler_middle.Handler.yml_conf["host"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)

        expect_response = json.loads(data_info["{}_expect_response".format(self.brand)])
        print(actual)
        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():

                if self.k in "data" and actual["code"] == 0:
                    for index, value in enumerate(self.v):
                        for self.key, self.value in value.items():
                            self.assertEqual(self.value, actual[self.k][index][self.key])

                else:
                    # print(self.v, actual[self.k])
                    self.assertEqual(self.v, actual[self.k])

            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))

        except Exception as err:
            self.result = "fail"
            logger.error("data: {}".format(data))
            logger.error("response: {}".format(actual))
            logger.error("第{}条用例失败..Fail...Expected, Actual{}".format(data_info["case_id"], err))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()





