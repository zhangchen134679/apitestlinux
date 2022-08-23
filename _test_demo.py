from middleware.middle_pre.middle_query import handler_middle
from common.handler_requests import visit
import unittest
import pytest
import allure
import ddt

logger = handler_middle.Handler().logger

handler = handler_middle.Handler

cases = range(100)


@pytest.mark.lrl
@ddt.ddt
class TestQueryMemberInfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取brand
        cls.brand = handler_middle.Handler.yml_conf["brand"]["lrl"]

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=cls.brand)

        cls.data = {
            "Brand_code": cls.brand,
            "Program_code": cls.brand,
            "queryType": "mobile",
            "Value": "15890533563"
        }

    @allure.step("查询会员基本信息")
    @pytest.mark.query
    @pytest.mark.query_member_info
    @ddt.data(*cases)
    def test_query_member_info(self, data_info):
        # 调用接口
        logger.info("第{}条用例访问接口...".format(data_info))
        actual = visit(url="https://dl-api.lorealchina.com/api/interface/third/vb/member/queryMemberInfo",
                       method='post',
                       json=self.data,
                       headers=self.headers)
        try:
            self.assertEqual('请求成功', actual['msg'])
        except Exception as e:
            print(self.data)
            print(actual)
            raise e


if __name__ == "__main__":
    unittest.main()





