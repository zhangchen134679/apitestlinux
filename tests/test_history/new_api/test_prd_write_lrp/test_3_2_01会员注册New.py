from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import pytest
import allure
import json
import time
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_mny

cases = excel.read_data("member_registerNew")


@pytest.mark.lrp
@ddt.ddt
class TestMemberRegisterNew(unittest.TestCase):

    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrp"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 从配置文件读取天猫店铺名称
        cls.tb_store_name = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["name"]

        # 从配置文件读取store_code
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]
# --------------------------------------------------------------------------------------------------------------------
        """
        :param repetition: 通过setUpClass生成一次mobile..具体替换数据见line105
               repetition: 通过setUpClass生成一次jdPin.openId.nickname.encryptMobile..具体替换数据见line108
            """
        cls.repetition_mobile = handler_middle.Handler().random_phone(cls.brand, headers=cls.headers)
        cls.repetition_jdPin = "repetition_jdPin_" + handler_middle.Handler().random_num
        cls.repetition_openId = "repetition_openId_" + handler_middle.Handler().random_num
        cls.repetition_nickname = "repetition_nickname_" + handler_middle.Handler().random_num
        cls.repetition_encryptMobile = "repetition_encryptMobile_" + handler_middle.Handler().random_num
# --------------------------------------------------------------------------------------------------------------------

    def setUp(self) -> None:

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用全渠道会员绑定解绑(新)接口
        for index in range(0, len(cls.member_list)):
            bind = handler_middle.MemberBinding(
                cls.brand, binding_type="0", value=cls.member_list[index], headers=cls.headers, query_type="union_code")
            bind.try_bind()

    @allure.step("会员注册New")
    @pytest.mark.write
    @pytest.mark.member_registerNew
    @ddt.data(*cases)
    def test_member_registerNew(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的mobile
        data_info = re.sub(r"#random_mobile#", handler_middle.
                           Handler().random_phone(self.brand, headers=self.headers), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的store_code
        data_info = re.sub(r"#store_code#", self.store_code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的fromSocialCode -- 入会渠道为天猫
        data_info = re.sub(r"#tb_store_name#", self.tb_store_name, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的jd_pin -- 入会渠道为京东
        data_info = re.sub(r"#random_JDpin#", "jd_pin" + handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的openId -- 入会渠道为微信
        data_info = re.sub(r"#random_openId#", "open_id" + handler_middle.Handler().random_num, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的nickname -- 入会渠道为天猫
        data_info = re.sub(r"#random_nickname#", "nickname_" + handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        """
        :param repetition_mobile: case01, case11..使用同一个mobile
        :param repetition_jdPin: case29, case61..使用同一个jdPin
        :param repetition_openId: case28, case60..使用同一个openId
        :param repetition_nickname: case30, case63..使用同一个nickname
        :param repetition_encryptMobile：  case31, case62..使用同一个encryptMobile
            """
        # 替换用例中的repetition_mobile
        data_info = re.sub(r"#repetition_mobile#", self.repetition_mobile, str(data_info))

        # 替换用例中的repetition_jdPin
        data_info = re.sub(r"#repetition_jdPin#", self.repetition_jdPin, str(data_info))

        # 替换用例中的repetition_openId
        data_info = re.sub(r"#repetition_openId#", self.repetition_openId, str(data_info))

        # 替换用例中的repetition_nickname
        data_info = re.sub(r"#repetition_nickname#", self.repetition_nickname, str(data_info))

        # 替换用例中的repetition_encryptMobile
        data_info = re.sub(r"#repetition_encryptMobile#", self.repetition_encryptMobile, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 转化数据格式
        data_info = eval(data_info)
        data = eval(data_info["data"])
#  --------------------------------------------------------------------------------------------------------------------
        # sleep 10s.
        """场景需要,强制等待10秒后访问接口"""
        if data_info["case_id"] in (11, 60):
            time.sleep(10)
#  --------------------------------------------------------------------------------------------------------------------
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler_middle.Handler.yml_conf["host"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)

        expect_response = json.loads(data_info["expect_response"])

        try:
            if actual["code"] == 0:
                self.member_list.append(actual["data"]["union_code"])
        except Exception as err:
            logger.error("member_list.appendError..{}".format(actual))
            raise err

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













