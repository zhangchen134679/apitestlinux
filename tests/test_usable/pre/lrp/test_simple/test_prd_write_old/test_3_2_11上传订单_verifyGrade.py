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

excel = handler_middle.Handler().excel_upload_order_info_simple

cases = excel.read_data("lrp_upload_order_verifyGrade")


@pytest.mark.lrp
@ddt.ddt
class TestUploadOrderVerifyGrade(unittest.TestCase):

    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        cls.sleep = 10

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrp"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 调用方法注册品牌下的会员
        for i in range(0, 3):
            member = handler_middle.register_member(cls.brand, headers=cls.headers)
            cls.member_list.append(member["data"]["union_code"])

        # 用例中降级用到的tradeNo
        cls.test_order_back = "test_arvAto_back_".lower()
        cls.order_5000_back_2000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_5000_back_3000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_5000_back_4000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_5000_back_5000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_3000_back_1000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_3000_back_2000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_3000_back_3000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_2000_back_1000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_2000_back_2000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_1000_back_1000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_1_back_1 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"

    def setUp(self) -> None:

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用会员退会接口
        for index in range(0, len(cls.member_list)):
            handler_middle.quit_member(
                cls.brand, value=cls.member_list[index], headers=cls.headers, query_type="union_code")

    @allure.step("上传订单")
    @pytest.mark.write
    @pytest.mark.upload_order
    @ddt.data(*cases)
    def test_upload_order_verifyGrade(self, data_info):
        allure.dynamic.title(str(data_info['title']))
        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的channelMemberId
        """
        re.search匹配data_info中&member_&字符串,匹配不到继续遍历index+1,匹配到则进行替换break
        """
        for index in range(0, 3):
            pattern = f"&member_{index+1}&"
            if re.search(pattern, data_info):
                data_info = re.sub(pattern, self.member_list[index], str(data_info))
                break
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tradeNo
        data_info = re.sub(r"&tradeNo&", handler_middle.Handler().random_trade, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中降级用到的tradeNo
        data_info = re.sub(r"&test_order_5000_back_2000&", self.order_5000_back_2000, str(data_info))
        data_info = re.sub(r"&test_order_5000_back_3000&", self.order_5000_back_3000, str(data_info))
        data_info = re.sub(r"&test_order_5000_back_4000&", self.order_5000_back_4000, str(data_info))
        data_info = re.sub(r"&test_order_5000_back_5000&", self.order_5000_back_5000, str(data_info))
        data_info = re.sub(r"&test_order_3000_back_1000&", self.order_3000_back_1000, str(data_info))
        data_info = re.sub(r"&test_order_3000_back_2000&", self.order_3000_back_2000, str(data_info))
        data_info = re.sub(r"&test_order_3000_back_3000&", self.order_3000_back_3000, str(data_info))
        data_info = re.sub(r"&test_order_2000_back_1000&", self.order_2000_back_1000, str(data_info))
        data_info = re.sub(r"&test_order_2000_back_2000&", self.order_2000_back_2000, str(data_info))
        data_info = re.sub(r"&test_order_1000_back_1000&", self.order_1000_back_1000, str(data_info))
        data_info = re.sub(r"&test_order_1_back_1&", self.order_1_back_1, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的data数据..
        replace = handler_middle.ReplaceDate(self.brand, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
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

                if self.k in "data":
                    time.sleep(self.sleep)

                    if data["orderType"] == 1:
                        # 调用查询当前会员等级接口
                        actual_grade = handler_middle.query_grade(self.brand, data["channelMemberId"], self.headers)

                        try:
                            for self.key, self.value in self.v.items():
                                self.assertEqual(self.value, actual_grade[self.k][self.key])

                        except AssertionError as err:
                            logger.error("actual_grade: {}".format(actual_grade))
                            raise err

                    elif data["orderType"] == 2:
                        # 调用查询当前会员等级接口
                        actual_grade = handler_middle.query_grade(self.brand, data["channelMemberId"], self.headers)

                        try:
                            for self.key, self.value in self.v.items():
                                self.assertEqual(self.value, actual_grade[self.k][self.key])

                        except AssertionError as err:
                            logger.error("actual_grade: {}".format(actual_grade))
                            raise err

                else:
                    # print(self.v, actual[self.k])
                    self.assertEqual(self.v, actual[self.k])

            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))

        except Exception as err:
            self.result = "fail"
            logger.error("data: {}".format(data))
            logger.error("response: {}".format(actual))
            logger.error("第{}条用例失败..Fail...Expected, Actual{}".format(data_info["case_id"], err))

            print("data: {}".format(data))
            print("response: {}".format(actual))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()
