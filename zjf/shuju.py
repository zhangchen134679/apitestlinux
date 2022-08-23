import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


class ExcelHandler:
    """
    讲测试用例格式转化为列表嵌套字典
    """
    def __init__(self, path):
        self.path = path
        self.work_book = None

    def open_file(self):
        work_book = openpyxl.load_workbook(self.path)
        self.work_book = work_book
        return work_book

    def get_sheet(self, sheet_name):
        self.open_file()
        return self.work_book[sheet_name]

    #def read_data(self, sheet_name):


    def write(self, sheet_name, row, column, data):
        sheet: Worksheet = self.get_sheet(sheet_name)
        sheet.cell(row, column).value = data
        self.save()
        self.close()

    def save(self):
        self.work_book.save(self.path)

    def close(self):
        self.work_book.close()

if __name__ == '__main__':
   r = ExcelHandler('ba上传模板.xlsx')
   for nRow in range(2,100002):
       data1 = r.write("BA",nRow,2,'Test001')


   print(1)

