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

excel = handler_middle.Handler().excel_upload_change_grade_bio

cases = excel.read_data("b")



@pytest.mark.bio
@ddt.ddt
class TestUploadOrderVerifyGrade(unittest.TestCase):

    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        cls.sleep = 10

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["bio"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 调用方法注册品牌下的会员
        for i in range(0, 200):
            member = handler_middle.register_member(cls.brand, headers=cls.headers)
            cls.member_list.append(member["data"]["union_code"])

        # 用例中降级用到的tradeNo
        cls.test_order_back = "test_arvAto_back_".lower()
        cls.tradeNo_31_1000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_53_1999 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_55_9001 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_58_1 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_60_2000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_72_1900 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_74_5001 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_76_2999 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_79_29999 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_81_19001 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_83_3000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_91_01 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_93_2500 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_95_3900 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_97_25001 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_99_4999 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_102_49999 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_104_39001 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_106_5000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_110_01 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_112_5000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_114_50001 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_116_7500 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_118_8900 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_120_75001 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_122_99999 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_124_89001 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.tradeNo_126_10000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"


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

        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的channelMemberId
        """
        re.search匹配data_info中&member_&字符串,匹配不到继续遍历index+1,匹配到则进行替换break
        """
        for index in range(0, 200):
            pattern = f"&member_{index+1}&"
            if re.search(pattern, data_info):
                data_info = re.sub(pattern, self.member_list[index], str(data_info))
                break
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tradeNo
        data_info = re.sub(r"&tradeNo&", handler_middle.Handler().random_trade, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中降级用到的tradeNo
        data_info = re.sub(r"&tradeNo-31-1000&", self.tradeNo_31_1000, str(data_info))
        data_info = re.sub(r"&tradeNo-53-1999&", self.tradeNo_53_1999, str(data_info))
        data_info = re.sub(r"&tradeNo-55-900.1&", self.tradeNo_55_9001, str(data_info))
        data_info = re.sub(r"&tradeNo-58-1&", self.tradeNo_58_1, str(data_info))
        data_info = re.sub(r"&tradeNo-60-2000&", self.tradeNo_60_2000, str(data_info))
        data_info = re.sub(r"&tradeNo-72-1900&", self.tradeNo_72_1900, str(data_info))
        data_info = re.sub(r"&tradeNo-74-500.1&", self.tradeNo_74_5001, str(data_info))
        data_info = re.sub(r"&tradeNo-76-2999&", self.tradeNo_76_2999, str(data_info))
        data_info = re.sub(r"&tradeNo-79-2999.9&", self.tradeNo_79_29999, str(data_info))
        data_info = re.sub(r"&tradeNo-81-1900.1&", self.tradeNo_81_19001, str(data_info))
        data_info = re.sub(r"&tradeNo-83-3000&", self.tradeNo_83_3000, str(data_info))
        data_info = re.sub(r"&tradeNo-91-0.1&", self.tradeNo_91_01, str(data_info))
        data_info = re.sub(r"&tradeNo-93-2500&", self.tradeNo_93_2500, str(data_info))
        data_info = re.sub(r"&tradeNo-95-3900&", self.tradeNo_95_3900, str(data_info))
        data_info = re.sub(r"&tradeNo-97-2500.1&", self.tradeNo_97_25001, str(data_info))
        data_info = re.sub(r"&tradeNo-99-4999&", self.tradeNo_99_4999, str(data_info))
        data_info = re.sub(r"&tradeNo-102-4999.9&", self.tradeNo_102_49999, str(data_info))
        data_info = re.sub(r"&tradeNo-104-3900.1&", self.tradeNo_104_39001, str(data_info))
        data_info = re.sub(r"&tradeNo-106-5000&", self.tradeNo_106_5000, str(data_info))
        data_info = re.sub(r"&tradeNo-110-0.1&", self.tradeNo_110_01, str(data_info))
        data_info = re.sub(r"&tradeNo-112-5000&", self.tradeNo_112_5000, str(data_info))
        data_info = re.sub(r"&tradeNo-114-5000.1&", self.tradeNo_114_50001, str(data_info))
        data_info = re.sub(r"&tradeNo-116-7500&", self.tradeNo_116_7500, str(data_info))
        data_info = re.sub(r"&tradeNo-118-8900&", self.tradeNo_118_8900, str(data_info))
        data_info = re.sub(r"&tradeNo-120-7500.1&", self.tradeNo_120_75001, str(data_info))
        data_info = re.sub(r"&tradeNo-122-9999.9&", self.tradeNo_122_99999, str(data_info))
        data_info = re.sub(r"&tradeNo-124-8900.1&", self.tradeNo_124_89001, str(data_info))
        data_info = re.sub(r"&tradeNo-126-10000&", self.tradeNo_126_10000, str(data_info))

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
        expect_response_point = data_info["expect_response_point"]

        #  正单进行订单状态变更
        time.sleep(5)
        if data['orderType'] == 1:

            response = handler_middle.upload_order_info_new(brand_code=data['brand_code'],
                                                            tradeno=data['tradeNo'],
                                                            status="TRADE_FINISHED",
                                                            headers=handler_middle.Handler().replace_uuid(self.headers))
            if response['code'] == 0:
                logger.info('订单变更状态成功')
            else:
                logger.error('订单状态变更失败 {}'.format(response))
        else:
            logger.info('非正单不做订单状态变更处理')


        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():

                if self.k in "data":
                    time.sleep(15)

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

            #  调用查询当前积分
            actual_point = handler_middle.query_member_points(brand_code=data['brand_code'],
                                                              member_code=data['channelMemberId'],
                                                              headers=self.headers)
            logger.info("查询积分接口返回: {}".format(actual_point))

            self.assertEqual(expect_response_point, actual_point['data']['points'][0]['evalidPoints'])

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
    pytest.main()
