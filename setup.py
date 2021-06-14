import os
from importlib import import_module
import platform
import zipfile
import requests as rq


req_file='requirements.txt'

with open(req_file) as r:
  req= [row.replace('\n','') for row in r.readlines()]

for r in req:
  try:
    import_module(r)
  except ImportError:
    print("\nTrying to Install required module: "+r+"\n")
    os.system('python -m pip3 install '+r)

if platform.system() == "Windows":
  try:
    re = rq.get("https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe")
    open('tessa.exe', 'wb').write(re.content)
    os.system("tessa.exe")
  except Exception as e:
    print("teseract Installation fehlgeschlagen. UPSI: "+e)



print('\nAlle Module installiert')