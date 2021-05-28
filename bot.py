from classes import *
import utils
from datetime import datetime
from time import sleep
import random
import re
import platform
from flask import Flask, request, render_template
import os
import webbrowser

R_DATE=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$'
R_PLZ=r'^[0-9]{5}$'

system = platform.system()
store = Storage()
app = Flask(__name__)
start = False
clear = lambda: os.system(utils.clear_str[system])
rand = lambda: 5+random.randint(1, 10)/5

@app.route('/',methods=['GET','POST'])
def index():
  if request.method == 'POST':
    for k in utils.user_data:
      store.save(k,request.form[k])
  return render_template("index.html", **store.state )
  
@app.route('/code/<code>',methods=["GET"])
def getCode(code):
  start = True
  store.save('sms',code)
  return 'nice'

def eingabe(text, regex):
  e = input(text)
  if re.match(regex,e):
    return e
  print('Ne, mach mal richtig...')
  eingabe(text, regex)

def ask_user_data():
  ud = utils.user_data
  for k,v in ud.items():
    if k not in store.state:
      e = eingabe(v['text'],v['rx'])
      store.save(k,e)
  return store()

def start_sms_service():
  pool = MultiProc()
  pool.add_process(app.run, host='0.0.0.0', port=5000, debug=False, threaded=True)
  pool.start()
  sleep(1)
  clear()
  return


if __name__ == "__main__":
  ui = input('Willst du ne UI? (y/n): ')
  if ui == 'y':
    start_sms_service()
    webbrowser.open('http://localhost:5000')
  else:
    clear()
    ask_user_data()
  input('Breit, wenn du es bist! \nDrücke einfach Enter und es geht los... ')

  session = ImpfBot(system)
  session.anmeldung(store('geb'),store('plz'))
  session.refresh()
  
  while True:
    sleep(rand())
    session.refresh()
    sleep(0.5)
    if session.check():
      break
    print(datetime.now().strftime("%H:%M:%S"),'keine Termine')

  print('JETZT IST WAS ANDERS!!!!!')
