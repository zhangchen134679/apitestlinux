from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import time
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_lrp

cases = excel.read_data("submit_gift_info")


@ddt.ddt
class TestSubmitGiftInfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        cls.sleep = 1

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrp"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"]["lrp"]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"]["lrp"]["password"]

        # 从配置文件读取天猫店铺名称
        cls.tb_store_name = handler_middle.Handler.yml_conf["crm_store"]["lrp"]["name"]

        # 从配置文件读取deal_store
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"]["lrp"]["deal_store_no"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

        # 供应商编号
        cls.code = "1"

    def setUp(self) -> None:

        # 调用会员注册接口
        self.register_media = handler_middle.register_member(self.brand, self.store_code, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register_media["data"]["union_code"]

        # 调用全渠道会员绑定解绑(新)接口
        self.Bind = handler_middle.MemberBinding(self.brand, binding_type="1", value=self.union_code, headers=self.headers)
        self.Bind.all_bind()

        # 调用积分变更接口
        handler_middle.change_points(self.brand, value=self.union_code, points=1000,
                                     change_type="ACC", point_type="ABP", change_channel="07",
                                     vender_seq_code=handler_middle.Handler().random_trade, headers=self.headers)
        time.sleep(self.sleep)

        # 调用积分变更接口  -- 供应商兑换单流水号(用于兑礼场景时填写订单号), 调用方确保该值唯一(同3.2.9会员积分变更接口内的流水号对应...
        self.number = handler_middle.Handler().random_num

        self.change_points = handler_middle.change_points(self.brand, value=self.union_code, vender_code=self.code,
                                                          change_type="RED", point_type="MBP", change_channel="08",
                                                          vender_seq_code=self.number, headers=self.headers, points=100)

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    def tearDown(self) -> None:
        # 调用全渠道会员绑定解绑(新)接口
        bind = handler_middle.MemberBinding(self.brand, binding_type="0", value=self.union_code, headers=self.headers)
        bind.try_bind()

    @ddt.data(*cases)
    def test_submit_gift_info(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的store_code
        data_info = re.sub(r"#store_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的供应商编号
        data_info = re.sub(r"#vender_code#", self.code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tradeNo
        data_info = re.sub(r"#tradeNo#", handler_middle.Handler().random_trade, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的流水编号  -- 供应商兑换单流水号(用于兑礼场景时填写订单号), 调用方确保该值唯一(同3.2.9会员积分变更接口内的流水号对应...
        data_info = re.sub(r"#vender_seq_code#", self.number, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的value值..data
        replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
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

                    # 调用订单明细查询接口
                    actual_order = handler_middle.query_order_detail(
                        self.brand, value=self.union_code, trade_no=data["tradeNo"], headers=self.headers)

                    try:
                        logger.info("第{}条用例againAssert...".format(data_info["case_id"]))
                        for self.key, self.value in self.v.items():
                            for self.keys, self.values in self.value[0].items():
                                self.assertEqual(self.values, actual_order[self.k][self.key][0][self.keys])

                    except AssertionError as err:
                        logger.error("againAssertFail...Expected, Actual{}".format(err))
                        raise err

                else:
                    try:
                        # AssertionError: 0 != 1 可能是因为前置条件加积分还没入库,导致减积分可用积分不足..兑礼fail..
                        self.assertEqual(self.v, actual[self.k])

                    except AssertionError as err:
                        logger.error("Fail...Expected, Actual{}".format(err))
                        logger.error("积分变更失败... {}".format(self.change_points))
                        print("积分变更失败... {}".format(self.change_points))
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
