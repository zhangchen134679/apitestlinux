from middleware.middle_pre_apitest_back.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import json
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_kie

cases = excel.read_data("member_regAndBind")


@ddt.ddt
class TestMemberRegAndBind(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["kie"]

        # 从配置文件读取天猫店铺名称
        cls.tb_store_name = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["name"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"][cls.brand]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"][cls.brand]["password"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

        # 用来替换用例数据时传入的store_code参数...
        cls.replace_store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["replace_deal_store_no"]

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
    def test_member_regAndBind(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的mobile
        data_info = re.sub(r"#mobile#", self.mobile, str(data_info))
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的store_code
        data_info = re.sub(r"#store_code#", self.replace_store_code, str(data_info))
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的fromSocialCode -- 入会渠道为天猫
        data_info = re.sub(r"#tb_store_name#", self.tb_store_name, str(data_info))
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的nickname -- 入会渠道为天猫
        data_info = re.sub(r"#nickname#", "nickname" + handler_middle.Handler().random_num, str(data_info))
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的accountNo -- 入会渠道为天猫
        data_info = re.sub(r"#accountNo#", "account_" + handler_middle.Handler().random_num, str(data_info))
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的jd_pin -- 入会渠道为京东
        data_info = re.sub(r"#JDpin#", "jd_pin" + handler_middle.Handler().random_num, str(data_info))
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的openId -- 入会渠道为微信
        data_info = re.sub(r"#openId#", "open_id" + handler_middle.Handler().random_num, str(data_info))
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

                if self.k in "data" and actual["code"] == 0:

                    for self.key, self.value in self.v.items():
                        """
                        assertEqual...
                        action, bindCode, status
                                                """
                        # print(self.value, actual[self.k][self.key])
                        self.assertEqual(self.value, actual[self.k][self.key])

                    if self.k in "SUCCESS":
                        # 调用查询会员基本信息接口
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

                else:
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





