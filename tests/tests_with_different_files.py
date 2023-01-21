import zipfile
import os
import xlrd
import csv
from zipfile import ZipFile
from os.path import basename
from PyPDF2 import PdfReader

# Путь к файлам
path_with_files = (os.path.join(os.path.dirname(os.path.abspath(__file__)) + '\\media'))
# Список имен файлов
list_with_files = os.listdir(path_with_files)
# Путь к zip архиву
zip_path = os.path.abspath((os.path.dirname(__file__)) + '\\test.zip')

# Создаем архив и записываем в него файлы
with zipfile.ZipFile('test.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
    for file in list_with_files:
        add_file = os.path.join(path_with_files, file)
        zf.write(add_file, basename(add_file))


def test_files_added():
    zip_ = ZipFile(zip_path)
    assert zip_.namelist() == ['CSV_format.csv', 'PDF_format.pdf', 'XSLX_format.xls']


def test_read_pdf():
    with zipfile.ZipFile(zip_path) as zf:
        file_new = zf.extract('PDF_format.pdf')
        reader = PdfReader(file_new)
        page = reader.pages[0]
        text = page.extract_text()
        assert text == 'Привет  '
    os.remove('PDF_format.pdf')


def test_read_xls():
    with zipfile.ZipFile(zip_path) as zf:
        file_new = zf.extract('XSLX_format.xls')
        book = xlrd.open_workbook(file_new)
        sheet = book.sheet_by_index(0)
        assert sheet.cell_value(rowx=1, colx=0) == 'Petr'
    os.remove('XSLX_format.xls')


def test_read_csv():
    with zipfile.ZipFile(zip_path) as zf:
        file_new = zf.extract('CSV_format.csv')
        with open(file_new, newline='') as f:
            reader = csv.reader(f)
            result = []
            for row in reader:
                result.append(row)
                assert result[0][1] == 'Period'
    os.remove('CSV_format.csv')