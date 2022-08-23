import time

from middleware.middle_pre.middle_write import handler_middle
from common.handler_requests import visit
from jsonpath import jsonpath
import unittest
import pytest
import allure
import json
import ddt
import re

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_write_common

cases = excel.read_data("query_activity_status")

handler = handler_middle.Handler


@pytest.mark.hr
@ddt.ddt
class TestMemberQueryActivityStatus(unittest.TestCase):

    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["hr"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        cls.store_code = handler_middle.Handler.yml_conf['crm_store'][cls.brand]["deal_store_no"]

        cls.product_code = handler_middle.Handler.yml_conf['crm_product'][cls.brand]["code"]

        cls.product_name = handler_middle.Handler.yml_conf['crm_product'][cls.brand]["name"]

        # cls.trade_no = handler_middle.Handler().random_trade

        # # 调用会员注册接口
        # cls.register_media = handler_middle.register_member(cls.brand, headers=cls.headers)
        #
        # # 提取会员union_code
        # cls.union_code = cls.register_media["data"]["union_code"]
        #
        # cls.order_result = handler_middle.upload_order(cls.brand, member_id=cls.union_code, store_code=cls.store_code,
        #                                                trade_no=cls.trade_no, total_price=1000, trade_price=1000,
        #                                                price=1000, amt=1000,
        #                                                commodity_code=cls.product_code, commodity_name=cls.product_name,
        #                                                headers=cls.headers)
        #
        # time.sleep(3)
        #
        # cls.order_history = handler_middle.query_order_history(cls.brand, value=cls.union_code, headers=cls.headers)
        #
        # try:
        #     # cls.order_detail = cls.order_history.get("data").get("orderInfos")[0].get("details")[0].get("detailNo")
        #     cls.order_detail = jsonpath(cls.order_history, "$..detailNo")[0]
        # except Exception as err:
        #     logger.error("order_detail.没有提取到")
        #
        # # union_code insert list
        # cls.member_list.append(cls.union_code)


    def setUp(self) -> None:

        # 调用会员注册接口
        self.register_media = handler_middle.register_member(self.brand, headers=self.headers)

        # 提取会员union_code
        self.union_code = self.register_media["data"]["union_code"]

        self.trade_no = handler_middle.Handler().random_trade

        self.order_result = handler_middle.upload_order(self.brand, member_id=self.union_code, store_code=self.store_code,
                                                       trade_no=self.trade_no, total_price=1000, trade_price=1000,
                                                       price=1000, amt=1000,
                                                       commodity_code=self.product_code, commodity_name=self.product_name,
                                                       headers=self.headers)

        time.sleep(3)

        self.order_history = handler_middle.query_order_history(self.brand, value=self.union_code, headers=self.headers)

        try:
            # cls.order_detail = cls.order_history.get("data").get("orderInfos")[0].get("details")[0].get("detailNo")
            self.order_detail = jsonpath(self.order_history, "$..detailNo")[0]
            time.sleep(3)

        except Exception as err:
            print(self.union_code)
            logger.error("order_detail.没有提取到")


        self.order_sendactivityinfo = handler_middle.send_activity_info(self.brand, value=self.union_code,
                                                                            trade_no=self.trade_no,
                                                                            detail_no=self.order_detail,
                                                                            sku_code=self.product_code,
                                                                            headers=self.headers)
        time.sleep(3)



            # cls.order_detail = cls.order_history.get("data").get("orderInfos")[0].get("details")[0].get("detailNo")



        # union_code insert list
        self.member_list.append(self.union_code)

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)


    @classmethod
    def tearDownClass(cls) -> None:
        pass

    @allure.step("...")
    @pytest.mark.write
    @pytest.mark.query_activity_status
    @ddt.data(*cases)
    def test_query_activity_status(self, data_info):

        # 替换用例中的brand_code
        data_info = re.sub(r"&brand_code&", self.brand, str(data_info))
        # 替换用例中的union_code
        data_info = re.sub("&union_code&", self.union_code, str(data_info))
        # 替换用例中的trade_no
        data_info = re.sub("&trade_no&", self.trade_no, str(data_info))
        # 替换用例中的detailNo
        data_info = re.sub("&order_detail&", self.order_detail, str(data_info))
        # 替换用例中的sku_code
        data_info = re.sub("&product_code&", self.product_code, str(data_info))

        # 转化数据格式
        data_info = eval(data_info)
        data = eval(data_info["data"])
        # logger.info(data)

        # replace = handler_middle.ReplaceDate(self.brand, value=self.union_code, headers=self.headers)
        # data_info = replace.replace_data(str(data_info))
        # data_info = eval(data_info)
        # data = eval(data_info["data"])
#  --------------------------------------------------------------------------------------------------------------------
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler.yml_conf["host"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)

        expect_response = json.loads(data_info["expect_response"])

        # print(expect_response)
        # print(actual)

        # print(actual)
        # print(self.register_media)
        #
        # print(self.order_result)
        #
        # print(self.order_history)
        #
        # print(self.order_detail)

        try:
            logger.info("第{}条用例断言...".format(data_info["case_id"]))
            # logger.info("预期结果为：{}".format(expect_response))
            # logger.info("实际结果为：{}".format(actual))
            self.assertEqual(expect_response, actual)
            logger.info("输入参数: {}".format(data))
            logger.info("预期结果为：{}".format(expect_response))
            logger.info("实际结果为: {}".format(actual))
            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))

        except AssertionError as err:
            self.result = "fail"
            logger.warning("输入参数: {}".format(data))
            logger.warning("预期结果为：{}".format(expect_response))
            logger.warning("实际结果为: {}".format(actual))
            logger.error("第{}条用例失败..Fail...Expected, Actual{}".format(data_info["case_id"], err))
            # print("data: {}".format(data))
            # print("response: {}".format(actual))
            raise err

        finally:
            logger.info("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    unittest.main()



