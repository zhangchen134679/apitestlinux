from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_lrp

cases = excel.read_data("member_banding")


@ddt.ddt
class TestMemberBinding(unittest.TestCase):

    member_code = []

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrp"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 从配置文件读取天猫店铺名称
        cls.tb_store_name = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["name"]

        # 从配置文件读取store_code
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]

        # 调用会员注册接口  -- 注册一个绑定媒体信息的会员,验证case_id: 19,20,21,22
        cls.register_media = handler_middle.register_member(cls.brand, store_code=cls.store_code, headers=cls.headers)

        # 提取会员union_code
        cls.media_code = cls.register_media["data"]["union_code"]

        # media_code插入到列表...
        cls.member_code.append(cls.media_code)

        # 调用全渠道会员绑定解绑(新)接口
        cls.Bind = handler_middle.MemberBinding(cls.brand, binding_type="1", value=cls.media_code, headers=cls.headers)
        cls.Bind.all_bind()

    def setUp(self) -> None:

        # 调用会员注册接口
        self.register_member = handler_middle.register_member(self.brand, self.store_code, headers=self.headers)

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

        # 提取会员union_code
        self.union_code = self.register_member["data"]["union_code"]

        # union_code插入到列表...
        self.member_code.append(self.union_code)

    @classmethod
    def tearDownClass(cls) -> None:
        # 调用全渠道会员绑定解绑(新)接口
        for i in range(0, len(cls.member_code)):
            if i == 0:
                for index in range(0, 2):
                    cls.bind = handler_middle.MemberBinding(cls.brand, binding_type="0",
                                                            value=cls.member_code[i], headers=cls.headers)
                    cls.bind.try_bind()
            else:
                cls.bind = handler_middle.MemberBinding(cls.brand, binding_type="0",
                                                        value=cls.member_code[i], headers=cls.headers)
                cls.bind.try_bind()

    @ddt.data(*cases)
    def test_member_binding(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的tb_nick
        data_info = re.sub(r"#taobao_nick#", handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的user_id
        data_info = re.sub(r"#user_id#", handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的open_id
        data_info = re.sub(r"#open_id#", handler_middle.Handler().random_num, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的seller_name
        data_info = re.sub(r"#seller_name#", self.tb_store_name, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的value值..data
        if eval(data_info)["case_id"] not in (19, 20, 21, 22):
            replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
            data_info = replace.replace_data(str(data_info))
        else:
            replace = handler_middle.ReplaceDate(self.brand, value=self.media_code, headers=self.headers)
            data_info = replace.replace_data(str(data_info))
# --------------------------------------------------------------------------------------------------------------------
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

                    try:
                        for self.keys, self.value in self.v.items():
                            self.assertEqual(self.value, actual[self.k][self.keys])

                    except AssertionError as err:
                        logger.error("againAssertFail...")
                        raise err

                else:
                    self.assertEqual(self.v, actual[self.k])

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

