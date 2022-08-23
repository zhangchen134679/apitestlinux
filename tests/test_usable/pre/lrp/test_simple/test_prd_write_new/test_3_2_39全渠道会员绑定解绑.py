from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
from jsonpath import jsonpath
import unittest
import pytest
import allure
import json
import time
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_write_common_simple

cases = excel.read_data("member_banding")


@pytest.mark.lrp
@ddt.ddt
class TestMemberBinding(unittest.TestCase):

    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrp"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)
# --------------------------------------------------------------------------------------------------------------------
        """
        media_register: 通过setUpClass注册一个会员..且绑定天猫,京东,微信..
        bind.all_bind(): 绑定天猫,京东,微信..
        media_mobile: 提取会员mobile...具体替换数据见line139
        mix_mobile: 提取会员mix_mobile...具体替换数据见line142
        结合media_register,class_register会员,主要验证用例33,34,35
        使用media_register的media_mobile,mix_mobile...使用class_register的openId,jd_pin...验证绑定微信京东天猫失败..
        """
        # 调用会员注册接口
        cls.media_register = handler_middle.register_member(cls.brand, headers=cls.headers)

        # 提取会员union_code
        cls.class_media_code = cls.media_register["data"]["union_code"]

        # 查询注册会员基本信息
        cls.query_member = handler_middle.query_member_info(cls.brand, value=cls.class_media_code, headers=cls.headers)

        # 调用全渠道会员绑定解绑(新)接口
        cls.bind = handler_middle.MemberBinding(cls.brand, value=cls.class_media_code, headers=cls.headers)

        # 绑定天猫..京东..微信..
        cls.bind.all_bind()

        # 提取会员mobile
        cls.media_mobile = cls.query_member["data"]["mobile"]

        # 提取会员mix_mobile
        cls.media_mix_mobile = jsonpath(cls.query_member, "$..media_account[?(@.type=='2')].accountNo")[0]
# --------------------------------------------------------------------------------------------------------------------
        """
        class_register: 通过setUpClass注册一个会员..验证23-53条用例的场景
        class_union_code: 调用ReplaceDate方法时传入member_code替换用户需要用到的数据..具体替换数据见line175    
        """
        # 调用会员注册接口
        cls.class_register = handler_middle.register_member(cls.brand, headers=cls.headers)

        # 提取会员union_code
        cls.class_union_code = cls.class_register["data"]["union_code"]
# --------------------------------------------------------------------------------------------------------------------
        # union_code insert list
        cls.member_list.extend([cls.class_media_code, cls.class_union_code])
# --------------------------------------------------------------------------------------------------------------------

    def setUp(self) -> None:
        """
        register_member: 通过setUp注册会员..
        1.验证1-22条用例的场景
        2.验证36-53条用例的场景..(解绑)
        not_bind_mobile: 用于用例38.39.44.45、输入已注册未绑定的手机号验证解绑失败..具体替换数据见line145
        not_bind_mix_mobile: 用于用例50.51、输入已注册未绑定的加密手机号验证解绑失败..具体替换数据见line148
        """
        # 调用会员注册接口
        self.register_member = handler_middle.register_member(self.brand, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register_member["data"]["union_code"]

        # 查询注册会员基本信息
        self.query_member = handler_middle.query_member_info(self.brand, self.union_code, headers=self.headers)

        # 提取会员mobile
        self.not_bind_mobile = self.query_member["data"]["mobile"]

        # 提取会员加密手机号
        self.not_bind_mix_mobile = jsonpath(self.query_member, "$..media_account[?(@.type=='2')].accountNo")[0]

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

        # union_code insert list
        self.member_list.append(self.union_code)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用全渠道会员绑定解绑(新)接口
        for index in range(0, len(cls.member_list)):
            cls.bind = handler_middle.MemberBinding(
                            cls.brand, binding_type="0", value=cls.member_list[index], headers=cls.headers)
            cls.bind.try_bind()

    @allure.step("全渠道会员绑定解绑")
    @pytest.mark.write
    @pytest.mark.member_binding
    @ddt.data(*cases)
    def test_member_binding(self, data_info):
        allure.dynamic.title(str(data_info['title']))
        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的media_mobile
        data_info = re.sub(r"&media_mobile&", self.media_mobile, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的media_mix_mobile
        data_info = re.sub(r"&media_mix_mobile&", self.media_mix_mobile, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的not_bind_mobile
        data_info = re.sub(r"&not_bind_mobile&", self.not_bind_mobile, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的not_bind_mix_mobile
        data_info = re.sub(r"&not_bind_mix_mobile&", self.not_bind_mix_mobile, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的user_id
        data_info = re.sub(r"&random_user_id&", "jd_pin" + handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的open_id
        data_info = re.sub(r"&random_open_id&", "open_id" + handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tb_nick
        data_info = re.sub(r"&random_taobao_nick&", "tb_nick" + handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的data..
        """
        if case_id <= 22
        每次通过setUp初始化一个会员..通过if..value=self.union_code..来进行前22条用例的数据替换操作..
        encryptMobile..mobile..
        if case_id >= 23
        通过if..value=self.class_union_code..来进行23-53条用例的数据替换操作..
        encryptMobile..mobile..jd_pin..openId
        """
        if eval(data_info)["case_id"] <= 22:
            replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
            data_info = replace.replace_data(str(data_info))
        else:
            replace = handler_middle.ReplaceDate(self.brand, value=self.class_union_code, headers=self.headers)
            data_info = replace.replace_data(str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])
# --------------------------------------------------------------------------------------------------------------------
        """
        if..sleep == true
        等待10s后访问接口请求..否则encryptMobile..jd_pin..openId重复
        """
        if data_info["sleep"]:
            time.sleep(10)
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
                if self.k in "data" and actual["code"] == 0:
                    for self.keys, self.value in self.v.items():
                        self.assertEqual(self.value, actual[self.k][self.keys])

                else:
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