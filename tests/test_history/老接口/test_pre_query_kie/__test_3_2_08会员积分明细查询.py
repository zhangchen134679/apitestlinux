from middleware.middle_pre_back.middle_query import handler_middle
from common.handler_requests import visit
import unittest
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_kie

cases = excel.read_data("query_member_points_detail")


@ddt.ddt
class TestQueryMemberPointsDetail(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["kie"]

        # 从配置文件读取订单流水号...交易时间
        cls.trade_no = handler_middle.Handler.yml_conf["trade_no"]["online"]["trade_no"]
        cls.trade_time = handler_middle.Handler.yml_conf["trade_no"]["online"]["trade_time"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"]["kie"]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"]["kie"]["password"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

        # 调用会员注册接口
        cls.register_member = handler_middle.register_member(cls.brand, headers=cls.headers)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用会员退会接口
        handler_middle.quit_member(cls.brand, value=cls.register_member["data"]["union_code"], headers=cls.headers)

    @ddt.data(*cases)
    def test_query_member_points_detail(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中没有积分的union_code
        data_info = re.sub(r"#not_points_union_code#", self.register_member["data"]["union_code"], str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的value值
        data_info = handler_middle.Handler().replace_data(self.brand, str(data_info))
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
                if self.k in "data":

                    # self.key == total..union_code..details
                    for self.key, self.value in self.v.items():

                        if self.key in "details" and data_info["case_id"] != 28:
                            # i, j == {'isPoint': 1.0, 'sourceCodeRemark': '天猫: 消费积分'}...
                            # i, j == {'isPoint': 1.0, 'sourceCodeRemark': '积分商城兑换-虚拟物品: 手工调整增积分'}....
                            for i, j in enumerate(expect_response["data"][self.key]):

                                # self.keys == isPoint..tradeNo..remain_points..sourceCodeRemark
                                try:
                                    logger.info("第{}条用例againAssert...".format(data_info["case_id"]))
                                    for self.keys, self.values in j.items():
                                        # print(self.values, actual[self.k][self.key][i][self.keys])
                                        self.assertTrue(self.values == actual[self.k][self.key][i][self.keys])

                                except AssertionError as err:
                                    logger.error("againAssert...预期结果: {}, 实际结果: {}".
                                                 format(self.values, actual[self.k][self.key][i][self.keys]))
                                    print("againAssert...预期结果: {}, 实际结果: {}".
                                          format(self.values, actual[self.k][self.key][i][self.keys]))
                                    raise err

                        # 会员details数据为空
                        elif data_info["case_id"] == 28:
                            self.assertTrue(not actual[self.k]["details"])

                else:
                    self.assertTrue(self.v == actual[self.k])
                    # print(self.v, actual[self.k])

            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))

        except Exception as err:
            self.result = "fail"

            logger.warning("data: {}".format(data))
            logger.warning("response: {}".format(actual))
            logger.error("第{}条用例失败, 预期结果: {}, 实际结果: {}".format(data_info["case_id"], self.v, actual[self.k]))

            print("data: {}".format(data))
            print("response: {}".format(actual))
            print("第{}条用例失败, 预期结果: {}, 实际结果: {}".format(data_info["case_id"], self.v, actual[self.k]))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()



