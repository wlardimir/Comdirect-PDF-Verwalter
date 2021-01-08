import os
#import macos_tags
import sys
import shutil
import time
import datetime
from PyPDF2 import PdfFileReader
from os import path
from glob import glob
from pathlib import Path
from PyPDF2 import PdfFileReader

#=== Vars ===

comdirect = "Comdirect"
listignore = ["Finanzreport", "Kosteninformation"]
jahressteuerbescheinigung = ["Jahressteuerbescheinigung"]

listyears = []
listofyears = []

#=== Defs ===

def file_end_with_pdf(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))

def set_create_date(listpdf, listignore):
    listpdf = [pdfItem for pdfItem in listpdf if not any(ignoreItem in pdfItem for ignoreItem in listignore)]
    pdfcounter = 0

    while pdfcounter < len(listpdf):
        day = int(listpdf[pdfcounter][-20:-18])
        month = int(listpdf[pdfcounter][-17:-15])
        year = int(listpdf[pdfcounter][-14:-10])

        date = datetime.datetime(year=year, month=month, day=day)
        modTime = time.mktime(date.timetuple())

        os.utime(listpdf[pdfcounter], (modTime, modTime))

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

def generate_pdf_years(listpdf):
    listyear = []
    pdfcounter = 0

    while pdfcounter < len(listpdf):
        reader = PdfFileReader(listpdf[pdfcounter])
        metadata = reader.getDocumentInfo()
        licensee = metadata['/Licensee']

        if comdirect in licensee:
            #macos_tags.add(comdirect, file=listpdf[pdfcounter])
            years = listpdf[pdfcounter][-14:-10]
            listyear.append(years)
            listyear = remove_duplicates(listyear)

        pdfcounter += 1

    return listyear

def return_date(listpdf, listofyears):
    x = 0
    while x < len(listpdf):
        years = listpdf[x][-14:-10]
        listofyears.append(years)
        x += 1

    return listofyears

def put_in_folder(listpdf, listyear):
    pdfcounter = 0
    while pdfcounter < len(listpdf):
        for listYearItem in listyear:
            if listYearItem in listpdf[pdfcounter]:
                Path(listYearItem).mkdir(parents=True, exist_ok=True)
                shutil.move(listpdf[pdfcounter], listYearItem)
                pdfcounter += 1

            else:
                sys.exit("Error message")

        pdfcounter += 1

def put_rest_pdf_to_folder(listpdf):
    listyear = []
    pdfcounter = 0
    x = 0

    while x < len(listpdf):
        years = listpdf[x][-14:-10]
        listyear.append(years)
        x += 1

    pdfcounter = 0
    while pdfcounter < len(listpdf):
        for listYearItem in listyear:
            if listYearItem in listpdf[pdfcounter]:
                Path(listYearItem).mkdir(parents=True, exist_ok=True)
                shutil.move(listpdf[pdfcounter], listYearItem)
                pdfcounter += 1

            else:
                sys.exit("Error message")

        pdfcounter += 1

#=== Main ===

listofpdf = file_end_with_pdf("","pdf")
set_create_date(listofpdf, jahressteuerbescheinigung)
listofpdf = remove_with_no_Licensee(listofpdf, listignore)
listyear = generate_pdf_years(listofpdf)
listofyears = return_date(listofpdf, listofyears)

dic_pdf = dict(zip(listofpdf, listofyears))
dic_pdf = dict(sorted(dic_pdf.items(), key=lambda item: item[1]))
listpdf = list(dic_pdf.keys())
listyear = list(dic_pdf.values())
put_in_folder(listpdf, listyear)
listofpdf = file_end_with_pdf("","pdf")
put_rest_pdf_to_folder(listofpdf)

print("Done!")
