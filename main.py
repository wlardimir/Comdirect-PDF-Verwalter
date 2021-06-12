import os
import macos_tags
import sys
import shutil
import time
import datetime
from PyPDF2 import PdfFileReader
from os import path
from glob import glob
from pathlib import Path
from PyPDF2 import PdfFileReader

# === Vars ===

comdirect = "Comdirect"
ignore_list = ["Finanzreport", "Kosteninformation"]
annual_tax_certificate = ["Jahressteuerbescheinigung"]

years_list = []
date_list = []

# === Defs ===

def comdirect_tags_macos(pdf_item_list):
    pdfcounter = 0

    while pdfcounter < len(pdf_item_list):
        macos_tags.add(comdirect, file=pdf_item_list[pdfcounter])
        pdfcounter += 1

def file_end_with_pdf(dr, ext):
    return glob(path.join(dr, "*.{}".format(ext)))


def set_create_date(pdf_list, ignore_list):
    pdf_list = [pdfItem for pdfItem in pdf_list if not any(
        ignoreItem in pdfItem for ignoreItem in ignore_list)]
    pdfcounter = 0

    while pdfcounter < len(pdf_list):
        day = int(pdf_list[pdfcounter][-20:-18])
        month = int(pdf_list[pdfcounter][-17:-15])
        year = int(pdf_list[pdfcounter][-14:-10])

        date = datetime.datetime(year=year, month=month, day=day)
        modTime = time.mktime(date.timetuple())

        os.utime(pdf_list[pdfcounter], (modTime, modTime))

        pdfcounter += 1


def remove_with_no_Licensee(listpdf, listignore):
    pdf = [pdfItem for pdfItem in listpdf if not any(ignoreItem in pdfItem for ignoreItem in listignore)]
    return pdf


def remove_duplicates(listofElements):
    uniqueList = []
    for elem in listofElements:
        if elem not in uniqueList:
            uniqueList.append(elem)
    return uniqueList


def generate_pdf_years(pdf_list):
    year_list = []
    pdfcounter = 0

    while pdfcounter < len(pdf_list):
        reader = PdfFileReader(pdf_list[pdfcounter])
        metadata = reader.getDocumentInfo()
        licensee = metadata['/Licensee']

        if comdirect in licensee:
            macos_tags.add(comdirect, file=pdf_list[pdfcounter])
            years = pdf_list[pdfcounter][-14:-10]
            year_list.append(years)
            year_list = remove_duplicates(year_list)

        pdfcounter += 1

    return year_list


def return_date(pdf_list, date_list):
    x = 0
    while x < len(pdf_list):
        years = pdf_list[x][-14:-10]
        date_list.append(years)
        x += 1

    return date_list


def put_in_folder(pdf_list, year_list):
    pdfcounter = 0
    while pdfcounter < len(pdf_list):
        for year_listItem in year_list:
            if year_listItem in pdf_list[pdfcounter]:
                Path(year_listItem).mkdir(parents=True, exist_ok=True)
                shutil.move(pdf_list[pdfcounter], year_listItem)
                pdfcounter += 1

            else:
                sys.exit("Error message")

        pdfcounter += 1


def put_rest_pdf_to_folder(pdf_list):
    year_list = []
    pdfcounter = 0
    x = 0

    while x < len(pdf_list):
        years = pdf_list[x][-14:-10]
        year_list.append(years)
        x += 1

    pdfcounter = 0
    while pdfcounter < len(pdf_list):
        for year_listItem in year_list:
            if year_listItem in pdf_list[pdfcounter]:
                Path(year_listItem).mkdir(parents=True, exist_ok=True)
                shutil.move(pdf_list[pdfcounter], year_listItem)
                pdfcounter += 1

            else:
                sys.exit("Error°")

        pdfcounter += 1

# === Main ===


pdf_item_list = file_end_with_pdf("", "pdf")
comdirect_tags_macos(pdf_item_list)
set_create_date(pdf_item_list, annual_tax_certificate)
pdf_item_list = remove_with_no_Licensee(pdf_item_list, ignore_list)
year_list = generate_pdf_years(pdf_item_list)
date_list = return_date(pdf_item_list, date_list)

dic_pdf = dict(zip(pdf_item_list, date_list))
dic_pdf = dict(sorted(dic_pdf.items(), key=lambda item: item[1]))
pdf_list = list(dic_pdf.keys())
year_list = list(dic_pdf.values())
put_in_folder(pdf_list, year_list)
pdf_item_list = file_end_with_pdf("", "pdf")
put_rest_pdf_to_folder(pdf_item_list)

print("Done!")
