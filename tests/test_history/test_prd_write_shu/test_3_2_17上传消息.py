from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import time
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_shu

cases = excel.read_data("upload_message_info")


@ddt.ddt
class TestUploadMessageInfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        cls.sleep = 0

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["shu"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"][cls.brand]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"][cls.brand]["password"]

        # 从配置文件读取天猫店铺名称
        cls.tb_store_name = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["name"]

        # 从配置文件读取deal_store
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

        # 生成当前时间并转化格式
        cls.time = time.strftime("%Y-%m-%d %H:%M:%S")

    def setUp(self) -> None:

        # 调用会员注册接口
        self.register_media = handler_middle.register_member(self.brand, self.store_code, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register_media["data"]["union_code"]

        # 调用全渠道会员绑定解绑(新)接口
        self.bind = handler_middle.MemberBinding(self.brand, value=self.union_code, headers=self.headers)

        # 绑定天猫..京东..微信..
        self.bind.all_bind()

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    def tearDown(self) -> None:

        # 调用全渠道会员绑定解绑(新)接口
        bind = handler_middle.MemberBinding(self.brand, binding_type="0", value=self.union_code, headers=self.headers)
        bind.try_bind()

    @ddt.data(*cases)
    def test_upload_message_info(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的action_time
        data_info = re.sub(r"#action_time#", self.time, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
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

        expect_response = eval(data_info["expect_response"])

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():

                if self.k in "details":
                    # 调用积分明细查询接口
                    time.sleep(self.sleep)
                    actual_detail = handler_middle.query_points_detail(self.brand, self.union_code, headers=self.headers)

                    try:
                        logger.info("第{}条用例againAssert...".format(data_info["case_id"]))
                        for self.key, self.value in self.v[0].items():
                            # IndexError, actual_detail == null
                            try:
                                self.assertEqual(self.value, actual_detail["data"][self.k][0][self.key])

                            except IndexError as er:
                                logger.error("没有查询到积分,index..{}".format(actual_detail))
                                print("没有查询到积分,index..{}".format(actual_detail))
                                raise er

                    except AssertionError as err:
                        logger.error("againAssert...预期结果: {}:{}, 实际结果: {}:{}"
                                     .format(self.key, self.value, self.key, actual_detail["data"][self.k][0][self.key]))
                        print("againAssert...预期结果: {}:{}, 实际结果: {}:{}"
                              .format(self.key, self.value, self.key, actual_detail["data"][self.k][0][self.key]))
                        raise err

                else:
                    if self.k in "data":

                        try:
                            for self.key, self.value in self.v.items():
                                self.assertEqual(self.value, actual[self.k][self.key])

                        except AssertionError as err:
                            logger.error("预期结果: {}, 实际结果: {}".format(self.value, actual[self.k][self.key]))
                            print("预期结果: {}, 实际结果: {}".format(self.v, actual[self.k][self.key]))
                            raise err

                    else:
                        try:
                            self.assertEqual(self.v, actual[self.k])

                        except AssertionError as err:
                            logger.error("预期结果: {}, 实际结果: {}".format(data_info["case_id"], self.v, actual[self.k]))
                            print("预期结果: {}, 实际结果: {}".format(data_info["case_id"], self.v, actual[self.k]))
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



