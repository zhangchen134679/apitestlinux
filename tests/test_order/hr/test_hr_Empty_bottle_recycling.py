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

excel = handler_middle.Handler().excel_upload_change_grade_HR

cases = excel.read_data("hr_Empty_bottle_recycling")


class Data:  # 收集接口返回数据
    order_history_order_no = None
    order_history_detail_no = None
    order_history_sku_code = None


collect_data = Data()


@pytest.mark.hr
@ddt.ddt
class TestUploadOrderVerifyGrade(unittest.TestCase):
    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        cls.sleep = 10

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["hr"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 调用方法注册品牌下的会员
        for i in range(0, 1):
            member = handler_middle.register_member(cls.brand, headers=cls.headers)
            cls.member_list.append(member["data"]["union_code"])

        # 用例中降级用到的tradeNo
        cls.test_order_back = "test_arvAto_back_".lower()
        cls.test_order_68000_back_38000 = f"{cls.test_order_back}{handler_middle.Handler().random_num}"

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
        for index in range(0, 1):
            pattern = f"&member_{index + 1}&"
            if re.search(pattern, data_info):
                data_info = re.sub(pattern, self.member_list[index], str(data_info))
                break
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tradeNo
        data_info = re.sub(r"&tradeNo&", handler_middle.Handler().random_trade, str(data_info))
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中降级用到的tradeNo
        data_info = re.sub(r"&test_order_68000_back_38000&", self.test_order_68000_back_38000, str(data_info))
        print(data_info)

        if eval(data_info)["case_id"] == 3:  # 替换3.2.69接口数据

            data_info = re.sub(r"&order_history_order_no&", str(getattr(collect_data, 'order_history_order_no')),
                               str(data_info))
            data_info = re.sub(r"&order_history_order_no&", str(getattr(collect_data, 'order_history_order_no')),
                               str(data_info))
            data_info = re.sub(r"&order_history_detail_no&", str(getattr(collect_data, 'order_history_detail_no')),
                               str(data_info))
            data_info = re.sub(r"&order_history_sku_code&", str(getattr(collect_data, 'order_history_sku_code')),
                               str(data_info))
        elif eval(data_info)["case_id"] == 4:  # 替换3.2.70接口数据
            data_info = re.sub(r"&order_history_order_no&", str(getattr(collect_data, 'order_history_order_no')),
                               str(data_info))
        # --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的data数据..
        replace = handler_middle.ReplaceDate(self.brand, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])

        print("data:", data)
        #  --------------------------------------------------------------------------------------------------------------------
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler_middle.Handler.yml_conf["host"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)
        logger.info('接口返回:{}'.format(actual))
        if data_info["case_id"] == 2:
            #  报存接口返回数据
            setattr(collect_data, 'order_history_order_no', actual["data"]["orderInfos"][0]["orderNo"])
            setattr(collect_data, 'order_history_detail_no', actual["data"]["orderInfos"][0]["details"][0]["detailNo"])
            setattr(collect_data, 'order_history_sku_code', actual["data"]["orderInfos"][0]["details"][0]["skuCode"])

        expect_response = json.loads(data_info["expect_response"])
        expect_response_point = data_info["expect_response_point"]

        time.sleep(10)

        if data_info["case_id"] == 1:

            response = handler_middle.upload_order_info_new(brand_code=data['brand_code'],
                                                            tradeno=data['tradeNo'],
                                                            status="TRADE_FINISHED",
                                                            headers=handler_middle.Handler().replace_uuid(self.headers))
            if response['code'] == 0:
                logger.info('订单变更状态成功')
                time.sleep(15)
            else:
                logger.error('订单状态变更失败 {}'.format(response))
        else:
            logger.info('非正单不做订单状态变更处理')
        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():
                # print(self.v, actual[self.k])
                self.assertEqual(self.v, actual[self.k])

            # #  调用查询当前积分
            actual_point = handler_middle.query_member_points(brand_code=self.brand,
                                                              member_code=data['value'],
                                                              headers=self.headers,
                                                              pointTypeGroup='VBP')

            logger.info("查询积分接口返回: {}".format(actual_point))
            if str(data_info['case_id']) in ('1', '2'):
                # 会员BP类型 接口返回points: [] 时使用
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
