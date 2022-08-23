from middleware.middle_prd.middle_write import handler_middle
from common.handler_requests import visit
import json, ddt, re, allure, unittest, pytest, time

logger = handler_middle.Handler().logger

excel = handler_middle.Handler().excel_upload_CR_ALL

host = handler_middle.Handler.yml_conf["host"]

if host == 'https://dl-api.lorealchina.com/api/interface/third/vb':
    cases = excel.read_data("lrl_MemberInfoVerification_vb")

elif host == 'https://dl-api.lorealchina.com/api/interface/third/va':
    cases = excel.read_data("lrl_MemberInfoVerification_va")

brand = handler_middle.Handler.yml_conf["brand"]["lrl"]


@ddt.ddt
class TestMemberInfoVerification(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"][brand]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler.headers(brand_code=cls.brand)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    @ddt.data(*cases)
    def test_case(self, data_info):

        # replace = handler_middle.ReplaceDate(self.brand, value=None, headers=self.headers)
        # data_info = replace.replace_data(data_info)
        # data_info = eval(data_info)
        data = eval(data_info["data"])
        # --------------------------------------------------------------------------------------------------------------------

        logger.info("第{}条用例访问接口...".format(data_info["case_id"]))
        actual = visit(url=handler_middle.Handler.yml_conf["host"] + data_info["url"],
                       method=data_info["method"],
                       json=data,
                       headers=self.headers)


        logger.info(handler_middle.Handler.yml_conf["host"] + data_info["url"])

        expect_response = json.loads(data_info["expect_response"])

        # logger.info("第{}条用例断言...".format(data_info["expect_response"]))
        try:
            for self.k, self.v in expect_response.items():
                self.assertEqual(self.v, actual[self.k])

            self.result = "pass"
            logger.info("第{}条用例成功".format(data_info["case_id"]))
            logger.info("接口入参为：{}".format(data))
            logger.info("接口返回为：{}".format(actual))

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
