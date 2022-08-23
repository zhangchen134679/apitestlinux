import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


class ExcelHandler:
    """
    测试用例格式转化为列表嵌套字典
    """
    def __init__(self, path):
        self.path = path
        self.work_book = None                               # 调用open_file时,声明一个work_book的对象

    def open_file(self):
        work_book = openpyxl.load_workbook(self.path)       # 实际上已经实例化一个work_book的对象
        self.work_book = work_book
        return work_book                                    # 返回的work_book对象

    def get_sheet(self, sheet_name):
        self.open_file()                                    # 2.调用open_file方法,拿到实例一个对象
        return self.work_book[sheet_name]                   # 3.通过实例对象.方法拿到sheet表单,并实例化sheet表单

    def read_data(self, sheet_name):
        sheet: Worksheet = self.get_sheet(sheet_name)       # 1.调用get_sheet方法
        my_list = []
        for i, j in enumerate(sheet):                     # 4.通过sheet表单.rows或者用list转化拿到所有的测试数据
            my_lit = []
            for v in j:
                my_lit.append(v.value)
            if my_lit[0] != 'skip':
               my_list.append(my_lit)

        new_list = []
        for i in my_list[1:]:
            my_dict = dict(zip(my_list[0], i))
            new_list.append(my_dict)
        return new_list

    def write(self, sheet_name, row, column, data):
        sheet: Worksheet = self.get_sheet(sheet_name)
        sheet.cell(row, column).value = data
        self.save()
        self.close()

    def save(self):
        self.work_book.save(self.path)

    def close(self):
        self.work_book.close()
