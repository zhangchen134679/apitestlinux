from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import json
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_shu

cases = excel.read_data("member_add_tags")


@ddt.ddt
class TestMemberAddTags(unittest.TestCase):

    source_tag = "MRM"

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["shu"]

        # 从配置文件读取token..username
        cls.username = handler_middle.Handler.yml_conf["access_token"][cls.brand]["username"]

        # 从配置文件读取token..password
        cls.password = handler_middle.Handler.yml_conf["access_token"][cls.brand]["password"]

        # 从配置文件读取deal_store_no
        cls.store_code = handler_middle.Handler.yml_conf["crm_store"][cls.brand]["deal_store_no"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(username=cls.username, password=cls.password)

        # 调用会员注册接口
        cls.register_member = handler_middle.register_member(cls.brand, store_code=cls.store_code, headers=cls.headers)

        # 提取会员union_code
        cls.union_code = cls.register_member["data"]["union_code"]

    def setUp(self) -> None:

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用会员退会接口
        handler_middle.quit_member(cls.brand, value=cls.union_code, headers=cls.headers, query_type="union_code")

    @ddt.data(*cases)
    def test_member_add_tags(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"#brand_code#", self.brand, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的member_code
        data_info = re.sub(r"#union_code#", self.union_code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的source_tag
        data_info = re.sub(r"#source_tag#", self.source_tag, str(data_info))
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

        expect_response = json.loads(data_info["expect_response"])

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():

                if self.k in "data" and actual["code"] == 0:

                    # 调用查询自定义会员标签接口
                    actual_tags = handler_middle.query_member_tags(
                        self.brand, value=self.union_code, source_tag=self.source_tag, headers=self.headers)

                    try:
                        logger.info("第{}条用例againAssert...".format(data_info["case_id"]))
                        for self.key, self.value in self.v.items():
                            self.assertEqual(self.value, actual_tags[self.k][self.key])

                    except AssertionError as err:
                        logger.error("againAssertFail...Expected, Actual{}".format(err))
                        raise err

                else:
                    try:
                        self.assertEqual(self.v, actual[self.k])
                    except AssertionError as err:
                        logger.error("Fail...Expected, Actual{}".format(err))
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
