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

cases = excel.read_data("member_points_change")


@pytest.mark.lrp
@ddt.ddt
class TestPointsChange(unittest.TestCase):

    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lancome"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用全渠道会员绑定解绑(新)接口
        for index in range(0, len(cls.member_list)):
            cls.bind = handler_middle.MemberBinding(
                cls.brand, binding_type="0", value=cls.member_list[index], headers=cls.headers)
            cls.bind.try_bind()

    def setUp(self) -> None:

        # 调用会员注册接口
        self.register_media = handler_middle.register_member(self.brand, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register_media["data"]["union_code"]

        # union_code insert list
        self.member_list.append(self.union_code)

    @allure.step("会员积分变更")
    @pytest.mark.write
    @pytest.mark.member_points_change
    @ddt.data(*cases)
    def test_member_points_change(self, data_info):
        allure.dynamic.title(str(data_info['title']))
        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的流水号
        data_info = re.sub(r"&vender_seq_code&", handler_middle.Handler().random_num, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
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
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的data..
        replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])
# --------------------------------------------------------------------------------------------------------------------
        """
        if..point_change == true
        加积分..
        """
        if data_info["point_change"]:
            handler_middle.change_points(self.brand, value=self.union_code, points="1000", headers=self.headers,
                                         vender_seq_code=handler_middle.Handler().random_num)
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

                if self.k in "points" and actual["code"] == 0:
                    actual_points = handler_middle.query_points(self.brand, value=self.union_code, headers=self.headers)

                    try:
                        for self.key, self.value in self.v[0].items():
                            # print(self.value, actual_points["data"][self.k][0][self.key])
                            self.assertEqual(self.value, actual_points["data"][self.k][0][self.key])

                    except Exception as err:
                        logger.error("actual_points: {}".format(actual_points))
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



