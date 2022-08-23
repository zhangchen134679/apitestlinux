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

excel = handler_middle.Handler().excel_upload_change_grade_LAN

cases = excel.read_data("L1017_TM")

brand = handler_middle.Handler.yml_conf["brand"]["lancome"]


@pytest.mark.bio
@ddt.ddt
class TestUploadOrderVerifyGrade(unittest.TestCase):
    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        cls.sleep = 1

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lancome"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 调用方法注册品牌下的会员
        for i in range(0, 61):
            member = handler_middle.register_member(cls.brand, headers=cls.headers)
            cls.member_list.append(member["data"]["union_code"])

        # 用例中降级用到的tradeNo
        cls.test_order_back = "test_arvAto_back_".lower()
        cls.order_150_back_1 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_2 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_3 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_4 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_5 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_6 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_7 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_8 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_9 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_10 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_11 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_12 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_13 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_14 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_15 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_16 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_17 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_18 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_19 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_20 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_21 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_22 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_23 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_24 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_25 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_26 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_27 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_28 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_29 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_30 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_31 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_32 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_33 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_34 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_35 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_36 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_37 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_38 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_39 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_40 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_41 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_42 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_43 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_44 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_45 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_46 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_47 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_48 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_49 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_50 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_51 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_52 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"
        cls.order_150_back_53 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"

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
        for index in range(0, 61):
            pattern = f"&member_{index + 1}&"
            if re.search(pattern, data_info):
                data_info = re.sub(pattern, self.member_list[index], str(data_info))
                break
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tradeNo
        data_info = re.sub(r"&tradeNo&", handler_middle.Handler().random_trade, str(data_info))
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中降级用到的tradeNo
        data_info = re.sub(r"&order_150_back_1&", self.order_150_back_1, str(data_info))
        data_info = re.sub(r"&order_150_back_2&", self.order_150_back_2, str(data_info))
        data_info = re.sub(r"&order_150_back_3&", self.order_150_back_3, str(data_info))
        data_info = re.sub(r"&order_150_back_4&", self.order_150_back_4, str(data_info))
        data_info = re.sub(r"&order_150_back_5&", self.order_150_back_5, str(data_info))
        data_info = re.sub(r"&order_150_back_6&", self.order_150_back_6, str(data_info))
        data_info = re.sub(r"&order_150_back_7&", self.order_150_back_7, str(data_info))
        data_info = re.sub(r"&order_150_back_8&", self.order_150_back_8, str(data_info))
        data_info = re.sub(r"&order_150_back_9&", self.order_150_back_9, str(data_info))
        data_info = re.sub(r"&order_150_back_10&", self.order_150_back_10, str(data_info))
        data_info = re.sub(r"&order_150_back_11&", self.order_150_back_11, str(data_info))
        data_info = re.sub(r"&order_150_back_12&", self.order_150_back_12, str(data_info))
        data_info = re.sub(r"&order_150_back_13&", self.order_150_back_13, str(data_info))
        data_info = re.sub(r"&order_150_back_14&", self.order_150_back_14, str(data_info))
        data_info = re.sub(r"&order_150_back_15&", self.order_150_back_15, str(data_info))
        data_info = re.sub(r"&order_150_back_16&", self.order_150_back_16, str(data_info))
        data_info = re.sub(r"&order_150_back_17&", self.order_150_back_17, str(data_info))
        data_info = re.sub(r"&order_150_back_18&", self.order_150_back_18, str(data_info))
        data_info = re.sub(r"&order_150_back_19&", self.order_150_back_19, str(data_info))
        data_info = re.sub(r"&order_150_back_20&", self.order_150_back_20, str(data_info))
        data_info = re.sub(r"&order_150_back_21&", self.order_150_back_21, str(data_info))
        data_info = re.sub(r"&order_150_back_22&", self.order_150_back_22, str(data_info))
        data_info = re.sub(r"&order_150_back_23&", self.order_150_back_23, str(data_info))
        data_info = re.sub(r"&order_150_back_24&", self.order_150_back_24, str(data_info))
        data_info = re.sub(r"&order_150_back_25&", self.order_150_back_25, str(data_info))
        data_info = re.sub(r"&order_150_back_26&", self.order_150_back_26, str(data_info))
        data_info = re.sub(r"&order_150_back_27&", self.order_150_back_27, str(data_info))
        data_info = re.sub(r"&order_150_back_28&", self.order_150_back_28, str(data_info))
        data_info = re.sub(r"&order_150_back_29&", self.order_150_back_29, str(data_info))
        data_info = re.sub(r"&order_150_back_30&", self.order_150_back_30, str(data_info))
        data_info = re.sub(r"&order_150_back_31&", self.order_150_back_31, str(data_info))
        data_info = re.sub(r"&order_150_back_32&", self.order_150_back_32, str(data_info))
        data_info = re.sub(r"&order_150_back_33&", self.order_150_back_33, str(data_info))
        data_info = re.sub(r"&order_150_back_34&", self.order_150_back_34, str(data_info))
        data_info = re.sub(r"&order_150_back_35&", self.order_150_back_35, str(data_info))
        data_info = re.sub(r"&order_150_back_36&", self.order_150_back_36, str(data_info))
        data_info = re.sub(r"&order_150_back_37&", self.order_150_back_37, str(data_info))
        data_info = re.sub(r"&order_150_back_38&", self.order_150_back_38, str(data_info))
        data_info = re.sub(r"&order_150_back_39&", self.order_150_back_39, str(data_info))
        data_info = re.sub(r"&order_150_back_40&", self.order_150_back_40, str(data_info))
        data_info = re.sub(r"&order_150_back_41&", self.order_150_back_41, str(data_info))
        data_info = re.sub(r"&order_150_back_42&", self.order_150_back_42, str(data_info))
        data_info = re.sub(r"&order_150_back_43&", self.order_150_back_43, str(data_info))
        data_info = re.sub(r"&order_150_back_44&", self.order_150_back_44, str(data_info))
        data_info = re.sub(r"&order_150_back_45&", self.order_150_back_45, str(data_info))
        data_info = re.sub(r"&order_150_back_46&", self.order_150_back_46, str(data_info))
        data_info = re.sub(r"&order_150_back_47&", self.order_150_back_47, str(data_info))
        data_info = re.sub(r"&order_150_back_48&", self.order_150_back_48, str(data_info))
        data_info = re.sub(r"&order_150_back_49&", self.order_150_back_49, str(data_info))
        data_info = re.sub(r"&order_150_back_50&", self.order_150_back_50, str(data_info))
        data_info = re.sub(r"&order_150_back_51&", self.order_150_back_51, str(data_info))
        data_info = re.sub(r"&order_150_back_52&", self.order_150_back_52, str(data_info))
        data_info = re.sub(r"&order_150_back_53&", self.order_150_back_53, str(data_info))


        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的data数据..
        replace = handler_middle.ReplaceDate(self.brand, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])

        expect_response_point = data_info["expect_response_point"]
        logger.info('预期结果{}'.format(expect_response_point))
        #  --------------------------------------------------------------------------------------------------------------------
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler_middle.Handler.yml_conf["host"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)
        time.sleep(3)

        if data['orderType'] == 1:

            response = handler_middle.upload_order_info_new(brand_code=data['brand_code'],
                                                            tradeno=data['tradeNo'],
                                                            status="TRADE_FINISHED",
                                                            headers=handler_middle.Handler().replace_uuid(self.headers))
            if response['code'] == 0:
                logger.info('订单变更状态成功')
                time.sleep(4)
            else:
                logger.error('订单状态变更失败 {}'.format(response))
        else:
            logger.info('非正单不做订单状态变更处理')



        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            #  调用查询当前积分
            actual_point = handler_middle.query_member_points(brand_code=data['brand_code'],
                                                              member_code=data['channelMemberId'],
                                                              headers=self.headers)
            logger.info("查询积分接口返回: {}".format(actual_point))
            if expect_response_point == '无积分':
                pass
            else:
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
    unittest.main()
