from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_shu

cases = excel.read_data("member_points_change")


@ddt.ddt
class TestPointsChange(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["shu"]

        # 从配置文件读取天猫店铺名称
        cls.tb_store_name = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["name"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"][cls.brand]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"][cls.brand]["password"]

        # 从配置文件读取store_code
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

        # 调用会员注册接口
        cls.register_media = handler_middle.register_member(cls.brand, store_code=cls.store_code, headers=cls.headers)

        # 提取会员union_code
        cls.union_code = cls.register_media["data"]["union_code"]

        # 调用全渠道会员绑定解绑(新)接口
        cls.bind = handler_middle.MemberBinding(cls.brand, value=cls.union_code, headers=cls.headers)

        # 绑定天猫..京东..微信..
        cls.bind.all_bind()

    @classmethod
    def tearDownClass(cls) -> None:
        # 调用全渠道会员绑定解绑(新)接口
        bind = handler_middle.MemberBinding(cls.brand, binding_type="0", value=cls.union_code, headers=cls.headers)
        bind.try_bind()

    def setUp(self) -> None:

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    @ddt.data(*cases)
    def test_member_points_change(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的流水号
        data_info = re.sub(r"#vender_seq_code#", handler_middle.Handler().random_num, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的value值
        replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
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

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in eval(data_info["expect_response"]).items():
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



