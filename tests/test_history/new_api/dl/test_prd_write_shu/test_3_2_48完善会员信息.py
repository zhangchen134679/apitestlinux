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

cases = excel.read_data("improve_member_Info")


@pytest.mark.shu
@ddt.ddt
class TestImproveMemberInfo(unittest.TestCase):

    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["shu"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 从配置文件读取天猫店铺名称
        cls.tb_store_name = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["name"]

        # 从配置文件读取store_code
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]
# --------------------------------------------------------------------------------------------------------------------
        """
        :param class_mobile: 提取会员mobile..
               class_union_code: 提取会员union_code..
               验证通过原注册手机号更新, 见case35..具体替换数据见line100
               验证第一次修改生日, 见case35..具体替换数据见line100
               验证第二次更改生日, 见case36..具体替换数据见line100
               通过这个会员验证参数全部为空的场景、见case91..case92..具体替换数据见line100
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
        # union_code insert list
        cls.member_list.extend([cls.class_union_code])
# --------------------------------------------------------------------------------------------------------------------

    def setUp(self) -> None:

        # 调用会员注册接口
        self.register = handler_middle.register_member(self.brand, store_code=self.store_code, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register["data"]["union_code"]

        # union_code insert list
        self.member_list.append(self.union_code)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用全渠道会员绑定解绑(新)接口
        for index in range(0, len(cls.member_list)):
            cls.bind = handler_middle.MemberBinding(
                cls.brand, binding_type="0", value=cls.member_list[index], headers=cls.headers)
            cls.bind.try_bind()

    @allure.step("完善会员信息")
    @pytest.mark.write
    @pytest.mark.improve_member_Info
    @ddt.data(*cases)
    def test_improve_member_Info(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tb_store_name
        data_info = re.sub(r"#tb_store_name#", self.tb_store_name, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的原注册会员union_code..mobile..
        data_info = re.sub("#class_mobile#", self.class_mobile, str(data_info))
        data_info = re.sub("#class_union_code#", self.class_union_code, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的mobile
        data_info = re.sub("#random_mobile#", handler_middle.Handler().random_phone(
                                                        self.brand, headers=self.headers), str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        if eval(data_info)["case_id"] <= 28:
            """
            前28条case调用全渠道会员绑定解绑(新)接口
            acct_type账号类型的验证...
            """
            # 调用全渠道会员绑定解绑(新)接口
            bind = handler_middle.MemberBinding(self.brand, value=self.union_code, headers=self.headers)

            # 绑定天猫.京东.微信
            bind.all_bind()

        if 82 <= eval(data_info)["case_id"] <= 84:
            """
            用例82~用例84调用全渠道会员绑定解绑(新)接口
            绑定天猫会员更新验证...
            用例84天猫会员绑定解绑后..进行更新手机号的操作
            """
            # 调用全渠道会员绑定解绑(新)接口
            bind = handler_middle.MemberBinding(self.brand, value=self.union_code, headers=self.headers)

            # 绑定天猫
            bind.tb_bind(channel="976")

            if eval(data_info)["case_id"] == 84:
                # 调用全渠道会员绑定解绑(新)接口
                time.sleep(10)
                member_bind = handler_middle.MemberBinding(
                    self.brand, binding_type="0", value=self.union_code, headers=self.headers)

                # 解绑天猫会员
                member_bind.tb_bind(channel="976")
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中data值..
        replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])
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
                        self.brand, value=data["mobile"], headers=self.headers, query_type="mobile")

                    try:
                        address = "address"
                        change_log = "changeLog"
                        if expect_response[self.k][address]:
                            if expect_response[self.k][change_log]:
                                for key, value in self.v.items():
                                    if key in change_log:
                                        for keys, values in value[0].items():
                                            # print(values, self.actual_member_info["data"][key][0][keys])
                                            self.assertEqual(values, self.actual_member_info["data"][key][0][keys])

                                    else:
                                        if key in address:
                                            for keys, values in value[0].items():
                                                # print(values, self.actual_member_info["data"][key][0][keys])
                                                self.assertEqual(values, self.actual_member_info["data"][key][0][keys])

                                        else:
                                            # print(value, self.actual_member_info["data"][key])
                                            self.assertEqual(value, self.actual_member_info["data"][key])

                            else:
                                for key, value in self.v.items():
                                    if key in address:
                                        for keys, values in value[0].items():
                                            # print(values, self.actual_member_info["data"][key][0][keys])
                                            self.assertEqual(values, self.actual_member_info["data"][key][0][keys])

                                    else:
                                        # print(value, self.actual_member_info["data"][key])
                                        self.assertEqual(value, self.actual_member_info["data"][key])

                    except AssertionError as err:
                        logger.error("actual_member_info: {}".format(self.actual_member_info))
                        raise err

                else:
                    if self.k in "data" and actual["code"] == 0:
                        for self.key, self.value in self.v.items():
                            # print(self.value, actual[self.k][self.key])
                            self.assertEqual(self.value, actual[self.k][self.key])

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


