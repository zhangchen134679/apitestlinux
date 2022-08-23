from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import time
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_lrp

cases = excel.read_data("upload_order_verifyGrade")


@ddt.ddt
class TestUploadOrderVerifyGrade(unittest.TestCase):

    member_code = []

    @classmethod
    def setUpClass(cls) -> None:

        cls.sleep = 10

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrp"]

        # 从配置文件读取商品编码...
        cls.product_code = handler_middle.Handler.yml_conf["crm_product"]["lrp_code"]

        # 从配置文件读取商品名称...
        cls.product_name = handler_middle.Handler.yml_conf["crm_product"]["lrp_name"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"]["lrp"]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"]["lrp"]["password"]

        # 从配置文件读取deal_store
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"]["lrp"]["deal_store_no"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

        # 生成当前时间并转化格式
        cls.time = time.strftime("%Y-%m-%d %H:%M:%S")

        # 调用方法注册品牌下的会员
        for i in range(0, 31):
            member = handler_middle.register_member(cls.brand, store_code=cls.store_code, headers=cls.headers)
            cls.member_code.append(member["data"]["union_code"])

        # 用例中降级用到的tradeNo
        cls.order_5000_back_2000 = "order_back_{}".format(handler_middle.Handler().random_num)
        cls.order_5000_back_3000 = "order_back_{}".format(handler_middle.Handler().random_num)
        cls.order_5000_back_4000 = "order_back_{}".format(handler_middle.Handler().random_num)
        cls.order_5000_back_5000 = "order_back_{}".format(handler_middle.Handler().random_num)
        cls.order_3000_back_1000 = "order_back_{}".format(handler_middle.Handler().random_num)
        cls.order_3000_back_2000 = "order_back_{}".format(handler_middle.Handler().random_num)
        cls.order_3000_back_3000 = "order_back_{}".format(handler_middle.Handler().random_num)
        cls.order_2000_back_1000 = "order_back_{}".format(handler_middle.Handler().random_num)
        cls.order_2000_back_2000 = "order_back_{}".format(handler_middle.Handler().random_num)
        cls.order_1000_back_1000 = "order_back_{}".format(handler_middle.Handler().random_num)
        cls.order_1_back_1 = "order_back_{}".format(handler_middle.Handler().random_num)

    def setUp(self) -> None:
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    @classmethod
    def tearDownClass(cls) -> None:
        while cls.member_code:
            # 调用会员退会接口
            handler_middle.quit_member(cls.brand, value=cls.member_code[0], headers=cls.headers, query_type="union_code")
            cls.member_code.pop(0)

    @ddt.data(*cases)
    def test_upload_order_verifyGrade(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的consentTime
        data_info = re.sub(r"#time#", self.time, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的store_code
        data_info = re.sub(r"#store_code#", self.store_code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的channelMemberId
        for i in range(0, 31):
            m = i+1
            pattern = "#member_{}#".format(m)
            data_info = re.sub(pattern, self.member_code[i], str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的commodityCode, commodityName
        data_info = re.sub(r"#commodityCode#", self.product_code, str(data_info))
        data_info = re.sub(r"#commodityName#", self.product_name, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tradeNo
        data_info = re.sub(r"#tradeNo#", handler_middle.Handler().random_trade, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中降级用到的tradeNo
        data_info = re.sub(r"#order_5000_back_2000#", self.order_5000_back_2000, str(data_info))
        data_info = re.sub(r"#order_5000_back_3000#", self.order_5000_back_3000, str(data_info))
        data_info = re.sub(r"#order_5000_back_4000#", self.order_5000_back_4000, str(data_info))
        data_info = re.sub(r"#order_5000_back_5000#", self.order_5000_back_5000, str(data_info))
        data_info = re.sub(r"#order_3000_back_1000#", self.order_3000_back_1000, str(data_info))
        data_info = re.sub(r"#order_3000_back_2000#", self.order_3000_back_2000, str(data_info))
        data_info = re.sub(r"#order_3000_back_3000#", self.order_3000_back_3000, str(data_info))
        data_info = re.sub(r"#order_2000_back_1000#", self.order_2000_back_1000, str(data_info))
        data_info = re.sub(r"#order_2000_back_2000#", self.order_2000_back_2000, str(data_info))
        data_info = re.sub(r"#order_1000_back_1000#", self.order_1000_back_1000, str(data_info))
        data_info = re.sub(r"#order_1_back_1#", self.order_1_back_1, str(data_info))
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

                if self.k in "data":

                    logger.info("第{}条用例againAssert...".format(data_info["case_id"]))

                    if data["orderType"] == 1:

                        # 调用查询当前会员等级接口
                        time.sleep(self.sleep)
                        actual_grade = handler_middle.query_grade(self.brand, data["channelMemberId"], self.headers)

                        try:
                            for self.key, self.value in self.v.items():
                                self.assertTrue(self.value == actual_grade[self.k][self.key])

                        except AssertionError as err:
                            logger.error("againAssert...预期结果: {}:{}, 实际结果: {}:{}"
                                         .format(self.key, self.value, self.key, actual_grade[self.k][self.key]))
                            print("againAssert...预期结果: {}:{}, 实际结果: {}:{}"
                                  .format(self.key, self.value, self.key, actual_grade[self.k][self.key]))
                            raise err

                    elif data["orderType"] == 2:

                        # 调用查询当前会员等级接口
                        time.sleep(self.sleep)
                        actual_grade = handler_middle.query_grade(self.brand, data["channelMemberId"], self.headers)

                        try:
                            for self.key, self.value in self.v.items():
                                self.assertTrue(self.value == actual_grade[self.k][self.key])

                        except AssertionError as err:
                            logger.error("againAssert...预期结果: {}:{}, 实际结果: {}:{}"
                                         .format(self.key, self.value, self.key, actual_grade[self.k][self.key]))
                            print("againAssert...预期结果: {}:{}, 实际结果: {}:{}"
                                  .format(self.key, self.value, self.key, actual_grade[self.k][self.key]))
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
