from middleware.middle_pre_back.middle_query import handler_middle
from common.handler_requests import visit
from jsonpath import jsonpath
import unittest
import random
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_kie

cases = excel.read_data("query_bind_info")


@ddt.ddt
class TestQueryBindInfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["kie"]

        # 从配置文件读取test_member_data
        cls.conf = handler_middle.Handler.yml_conf["test_member_data"]["kie"]

        # 从配置文件读取别人已绑定的open_id
        cls.other_bind_open_id = handler_middle.Handler.yml_conf["other_bind"]["kie"]["other_bind_open_id"]

        # 从配置文件读取别人已绑定的天猫nick
        cls.other_bind_tb_nick = handler_middle.Handler.yml_conf["other_bind"]["kie"]["other_bind_tb_nick"]

        # 从配置文件读取别人已绑定的jd_pin
        cls.other_bind_jd_pin = handler_middle.Handler.yml_conf["other_bind"]["kie"]["other_bind_jd_pin"]

        # 从配置文件读取天猫店铺名称
        cls.seller_name = handler_middle.Handler.yml_conf["crm_store"]["kie"]["name"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"]["kie"]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"]["kie"]["password"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

        # 调用会员注册接口
        cls.register_member = handler_middle.register_member(cls.brand, headers=cls.headers)

        # 调用查询会员基本信息接口
        cls.query_member_info = handler_middle.query_member_info(cls.brand, headers=cls.headers,
                                                                 value=cls.register_member["data"]["union_code"])

    @classmethod
    def tearDownClass(cls) -> None:
        # 调用会员退会接口
        handler_middle.quit_member(cls.brand, value=cls.register_member["data"]["union_code"], headers=cls.headers)

    @ddt.data(*cases)
    def test_query_bind_info(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的seller_name
        data_info = re.sub(r"#tb_seller_name#", self.seller_name, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未注册的mobile
        data_info = re.sub(r"#not_register_mobile#",
                           handler_middle.Handler().random_phone(self.brand, self.headers), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中已注册未绑定的mobile
        data_info = re.sub(r"#not_bind_mobile#", jsonpath(self.query_member_info, "$..mobile")[0], str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中已绑定的mobile
        data_info = re.sub(r"#bind_mobile#", self.conf["mobile"], str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未绑定的open_id
        data_info = re.sub(r"#not_bind_open_id#", "open_id" + str(random.randint(1000000, 9000000)), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中已绑定的open_id
        data_info = re.sub(r"#bind_open_id#", self.conf["openId"], str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中别人已绑定的open_id
        data_info = re.sub(r"#other_bind_open_id#", self.other_bind_open_id, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未注册的mix_mobile
        data_info = re.sub(r"#not_register_mix_mobile#", "mix" + str(random.randint(1000000, 9000000)), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未绑定的mix_mobile
        data_info = re.sub(r"#not_bind_mix_mobile#",
                           jsonpath(self.query_member_info,
                                    "$..data.media_account[?(@.type=='2')].accountNo")[0], str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中已绑定的mix_mobile
        data_info = re.sub(r"#bind_mix_mobile#", self.conf["encryptMobile"], str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未绑定的天猫昵称
        data_info = re.sub(r"#not_bind_taobao_nick#", "tb_nick" + str(random.randint(100000, 900000)), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中已绑定的天猫昵称
        data_info = re.sub(r"#bind_taobao_nick#", self.conf["taobaoid"], str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中别人已绑定的天猫nick
        data_info = re.sub(r"#other_bind_taobao_nick#", self.other_bind_tb_nick, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中未绑定的京东pin
        data_info = re.sub(r"#not_bind_jd_pin#", "JD_pin" + str(random.randint(1000000000, 9000000000)), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中已绑定的京东pin
        data_info = re.sub(r"#bind_JD_pin#", self.conf["JDpin"], str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中别人已绑定的京东pin
        data_info = re.sub(r"#other_bind_jd_pin#", self.other_bind_jd_pin, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
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

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in eval(data_info["expect_response"]).items():
                # print(self.v, actual[self.k])
                self.assertTrue(actual[self.k] == self.v)

            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))

        except Exception as err:
            self.result = "fail"

            logger.warning("data: {}".format(data))
            logger.warning("response: {}".format(actual))
            logger.error("第{}条用例失败, 预期结果: {}, 实际结果: {}".format(data_info["case_id"], self.v, actual[self.k]))

            print("data: {}".format(data))
            print("response: {}".format(actual))
            print("第{}条用例失败, 预期结果: {}, 实际结果: {}".format(data_info["case_id"], self.v, actual[self.k]))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()
