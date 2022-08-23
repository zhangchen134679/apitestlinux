# pre环境
# from middleware.middle_pre_back.middle_write import handler_middle

# prd环境
from middleware.middle_prd.middle_write import handler_middle

from common.handler_excel import ExcelHandler
import unittest
import pytest
import ddt
import os

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"data\会员退会名单.xlsx")

excel = ExcelHandler(file_path)

cases = excel.read_data("member")

brand = "lrp"


@pytest.mark.lrp
@ddt.ddt
class TestDelete(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=brand)

    @pytest.mark.quit_member
    @ddt.data(*cases)
    def test_delete_member(self, data_info):

        # 替换headers的uuid
        self.headers = handler_middle.Handler().replace_uuid(self.headers)

        bind = handler_middle.MemberBinding(
            brand_code=brand, binding_type="0", value=str(data_info["data"]),
            headers=self.headers, query_type="union_code")

        try:
            print(bind.tb_bind("976"))
        except TypeError:
            pass
        finally:
            try:
                print(bind.jd_bind("9AL"))
            except TypeError:
                pass
            finally:
                try:
                    print(bind.wx_bind("6P0"))
                except TypeError:
                    pass
                finally:
                    print(bind.quit_member())
                    print("quit_member", data_info["data"])


if __name__ == "__main__":
    unittest.main()
    pass
