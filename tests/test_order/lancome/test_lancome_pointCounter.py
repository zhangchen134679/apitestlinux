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

excel = handler_middle.Handler().excel_upload_change_grade_LAN

cases = [
    {'case_id': 1, 'amount': '999', 'grade': '50', 'point': '1998'},
    {'case_id': 2, 'amount': '1000', 'grade': '50', 'point': '2500'},
    {'case_id': 3, 'amount': '2000', 'grade': '50', 'point': '5500'},
    {'case_id': 4, 'amount': '3000', 'grade': '50', 'point': '9000'},
    {'case_id': 5, 'amount': '4000', 'grade': '50', 'point': '11000'},
    {'case_id': 6, 'amount': '5000', 'grade': '50', 'point': '18000'},
    {'case_id': 7, 'amount': '6000', 'grade': '50', 'point': '20000'},
    {'case_id': 8, 'amount': '7000', 'grade': '50', 'point': '25000'},
    {'case_id': 9, 'amount': '8000', 'grade': '50', 'point': '27000'},
    {'case_id': 10, 'amount': '10000', 'grade': '50', 'point': '35000'},
    {'case_id': 11, 'amount': '16000', 'grade': '50', 'point': '55000'},
    {'case_id': 12, 'amount': '36000', 'grade': '50', 'point': '109000'},
    {'case_id': 13, 'amount': '21000', 'grade': '50', 'point': '71500'},
    {'case_id': 14, 'amount': '21000', 'grade': '40', 'point': '71500'},
    {'case_id': 15, 'amount': '21000', 'grade': '30', 'point': '79700'},
    {'case_id': 16, 'amount': '21000', 'grade': '60', 'point': '79700'},
    {'case_id': 17, 'amount': '21000', 'grade': '20', 'point': '92000'},
    {'case_id': 18, 'amount': '21000', 'grade': '10', 'point': '112500'},
]

brand = handler_middle.Handler.yml_conf["brand"]["lancome"]


@ddt.ddt
class TestPointCounter(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lancome"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

    def setUp(self) -> None:

        # 替换headers的uuid...
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

    @ddt.data(*cases)
    def test_upload_order_verifyGrade(self, data_info):
        amount = data_info['amount']
        grade = data_info['grade']
        point = data_info['point']
        data = {
            "brand_code": self.brand,
            "program_code": self.brand,
            "amount": amount,
            "grade_code": grade}
        actual = visit(url=handler_middle.Handler.yml_conf["host"] + '/member/pointCounter', method='post',
                       json=data,
                       headers=self.headers)

        if actual['msg'] == '请求成功':
            try:
                self.assertEqual(point, actual['data']['points'])
                self.result = "pass"
                logger.info("第{}条用例成功".format(data_info["case_id"]))
                logger.info("预期结果{}-----实际结果{}".format(point,actual['data']['points']))
            except AssertionError as err:
                self.result = "fail"
                logger.error("第{}条用例失败".format(data_info["case_id"]))
                raise err
        else:
            logger.error('接口访问失败{}'.format(actual))


if __name__ == "__main__":
    unittest.main()
