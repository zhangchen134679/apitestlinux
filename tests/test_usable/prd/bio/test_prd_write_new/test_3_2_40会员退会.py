from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import pytest
import allure
import json
import time
import ddt

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_write_common

cases = excel.read_data("quit_member")


@pytest.mark.bio
@ddt.ddt
class TestQuitMember(unittest.TestCase):

    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["bio"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 调用会员注册接口
        cls.media_register = handler_middle.register_member(cls.brand, headers=cls.headers)

        # 提取会员union_code
        cls.class_media_code = cls.media_register["data"]["union_code"]

        # 调用全渠道会员绑定解绑(新)接口
        cls.bind = handler_middle.MemberBinding(cls.brand, value=cls.class_media_code, headers=cls.headers)

        # 绑定天猫..京东..微信..
        cls.bind.all_bind()

        # union_code insert list
        cls.member_list.append(cls.class_media_code)
# --------------------------------------------------------------------------------------------------------------------

    def setUp(self) -> None:

        # 调用会员注册接口
        self.register = handler_middle.register_member(self.brand, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register["data"]["union_code"]

        # union_code insert list
        self.member_list.append(self.union_code)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用全渠道会员绑定解绑(新)接口
        for index in range(0, len(cls.member_list)):
            bind = handler_middle.MemberBinding(
                cls.brand, binding_type="0", value=cls.member_list[index], headers=cls.headers, query_type="union_code")
            bind.try_bind()

    @allure.step("会员退会")
    @pytest.mark.write
    @pytest.mark.quit_member
    @ddt.data(*cases)
    def test_quit_member(self, data_info):
        """
        if..bind == true
        绑定天猫..京东..微信..
        """
        if data_info["bind"]:
            self.bind = handler_middle.MemberBinding(self.brand, value=self.union_code, headers=self.headers)
            if data_info["bind"] == 976:
                self.bind.tb_bind("976")
            elif data_info["bind"] == "9AL":
                self.bind.jd_bind("9AL")
            elif data_info["bind"] == "6P0":
                self.bind.wx_bind("6P0")
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的data..
        if data_info["case_id"] <= 13 or data_info["case_id"] >= 32:
            replace = handler_middle.ReplaceDate(self.brand, headers=self.headers, value=self.union_code)
            data_info = replace.replace_data(str(data_info))
        else:
            replace = handler_middle.ReplaceDate(self.brand, headers=self.headers, value=self.class_media_code)
            data_info = replace.replace_data(str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])
#  --------------------------------------------------------------------------------------------------------------------
        if data_info["case_id"] >= 32:
            # 调用全渠道会员绑定解绑(新)接口
            self.bind = handler_middle.MemberBinding(
                            self.brand, value=self.union_code, headers=self.headers, binding_type="0")

            if data_info["sleep"]:
                time.sleep(10)

            # 解绑媒体信息退会...
            self.bind.try_bind()

            if data_info["case_id"] == 39:
                time.sleep(10)
#  --------------------------------------------------------------------------------------------------------------------
        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)
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













