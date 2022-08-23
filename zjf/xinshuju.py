import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from common.handler_excel import ExcelHandler

work_book = openpyxl.load_workbook('ba上传模板.xlsx')
def write(self, sheet_name, row, column, data):
        sheet: Worksheet = self.get_sheet(sheet_name)
        sheet.cell(row, column).value = data

if __name__ == '__main__':
   r = ExcelHandler('ba上传模板.xlsx')
   for nRow in range(2,100002):
       data1 = r.write("BA", nRow, 2, 'Test001')
       data2 = r.write("BA", nRow, 3, 'Test002')

   r.save('ba上传模板.xlsx')
   r.close()
   print(1)

