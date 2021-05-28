from time import sleep
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Manager, Process


class Storage:
  path='./storage.json'
  def __init__(self):
    with open(self.path,'w') as storage:
      storage.write('')

  def __call__(self) -> dict:
    with open(self.path) as storage:
      return dict(json.loads(storage.read()))

  def read(self):
    with open(self.path) as storage:
      return dict(json.loads(storage.read()))

  def load(self, key):
    s=self.read()
    if key in s:
      return s[key]
    return None

  def save(self,data:dict):
    s=self.read()
    s.update(data)
    with open(self.path,'w') as storage:
      storage.write(json.dumps(s))
    return s



class ImpfBot:
  driver_path= {
    'Linux': './chromedriver_linux',
    'Darwin': './chromedriver_linux',
    'Windows': './chromedriver.exe',
  }
  def __init__(self,os) -> None:
    self.driver = webdriver.Chrome(self.driver_path[os])
    self.vars = {}
  
  def teardown(self):
    self.driver.quit()
  
  def check(self):
    try:
      self.driver.find_element(By.XPATH, "/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[1]/div/div[1]/div[5][contains(.,\'Keine Termine verfügbar\')]")
      return False
    except:
      return True

  def refresh(self):
    self.driver.find_element(By.XPATH, "//span[contains(.,\'Suchen\')]").click()

  def anmeldung(self,geb:str,plz:str,t:int=0.3):
    s = lambda: sleep(t)
    self.driver.get("https://www.impfportal-niedersachsen.de/portal/")
    input('Schau mal, ob da ein recaptcha ist.\nEnter, wenns losgehen kann...')
    self.driver.find_element(By.CSS_SELECTOR, ".mat-checkbox-inner-container-no-side-margin").click()
    s()
    element = self.driver.find_element(By.XPATH, "//button[contains(.,\'Weiter\')]")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    s()
    self.driver.find_element(By.XPATH, "//button[contains(.,\'Weiter\')]").click()
    s()
    element = self.driver.find_element(By.CSS_SELECTOR, ".cdk-focused > .mat-button-wrapper")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    s()
    self.driver.find_element(By.CSS_SELECTOR, ".cdk-focused > .mat-button-wrapper").click()
    s()
    self.driver.find_element(By.ID, "mat-input-2").click()
    s()
    self.driver.find_element(By.ID, "mat-input-2").send_keys(geb)
    s()
    self.driver.find_element(By.XPATH, "//span[contains(.,\'Weiter\')]").click()
    s()
    self.driver.find_element(By.XPATH, '//*[@id="mat-radio-2"]/label/span[1]').click()
    s()
    self.driver.find_element(By.XPATH, "//span[contains(.,\'Verstanden\')]").click()
    s()
    self.driver.find_element(By.XPATH, "//span[contains(.,\'Weiter\')]").click()
    s()
    self.driver.find_element(By.CSS_SELECTOR, ".cdk-focused > .mat-button-wrapper").click()
    s()
    self.driver.find_element(By.ID, "mat-input-0").click()
    s()
    self.driver.find_element(By.ID, "mat-input-0").send_keys(plz)
  
class MultiProc:
    def __init__(self,processes:list=[]) -> None:
        """
        Give me a list with prozesses or prozess objects in this format:

        [
            function1, 

            {
                'id': ' ',
                'func': function2,
                'args': [...],
                'kwargs': {...}
            },
            ...
        ]
        """
        self.manager = Manager()
        self.return_dict = self.manager.dict()
        self.jobs=[]
        self.procs=[]
        self.i=0
        self.append_processes(processes)
        return
    
    def append_processes(self,processes:list):
        """
        Give me a list with prozesses or prozess objects in this format:

        [
            function1, 

            {
                'id': ' ',
                'func': function2,
                'args': [...],
                'kwargs': {...}
            },
            ...
        ]
        """
        if type(processes) is not list:
            processes = [processes]
        for proc in processes:
            if type(proc) != dict:
                proc = {'func':proc}
            if 'id' not in proc or not proc['id']:
                proc.update({'id':self.i})
            if 'args' not in proc:
                proc.update({'args':[]})
            if 'kwargs' not in proc or not proc['kwargs']:
                proc.update({'kwargs':{}})
            self.procs.append(proc)
            self.i+=1

    def add_process(self,function,*args,**kwargs):
        """
        function: function or {'id' : function}
        *args and **kwargs will be bypassed to the function
        """
        id = None
        if type(function) is dict:
            (id, function) = list(function.items())[0]
        p = {
            'id': id,
            'func': function,
            'args': args,
            'kwargs': kwargs
        }
        self.append_processes([p])

    def _worker(self,id,proc,*args,**kwargs):
        self.return_dict.update({id:proc(*args,**kwargs)})
        return
    
    def start(self) -> None:
        for proc in self.procs:
            p = Process(target=self._worker,args=(proc['id'],proc['func'],*proc['args'], ),kwargs=proc['kwargs'])
            self.jobs.append(p)
            p.start()
        return
    
    def join(self) -> list:
        for p in self.jobs:
            p.join()
        return dict(self.return_dict)

    def execute(self) -> list:
        self.start()
        return self.join()