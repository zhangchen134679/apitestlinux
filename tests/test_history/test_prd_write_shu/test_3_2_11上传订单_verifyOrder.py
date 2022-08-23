from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import time
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_shu

cases = excel.read_data("upload_order_verifyOrder")


@ddt.ddt
class TestUploadOrderVerifyOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        cls.sleep = 10

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["shu"]

        # 从配置文件读取店员BA
        cls.BA_code = handler_middle.Handler.yml_conf["crm_employee"][cls.brand]

        # 从配置文件读取deal_store
        cls.deal_store = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]

        # 从配置文件读取天猫店铺名称
        cls.tb_store_name = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["name"]

        # 从配置文件读取商品名称...商品编码
        cls.product_code = handler_middle.Handler.yml_conf["crm_product"][cls.brand]["code"]
        cls.product_name = handler_middle.Handler.yml_conf["crm_product"][cls.brand]["name"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"][cls.brand]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"][cls.brand]["password"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

    def setUp(self) -> None:

        # 调用会员注册接口
        self.register_media = handler_middle.register_member(self.brand, self.deal_store, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register_media["data"]["union_code"]

        # 调用全渠道会员绑定解绑(新)接口
        self.Bind = handler_middle.MemberBinding(
                            self.brand, binding_type="1", value=self.union_code, headers=self.headers)
        self.Bind.all_bind()

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    def tearDown(self) -> None:

        # 调用全渠道会员绑定解绑(新)接口
        bind = handler_middle.MemberBinding(self.brand, binding_type="0", value=self.union_code, headers=self.headers)
        bind.all_bind()
        bind.quit_member()

    @ddt.data(*cases)
    def test_upload_order_verifyOrder(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的store_code
        data_info = re.sub(r"#store_code#", self.deal_store, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tradeNo
        data_info = re.sub(r"#tradeNo#", handler_middle.Handler().random_trade, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的employeeCode
        data_info = re.sub(r"#employeeCode#", self.BA_code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的commodityCode, commodityName
        data_info = re.sub(r"#commodityCode#", self.product_code, str(data_info))
        data_info = re.sub(r"#commodityName#", self.product_name, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的value值
        replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
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

        expect_response = eval(data_info["expect_response"])

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():

                if self.k in "orders":

                    # 调用订单列表查询接口
                    time.sleep(self.sleep)
                    actual_order = handler_middle.query_order(self.brand, value=self.union_code, headers=self.headers)

                    try:
                        logger.info("第{}条用例againAssert...".format(data_info["case_id"]))
                        for self.key, self.value in self.v[0].items():
                            # IndexError, actual_order == null
                            try:
                                self.assertTrue(self.value == actual_order["data"][self.k][0][self.key])

                            except IndexError as err:
                                logger.error("没有查询到订单,index..{}".format(actual_order))
                                print("没有查询到订单,index..{}".format(actual_order))
                                raise err

                    except AssertionError as err:
                        logger.error("againAssert...预期结果: {}:{}, 实际结果: {}:{}"
                                     .format(self.key, self.value, self.key, actual_order["data"][self.k][0][self.key]))
                        print("againAssert...预期结果: {}:{}, 实际结果: {}:{}"
                              .format(self.key, self.value, self.key, actual_order["data"][self.k][0][self.key]))
                        raise err

                else:
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

