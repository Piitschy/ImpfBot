import os
from importlib import import_module

req_file='requirements.txt'

with open(req_file) as r:
  req= [row.replace('\n','') for row in r.readlines()]

for r in req:
  try:
    import_module(r)
  except ImportError:
    print("\nTrying to Install required module: "+r+"\n")
    os.system('python -m pip install '+r)

print('\nAlle Module installiert')