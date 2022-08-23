import unittest
import ddt

cases = [
    {"case_id": 1, "data": {'username': '123', 'password': '456'}},
    {"case_id": 2, "data": {'username': '123', 'password': '456'}},
    {"case_id": 3, "data": {'username': '123', 'password': '456'}}
]


@ddt.ddt
class TestLogin(unittest.TestCase):

    def setUp(self) -> None:

        if cases[0]["case_id"] == 1:
            print("???")
        else:
            print("!!")

    @ddt.data(*cases)
    def test_data(self, data_info):
        print(data_info)
        pass


if __name__ == '__main__':
    unittest.main()
