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

excel = handler_middle.Handler().excel_lrp

cases = excel.read_data("upload_message_info")


@pytest.mark.lrp
@ddt.ddt
class TestUploadMessageInfo(unittest.TestCase):

    member_list = []

    sleep = 2

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrp"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 从配置文件读取store_code
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]

        # 生成当前时间并转化格式
        cls.time = time.strftime("%Y-%m-%d %H:%M:%S")

    def setUp(self) -> None:

        # 调用会员注册接口
        self.register_media = handler_middle.register_member(self.brand, self.store_code, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register_media["data"]["union_code"]

        # union_code insert list
        self.member_list.append(self.union_code)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用全渠道会员绑定解绑(新)接口
        for index in range(0, len(cls.member_list)):
            cls.bind = handler_middle.MemberBinding(
                cls.brand, binding_type="0", value=cls.member_list[index], headers=cls.headers)
            cls.bind.try_bind()

    @allure.step("上传消息")
    @pytest.mark.write
    @pytest.mark.upload_message_info
    @ddt.data(*cases)
    def test_upload_message_info(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的action_time
        data_info = re.sub(r"#action_time#", self.time, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        """
        if..bind == true
        绑定天猫..京东..微信..
        """
        if eval(data_info)["bind"]:
            self.bind = handler_middle.MemberBinding(self.brand, value=self.union_code, headers=self.headers)
            if eval(data_info)["bind"] == 976:
                self.bind.tb_bind("976")
            elif eval(data_info)["bind"] == "9AL":
                self.bind.jd_bind("9AL")
            elif eval(data_info)["bind"] == "6P0":
                self.bind.wx_bind("6P0")
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的data数据..
        replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])
# --------------------------------------------------------------------------------------------------------------------
        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)
# --------------------------------------------------------------------------------------------------------------------
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

                if self.k in "details":
                    time.sleep(self.sleep)
                    actual_points_detail = handler_middle.query_points_detail(
                                        self.brand, self.union_code, headers=self.headers)

                    for self.key, self.value in self.v[0].items():
                        try:
                            # print(self.value, actual_points_detail["data"][self.k][0][self.key])
                            self.assertEqual(self.value, actual_points_detail["data"][self.k][0][self.key])

                        # IndexError, actual_detail == null
                        except IndexError as err:
                            logger.error("actual_points_detail: {}".format(actual_points_detail))
                            raise err

                else:
                    if self.k in "data":
                        for self.key, self.value in self.v.items():
                            # print(self.value, actual[self.k][self.key])
                            self.assertEqual(self.value, actual[self.k][self.key])

                    else:
                        # print(self.v, actual[self.k])
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



