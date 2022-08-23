from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import pytest
import allure
import json
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_write_common

cases = excel.read_data("submit_gift_info")


@pytest.mark.lrl
@ddt.ddt
class TestSubmitGiftInfo(unittest.TestCase):

    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrl"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

    def setUp(self) -> None:

        # 调用会员注册接口
        self.register_media = handler_middle.register_member(self.brand, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register_media["data"]["union_code"]

        # 生成订单流水编号
        self.venDer_seq_code = handler_middle.Handler().random_trade

        # union_code insert list
        self.member_list.append(self.union_code)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用全渠道会员绑定解绑(新)接口
        for index in range(0, len(cls.member_list)):
            cls.bind = handler_middle.MemberBinding(
                cls.brand, binding_type="0", value=cls.member_list[index], headers=cls.headers)
            cls.bind.try_bind()

    @allure.step("上传兑换信息")
    @pytest.mark.write
    @pytest.mark.submit_gift_info
    @ddt.data(*cases)
    def test_submit_gift_info(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的供应商编号
        data_info = re.sub(r"&vender_code&", "1", str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tradeNo
        data_info = re.sub(r"&tradeNo&", handler_middle.Handler().random_trade, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的流水编号  -- 兑换单流水号..须和积分变更(减积分)保持一致
        data_info = re.sub(r"&vender_seq_code&", self.venDer_seq_code, str(data_info))
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
        # 替换用例中的data..
        replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])
#  --------------------------------------------------------------------------------------------------------------------
        """
        if..point_change == true
        加积分..
        """
        if data_info["point_change"]:
            # 调用积分变更接口加积分..
            handler_middle.change_points(self.brand, value=self.union_code, points="1000", headers=self.headers,
                                         vender_seq_code=handler_middle.Handler().random_num)
            # 调用积分变更接口减积分..
            handler_middle.change_points(self.brand, value=self.union_code, points="1000", headers=self.headers,
                                         change_type="RED", point_type="RDP", vender_seq_code=self.venDer_seq_code)
#  --------------------------------------------------------------------------------------------------------------------
        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)
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

                if self.k in "data" and actual["code"] == 0:
                    actual_order = handler_middle.query_order(
                                self.brand, value=self.union_code, headers=self.headers, order_type=2)
                    try:
                        for self.key, self.value in self.v.items():
                            if self.key in "orders":
                                for self.keys, self.values in self.value[0].items():
                                    # print(self.values, actual_order[self.k][self.key][0][self.keys])
                                    self.assertEqual(self.values, actual_order[self.k][self.key][0][self.keys])

                            else:
                                # print(self.value, actual_order[self.k][self.key])
                                self.assertEqual(self.value, actual_order[self.k][self.key])

                    except Exception as err:
                        logger.error("actual_order: {}".format(actual_order))
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
            logger.error("第{}条用例失败..Fail...Expected, Actual{}".format(data_info["case_id"], err))

            print("data: {}".format(data))
            print("response: {}".format(actual))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()
