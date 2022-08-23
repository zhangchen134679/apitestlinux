from middleware.middle_pre.middle_write import handler_middle
from common.handler_requests import visit
import unittest
import pytest
import allure
import json
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_write_common

cases = excel.read_data("member_gift_record")

handler = handler_middle.Handler


@pytest.mark.lrl
@ddt.ddt
class TestSaveMemberGiftRecord(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrl"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        # 调用会员注册接口
        cls.register_member = handler_middle.register_member(cls.brand, headers=cls.headers)

        # 提取会员union_code
        cls.union_code = cls.register_member["data"]["union_code"]

    def setUp(self) -> None:

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    @classmethod
    def tearDownClass(cls) -> None:

        # 调用会员退会接口
        handler_middle.quit_member(cls.brand, value=cls.union_code, headers=cls.headers, query_type="union_code")

    @allure.step("保存会员入会礼品记录")
    @pytest.mark.write
    @pytest.mark.member_gift_record
    @ddt.data(*cases)
    def test_member_gift_record(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
#  --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的union_code
        data_info = re.sub(r"&union_code&", self.union_code, str(data_info))
# --------------------------------------------------------------------------------------------------------------------
        # 替换用例中的data..
        replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
        data_info = replace.replace_data(str(data_info))
        data_info = eval(data_info)
        data = eval(data_info["data"])
# --------------------------------------------------------------------------------------------------------------------
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler.yml_conf["host"] + handler.yml_conf["var"]["vb_all"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)

        expect_response = json.loads(data_info["{}_expect_response".format(self.brand)])

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            for self.k, self.v in expect_response.items():

                if self.k in "data" and actual["code"] == 0:
                    actual_gift_record = handler_middle.query_member_gift_record(
                                    self.brand, value=self.union_code, headers=self.headers)

                    try:
                        for self.key, self.value in self.v.items():
                            self.assertEqual(self.value, actual_gift_record[self.k][self.key])

                    except AssertionError as err:
                        logger.error("actual_gift_record: {}".format(actual_gift_record))
                        raise err

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



