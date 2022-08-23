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

cases = excel.read_data("query_bind_info")


@pytest.mark.ac
@ddt.ddt
class TestQueryBindInfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["ac"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 从配置文件读取天猫店铺名称
        cls.seller_name = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["name"]

        # 从配置文件读取deal_store_no
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]

    @allure.step("全渠道会员绑定状态查询")
    @pytest.mark.query
    @pytest.mark.query_bind_info
    @ddt.data(*cases)
    def test_query_bind_info(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的seller_name
        data_info = re.sub(r"#tb_seller_name#", self.seller_name, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未注册的mobile
        data_info = re.sub(r"#not_register_mobile#", handler_middle.
                           Handler().random_phone(self.brand, self.headers), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未绑定的open_id
        data_info = re.sub(r"#not_bind_open_id#", handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未注册的mix_mobile
        data_info = re.sub(r"#not_register_mix_mobile#", handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未绑定的天猫昵称
        data_info = re.sub(r"#not_bind_taobao_nick#", handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未绑定的京东pin
        data_info = re.sub(r"#not_bind_jd_pin#", handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的value值
        data_info = handler_middle.Handler().replace_data(self.brand, str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])
#  --------------------------------------------------------------------------------------------------------------------
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


