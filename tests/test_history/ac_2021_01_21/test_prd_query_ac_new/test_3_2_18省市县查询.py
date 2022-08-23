from middleware.middle_prd.middle_query import handler_middle
from common.handler_requests import visit
import unittest
import pytest
import allure
import json
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_ac

cases = excel.read_data("query_district")


@pytest.mark.ac
@ddt.ddt
class TestQueryDistrict(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["ac"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

    @allure.step("省市县查询")
    @pytest.mark.query
    @pytest.mark.query_district
    @ddt.data(*cases)
    def test_query_district(self, data_info):

        # 替换用例中的data数据
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 转化数据格式
        data_info = eval(data_info)
        data = eval(data_info["data"])
# --------------------------------------------------------------------------------------------------------------------
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler_middle.Handler.yml_conf["host"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)

        expect_response = json.loads(data_info["expect_response"])

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():

                if self.k in "data" and actual["code"] == 0 and data_info["case_id"] != 10:
                    for i, j in enumerate(expect_response[self.k]):
                        for self.key, self.value in self.v[i].items():
                            # print(self.value, actual[self.k][i][self.key])
                            self.assertEqual(self.value, actual[self.k][i][self.key])

                    # 地区data数据不为空
                    self.assertTrue(actual["data"])

                else:
                    # print(self.v, actual[self.k])
                    self.assertEqual(self.v, actual[self.k])

            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))

        except Exception as err:
            self.result = "fail"
            logger.warning("data: {}".format(data))
            logger.warning("response: {}".format(actual))
            logger.error("第{}条用例失败..Fail...Expected, Actual{}".format(data_info["case_id"], err))

            print("data: {}".format(data))
            print("response: {}".format(actual))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()



