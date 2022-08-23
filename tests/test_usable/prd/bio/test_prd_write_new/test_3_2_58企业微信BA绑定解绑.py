from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import pytest
import allure
import json
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_write_common

cases = excel.read_data("wechat_ba_bind")


@pytest.mark.bio
@ddt.ddt
class TestWechatBaBind(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["bio"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 调用会员注册接口
        cls.register_wechat = handler_middle.register_wechat(cls.brand, headers=cls.headers)

        # 提取会员union_code
        cls.union_code = cls.register_wechat["data"]["union_code"]

    def setUp(self) -> None:

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用全渠道会员绑定解绑(新)接口
        cls.bind = handler_middle.MemberBinding(cls.brand, binding_type="0", value=cls.union_code, headers=cls.headers)
        cls.bind.wx_bind(channel="6P0")
        cls.bind.quit_member()

    @allure.step("企业微信BA绑定解绑")
    @pytest.mark.write
    @pytest.mark.wechat_ba_bind
    @ddt.data(*cases)
    def test_wechat_ba_bind(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的baUserId
        data_info = re.sub(r"&baUserId&", handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的cusUserId
        replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
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
                # print(self.v, actual[self.k])
                self.assertEqual(self.v, actual[self.k])

            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))

        except Exception as err:
            self.result = "fail"
            logger.warning("data: {}".format(data))
            logger.warning("response: {}".format(actual))
            logger.error("第{}条用例失败".format(data_info["case_id"]))

            print("data: {}".format(data))
            print("response: {}".format(actual))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()


