# ImpfBot

[![Python](https://img.shields.io/badge/Made%20with-Python%203.9-blue.svg?logo=Python&logoColor=yellow)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-orange.svg?logo=GNU&logoColor=orange)](https://www.gnu.org/licenses/gpl-3.0)

## _Grabb' dir einen Termin_

Dieser Bot regelt für dich...

:arrow_forward: Nur für Leute aus Gruppe 3 _( Rest folgt )_

> :warning: **Bitte missbrau' dieses Tool nicht**: Der Grundgedanke ist es, eine faire Möglichkeit für alle zu schaffen, die an spontane Impftermine kommen wollen. Du sollst eine Chance gegen andere (kommerzielle) Bot-Nutzer haben. Benutz dieses Tool bitte nur für deinen eigenen Termin.

## Installation
Geht nur mit installiertem Browser [Chrome v91](https://www.google.com/intl/de_de/chrome/) und in Niedersachsen...

- Lad' dir erstmal [Python](https://www.python.org/downloads/).
- Installiere Python
  - Windows: Achte darauf, dass du 'add Path' aktivierst und pip mitinstallierst!!!
  - Linux/Mac: Installiere Python und installiere dann pip mit:
    ```bash
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    
    python3 get-pip.py
    ```
- Lad' dir den [Bums hier](https://github.com/Piitschy/ibot/archive/refs/heads/main.zip) runter und entpacke ihn.

- Installier' die Requirements:
  - Windows: doppelklicke auf ```setup.py```
    >:exclamation: Wenn das nicht geht, öffne nochmal den Python installer und 'modifiziere' die Installation nochmal - also 'add path' und soo...
  - Mac: Rechtklick ```setup.py``` > Öffnen mit > Python Launcher.app
  
  - ODER für alle: öffne das Verzeichnis in CMD/PowerShell* oder im Terminal* gib' das hier ein:
      ```bash
      python3 setup.py
      ```
    >Wenn das nicht, klappt öffne das Verzeichnis in CMD/PowerShell* oder im Terminal* gib' das hier ein:
    ```bash
    python3 -m pip3 install -r requirements.txt
    ```
- Starte den Bot: 
  - Windows: doppelklicke auf ```run.py```
  - Mac: Rechtklick ```run.py``` > Öffnen mit > Python Launcher.app
    > :exclamation: Mac-Nutzer müssen ```chromedriver_darwin``` nach dem ersten Start unter ```Einstellungen > Sicherheit``` das Starten erlauben!
  
  - ODER für alle: öffne das Verzeichnis in CMD/PowerShell* oder im Terminal* gib' das hier ein:
      ```bash
      python3 run.py
      ```

*Geh' auf den frisch entpackten Ordner und öffne ihn in der CMD/PowerShell oder im Terminal. _( shift+rechtklick auf den ibot-Ordner - 'in CMD/Terminal/PowerShell öffnen' )_

## upcoming features
- Auto-SMS-Service
- Auto-Capture