from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import json, ddt, re, allure, unittest, pytest, time

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_smoke_d2s

cases = excel.read_data("smoke_request")

time.sleep(2)
@pytest.mark.d2s
@ddt.ddt
class TestSmokeTest(unittest.TestCase):
    """
    set_vender_code: 供应商编号,用于积分变更接口、会员积分变更状态查询
    set_vender_seq_code:生成一次兑换流水号,用于积分变更接口,会员积分变更状态查询,上传兑换信息(仅安客诚使用),会员绑定查询,会员绑定解绑,
    兑换订单绑定,全渠道会员绑定查询,全渠道会员绑定,全渠道会员绑定状态查询(新),全渠道会员绑定解绑(新),积分变更(专用）,上传兑换信息(新),
    会员积分变更（可欠账）
    set_trade_no: 生成一次订单编号,用于上传订单,订单明细查询,上传兑换信息(仅安客诚使用),兑换订单绑定,验证订单是否可退,上传兑换信息(新),
    订单状态更新接口
    set_baUserId: 生成一次baUserId,用于企业微信BA绑定解绑or企业微信BA绑定查询
    test_member: 生成一次test_member,用于会员信息上传接口
    """
    sleep = 10
    member_list = []
    set_vender_code = "1"
    set_vender_seq_code = handler_middle.Handler().random_num
    set_trade_no = handler_middle.Handler().random_trade
    set_baUserId = handler_middle.Handler().random_num
    test_member = handler_middle.Handler().random_num


    @classmethod
    def setUpClass(cls) -> None:

        with open('test.txt', 'r') as f:
            brand = f.read()

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"][brand]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler.headers(brand_code=cls.brand)

        # 调用会员注册接口
        cls.register_media: dict = handler_middle.register_member(cls.brand, headers=cls.headers)

        # 获取会员编号
        cls.member = cls.register_media["data"]["union_code"]

        # 调用会员注册接口
        cls.register_quit: dict = handler_middle.register_member(cls.brand, headers=cls.headers)

        # 获取会员编号
        cls.quit_member = cls.register_quit["data"]["union_code"]

        # 获取会员编号添加到列表中
        cls.member_list.append(cls.member)

    @classmethod
    def tearDownClass(cls) -> None:
        for index in range(len(cls.member_list)):
            cls.unbind = handler_middle.MemberBinding(
                cls.brand, value=cls.member_list[index], headers=cls.headers, binding_type="0")
            if index == 0:
                time.sleep(cls.sleep)
                cls.unbind.wx_bind(channel='6P0')
                time.sleep(cls.sleep)
                cls.unbind.jd_bind(channel='9AL')
                cls.quit_result = cls.unbind.quit_member()
            else:
                cls.quit_result = cls.unbind.quit_member()

    @allure.step("冒烟测试")
    @pytest.mark.smoke
    @ddt.data(*cases)
    def test_case_most(self, data_info):
        
        allure.dynamic.feature('测试品牌{}'.format(self.brand))  # 测试品牌
        allure.dynamic.title(data_info["interface"])  # 报告标题
        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))

        # 替换用例中的union_code
        data_info = re.sub(r"&union_code&", self.member, str(data_info))

        # 替换用例中的quit_member
        data_info = re.sub(r"&quit_member&", self.quit_member, str(data_info))

        # 替换用例中的test_member
        data_info = re.sub(r"&test_member&", self.test_member, str(data_info))

        # 替换用例中的trade_no
        data_info = re.sub(r"&tradeNo&", self.set_trade_no, str(data_info))

        # 替换用例中的baUserId
        data_info = re.sub(r"&baUserId&", self.set_baUserId, str(data_info))

        # 替换用例中的vender_code
        data_info = re.sub(r"&vender_code&", self.set_vender_code, str(data_info))

        # 替换用例中的vender_seq_code
        data_info = re.sub(r"&vender_seq_code&", self.set_vender_seq_code, str(data_info))

        if eval(data_info)["case_id"] in (23, 24, 33, 34, 35, 36, 54, 55):
            """
            23:会员绑定查询、24:会员绑定解绑、33:全渠道会员绑定查询、34:全渠道会员绑定、
            35:全渠道会员绑定状态查询(新)、36:全渠道会员绑定解绑(新)、54:企业微信BA绑定解绑、55:企业微信BA绑定查询
            """
            replace = handler_middle.ReplaceDate(self.brand, value=self.member, headers=self.headers)
            data_info = replace.replace_data(data_info)
        replace = handler_middle.ReplaceDate(self.brand, value=None, headers=self.headers)
        data_info = replace.replace_data(data_info)
        data_info = eval(data_info)
        data = eval(data_info["data"])
        # --------------------------------------------------------------------------------------------------------------------
        """
        44:完善会员信息
        解绑天猫会员后进行更新会员信息
        """
        if data_info["case_id"] == 44:
            unbind = handler_middle.MemberBinding(self.brand, value=self.member, headers=self.headers, binding_type="0")
            time.sleep(self.sleep)
            unbind.tb_bind(channel='976')
        # --------------------------------------------------------------------------------------------------------------------
        # 替换headers的uuid...
        self.headers = handler_middle.Handler.replace_uuid(self.headers)
        # --------------------------------------------------------------------------------------------------------------------
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler_middle.Handler.yml_conf["host"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)
        print(actual)

        logger.info(handler_middle.Handler.yml_conf["host"] + data_info["url"])

        """将注册成功后的会员编号添加到列表中"""
        if data_info["case_id"] in (1, 43, 48):
            try:
                self.member_list.append(actual["data"]["union_code"])
            except KeyError:
                logger.error("self.member_list.append..Error")

        expect_response = json.loads(data_info["expect_response"])

        logger.info("第{}条用例断言...".format(data_info["case_id"]))
        try:
            if data_info["case_id"] in (34, 35, 36, 43, 44):
                """
                34:全渠道会员绑定、35:全渠道会员绑定状态查询(新)、36:全渠道会员绑定解绑(新)
                43:会员注册绑定、44：完善会员信息
                """
                for self.k, self.v in expect_response.items():
                    if self.k in "data":
                        for self.key, self.value in self.v.items():
                            self.assertEqual(self.value, actual[self.k][self.key])
                    else:
                        self.assertEqual(self.v, actual[self.k])

                """会员资质校验接口Assert"""
            elif data_info["case_id"] == 53:
                for self.k, self.v in expect_response.items():
                    if self.k in "data":
                        for self.key, self.value in self.v.items():
                            if self.key in "userInfo":
                                for self.keys, self.values in self.value.items():
                                    # print(self.keys, self.values)
                                    self.assertEqual(self.values, actual[self.k][self.key][self.keys])
                            else:
                                # print(self.key, self.value, "assert:", self.value, actual[self.k][self.key])
                                self.assertEqual(self.value, actual[self.k][self.key])
                    else:
                        # print(self.v, actual[self.k])
                        self.assertEqual(self.v, actual[self.k])

            else:
                for self.k, self.v in expect_response.items():
                    self.assertEqual(self.v, actual[self.k])

            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))

        except Exception as err:
            self.result = "fail"
            logger.error("data: {}".format(data))
            logger.error("response: {}".format(actual))
            logger.error("第{}条用例失败".format(data_info["case_id"]))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()
