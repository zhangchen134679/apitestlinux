from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import json
import time
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_shu

cases = excel.read_data("member_register")


@ddt.ddt
class TestMemberRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["shu"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"][cls.brand]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"][cls.brand]["password"]

        # 从配置文件读取天猫店铺名称
        cls.tb_store_name = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["name"]

        # 从配置文件读取deal_store_no
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

        # 生成当前时间并转化格式
        cls.time = time.strftime("%Y-%m-%d %H:%M:%S")

    def setUp(self) -> None:

        # 调用随机生成11位手机号..
        self.mobile = handler_middle.Handler().random_phone(self.brand, headers=self.headers)

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    def tearDown(self) -> None:
        # 调用全渠道会员绑定解绑(新)接口
        bind = handler_middle.MemberBinding(
            self.brand, binding_type="0", value=self.mobile, headers=self.headers, query_type="mobile")
        bind.try_bind()

    @ddt.data(*cases)
    def test_member_register(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的mobile
        data_info = re.sub(r"#mobile#", self.mobile, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的consentTime
        data_info = re.sub(r"#time#", self.time, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的store_code
        data_info = re.sub(r"#store_code#", self.store_code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的fromSocialCode -- 入会渠道为天猫
        data_info = re.sub(r"#tb_store_name#", self.tb_store_name, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的nickname -- 入会渠道为天猫
        data_info = re.sub(r"#nickname#", "nickname" + str(int(time.time())), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的accountNo -- 入会渠道为天猫
        data_info = re.sub(r"#accountNo#", "account_" + str(int(time.time())), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的jd_pin -- 入会渠道为京东
        data_info = re.sub(r"#JDpin#", "jd_pin" + str(int(time.time())), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的openId -- 入会渠道为微信
        data_info = re.sub(r"#openId#", "open_id" + str(int(time.time())), str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 转化数据格式
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

                try:
                    self.assertEqual(self.v, actual[self.k])

                except AssertionError as err:
                    logger.error("Fail...Expected, Actual{}".format(err))
                    raise err

                if actual[self.k] == 0:
                    # 调用查询会员基本信息
                    actual_member = handler_middle.query_member_info(
                        self.brand, value=data["mobile"], headers=self.headers, query_type="mobile")

                    try:
                        # KeyError: 'data' 可能是因为注册成功的会员没有入库, 查询不到此会员信息...
                        self.assertTrue(actual_member["data"])

                    except KeyError as err:
                        logger.error("againAssertFail...KeyError: 'data'")
                        logger.error("没有查询到会员...{}".format(actual_member))
                        print("没有查询到会员...{}".format(actual_member))
                        raise err

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
