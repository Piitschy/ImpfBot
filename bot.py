from classes import *
from datetime import datetime
from time import sleep
import random
import re
import platform
from playsound import playsound
import os

clear_str = {
  'Linux': 'clear',
  'Darwin': 'clear',
  'Windows': 'cls',
}

system = platform.system()

rxDate=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$'
rxPLZ=r'^[0-9]{5}$'

rand = lambda: 5+random.randint(1, 10)/5
clear = lambda: os.system(clear_str[system])

def eingabe(text, regex):
  e = input(text)
  if re.match(regex,e):
    return e
  print('Ne, mach mal richtig...')
  eingabe(text, regex)

clear()
geb=eingabe('Geburtstag (dd.MM.yyyy): ',rxDate)
plz=eingabe('PLZ: ',rxPLZ)

session = ImpfBot(system)
session.anmeldung(geb,plz)
session.refresh()

while True:
  sleep(rand())
  session.refresh()
  sleep(0.5)
  if session.check():
    break
  print(datetime.now().strftime("%H:%M:%S"),'keine Termine')

while True:
  playsound('audio.mp3')
  print('JETZT IST WAS ANDERS!!!!!')
  sleep(2)

