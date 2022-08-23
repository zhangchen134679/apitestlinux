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

excel = handler_middle.Handler().excel_mny

cases = excel.read_data("member_update")


@pytest.mark.shu
@ddt.ddt
class TestMemberUpdate(unittest.TestCase):

    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["shu"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 从配置文件读取store_code
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]
# --------------------------------------------------------------------------------------------------------------------
        """
        :param class_mobile: 提取会员mobile..
               class_union_code: 提取会员union_code..
               验证通过原注册手机号更新, 见case23..具体替换数据见line127
               验证第一次修改生日, 见case24..具体替换数据见line127
               验证第二次更改生日, 见case25..具体替换数据见line127
               """
        # 调用会员注册接口
        cls.class_register = handler_middle.register_member(cls.brand, store_code=cls.store_code, headers=cls.headers)

        # 提取会员union_code
        cls.class_union_code = cls.class_register["data"]["union_code"]

        # 查询注册会员基本信息
        cls.query_member = handler_middle.query_member_info(cls.brand, value=cls.class_union_code, headers=cls.headers)

        # 提取会员mobile
        cls.class_mobile = cls.query_member["data"]["mobile"]
# --------------------------------------------------------------------------------------------------------------------
        """
        :param class_tb_mobile: 提取会员mobile..
               class_tb_union_code: 提取会员union_code..
               验证天猫会员更新, 见case63-75..具体替换数据见line132
               """
        # 调用会员注册接口
        cls.class_tb_register = handler_middle.register_member(
                cls.brand, store_code=cls.store_code, headers=cls.headers, chanel_code="976")

        # 提取会员union_code
        cls.class_tb_union_code = cls.class_tb_register["data"]["union_code"]

        # 查询注册会员基本信息
        cls.query_member = handler_middle.query_member_info(cls.brand, value=cls.class_tb_union_code, headers=cls.headers)

        # 提取会员mobile
        cls.class_tb_mobile = cls.query_member["data"]["mobile"]
# --------------------------------------------------------------------------------------------------------------------
        # union_code insert list
        cls.member_list.extend([cls.class_union_code, cls.class_tb_union_code])
# --------------------------------------------------------------------------------------------------------------------

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用会员退会接口
        for index in range(0, len(cls.member_list)):
            handler_middle.quit_member(
                cls.brand, value=cls.member_list[index], headers=cls.headers, query_type="union_code")

    def setUp(self) -> None:

        # 生成当前时间并转化格式
        self.time = time.strftime("%Y-%m-%d %H:%M:%S")

        # 调用会员注册接口
        self.register = handler_middle.register_member(self.brand, store_code=self.store_code, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register["data"]["union_code"]

        # union_code insert list
        self.member_list.append(self.union_code)

    @allure.step("会员基本信息更新")
    @pytest.mark.write
    @pytest.mark.member_update
    @ddt.data(*cases)
    def test_member_update(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub("#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的mobile
        data_info = re.sub("#mobile#", handler_middle.Handler().random_phone(
                                        self.brand, headers=self.headers), str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的union_code
        data_info = re.sub("#union_code#", self.union_code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的consentTime
        data_info = re.sub("#time#", self.time, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的store_code
        data_info = re.sub("#store_code#", self.store_code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的原注册会员union_code..mobile..
        data_info = re.sub("#class_mobile#", self.class_mobile, str(data_info))
        data_info = re.sub("#class_union_code#", self.class_union_code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中绑定天猫会员的union_code..mobile..
        data_info = re.sub("#class_tb_mobile#", self.class_tb_mobile, str(data_info))
        data_info = re.sub("#class_tb_union_code#", self.class_tb_union_code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        """
        :param 读取配置文件的线下门店替换case29中天猫门店, 从而验证更新时...门店不会被更新
            """
        # 替换用例中的offline_store_code
        data_info = re.sub("#offline_store_code#", handler_middle.Handler.
                           yml_conf["crm_store"][self.brand]["offline_store_no"], str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 转化数据格式
        data_info = eval(data_info)
        data = eval(data_info["data"])
# --------------------------------------------------------------------------------------------------------------------
        if data_info["case_id"] == 69:
            """
            : 验证case67..调用接口前进行天猫解绑操作,而后更新会员基本信息..
            : case68调用更新接口时用case67已更新好的数据,非必填参数为空..调用查询接口断言case67的会员基本信息未变化
                    """
            # 调用全渠道会员绑定解绑(新)接口
            member_bind = handler_middle.MemberBinding(
                            self.brand, binding_type="0", value=self.class_tb_union_code, headers=self.headers)

            # 解绑天猫会员
            member_bind.tb_bind(channel="976")
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

        expect_response = json.loads(data_info["{}_expect_response".format(self.brand)])

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():

                if self.k in "expect_member_info":
                    self.actual_member_info = handler_middle.query_member_info(
                                    self.brand, value=data["union_code"], headers=self.headers)
                    try:
                        address = "address"
                        change_log = "changeLog"
                        if expect_response[self.k][address]:
                            for key, value in self.v.items():
                                if key in address:
                                    for keys, values in value[0].items():
                                        # print(values, actual_member_info["data"][key][0][keys])
                                        self.assertEqual(values, self.actual_member_info["data"][key][0][keys])

                                else:
                                    # print(value, actual_member_info["data"][key])
                                    self.assertEqual(value, self.actual_member_info["data"][key])

                        elif expect_response[self.k][change_log]:
                            for key, value in self.v.items():
                                if key in change_log:
                                    for keys, values in value[0].items():
                                        # print(values, actual_member_info["data"][key][0][keys])
                                        self.assertEqual(values, self.actual_member_info["data"][key][0][keys])

                                else:
                                    # print(value, actual_member_info["data"][key])
                                    self.assertEqual(value, self.actual_member_info["data"][key])

                        else:
                            for self.key, self.value in self.v.items():
                                # print(self.value, actual_member_info["data"][self.key])
                                self.assertEqual(self.value, self.actual_member_info["data"][self.key])

                    except AssertionError as err:
                        logger.error("actual_member_info: {}".format(self.actual_member_info))
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


