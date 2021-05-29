from classes import *
import utils
from datetime import datetime
from time import sleep
import random
import re
import platform
from flask import Flask, request, render_template, redirect, url_for
import logging
import os
import webbrowser
import threading

system = platform.system()
store = Storage()
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
  store.save('sms',code)
  return 'nice'

@app.route('/start',methods=["GET"])
def start():
  threading.Thread(target=start_bot).start()
  return redirect(url_for('index'))

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

def start_flask():
  pool = MultiProc()
  pool.add_process(app.run, host='0.0.0.0', port=5000, debug=False, threaded=True)
  pool.start()
  sleep(1)
  clear()
  return

def start_bot():
  session = ImpfBot(system,"https://www.impfportal-niedersachsen.de/portal/")
  session.anmeldung(store.load('geb',local='de'),store('plz'))
  session.refresh()
  
  while True:
    sleep(rand())
    session.refresh()
    sleep(0.5)
    if session.check():
      break
    print(datetime.now().strftime("%H:%M:%S"),'keine Termine')

  print('JETZT IST WAS ANDERS!!!!!')

if __name__ == "__main__":
  print('Du kannst deine Daten jederzeit in storage.json ändern oder die Datei löschen, um sie zurückzusetzten.')
  ui = input('Möchtest du das Interface (BETA) starten? (y/n): ')
  if ui == 'y':
    #start_flask()
    threading.Thread(target=app.run).start()
    print('Starte Server...')
    sleep(1)
    clear()
    webbrowser.open('http://localhost:5000')
    print("...")
    sleep(5)
  clear()
  for k in utils.user_data:
    if k not in store.state:
      manuell = input('Willst du deine fehlenden Daten hier eingeben? (y/n): ')
      if manuell == 'y':
        clear()
        ask_user_data()
  clear()

  input('Breit, wenn du es bist! \nDrücke einfach Enter und es geht los... ')

  start_bot()
