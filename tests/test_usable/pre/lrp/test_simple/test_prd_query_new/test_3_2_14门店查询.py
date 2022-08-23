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

cases = excel.read_data("query_store")

handler = handler_middle.Handler


@pytest.mark.lrp
@ddt.ddt
class TestQueryStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrp"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler.headers(brand_code=cls.brand)

    @allure.step("门店查询")
    @pytest.mark.query
    @pytest.mark.query_store
    @ddt.data(*cases)
    def test_query_store(self, data_info):
        allure.dynamic.title(str(data_info['title']))
        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的store_code
        data_info = re.sub(r"&store_code&", handler.yml_conf["crm_store"][self.brand]["deal_store_no"], str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 转化数据格式
        data_info = eval(data_info)
        data = eval(data_info["data"])
# --------------------------------------------------------------------------------------------------------------------
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler.yml_conf["host"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)

        expect_response = json.loads(data_info["{}_expect_response".format(self.brand)])
        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():

                if self.k in "data" and actual["code"] == 0 and data_info["case_id"] != 7:
                    logger.info("第{}条用例againAssert...".format(data_info["case_id"]))
                    for i, j in enumerate(expect_response[self.k]):
                        for self.key, self.value in self.v[i].items():
                            self.assertEqual(self.value, actual[self.k][i][self.key])
                            # print(self.value, actual[self.k][i][self.key])

                    # 门店data数据不为空
                    self.assertTrue(actual["data"])

                else:
                    # print(self.v, actual[self.k])
                    self.assertEqual(self.v, actual[self.k])

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
