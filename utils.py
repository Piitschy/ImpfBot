R_TXT=r'^[A-ZÄÖÜ]{1}[a-zA-Z äöüÄÖÜß ]$'
R_NR=r'^[0-9]{1,4}[ ]{0,1}[a-zA-Z]'
R_DATE=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$'
R_PLZ=r'^[0-9]{5}$'
R_MAIL=r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
R_TEL=r'^[0-9]{6,16}'

path='./storage.json'

driver_path= {
  'Linux': './drivers/chromedriver_linux',
  'Darwin': './drivers/chromedriver_linux',
  'Windows': './drivers/chromedriver.exe',
}

clear_str = {
  'Linux': 'clear',
  'Darwin': 'clear',
  'Windows': 'cls',
}

user_data = {
  'geb': {
    'text': 'Geburtstag (dd.MM.yyyy): ',
    'rx': R_DATE
  },
  'plz': {
    'text': 'PLZ: ',
    'rx': R_PLZ
  },
  'lastname': {
    'text': 'Nachname: ',
    'rx': R_TXT
  },
  'firstname': {
    'text': 'Vorname: ',
    'rx': R_TXT
  },
  'tel': {
    'text': 'Telefonnummer: ',
    'rx': R_TEL
  },
  'mail': {
    'text': 'E-Mail: ',
    'rx': R_MAIL
  },
  'str':{
    'text': 'Straße: ',
    'rx': R_TXT
  },
  'hausnr':{
    'text': 'Hausnummer: ',
    'rx': R_NR
  }
}