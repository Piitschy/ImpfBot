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
import utils


class Storage:
  def __init__(self):
    try:
      self.state= self.read()
    except:
      self.state = self.clear()
  
  def __call__(self, key:str=None) -> dict:
    if key:
      return self.load(key)
    return self.refresh

  def refresh(self):
    self.state = self.read()
    return self.state

  def read(self):
    with open(utils.path) as storage:
      return dict(json.loads(storage.read()))

  def clear(self):
    with open(utils.path,'w') as storage:
        storage.write('{}')
    return self.refresh()

  def load(self, key:str, local:str=None):
    if key in self.state:
      if key == 'geb' and local == 'de':
        geb=self.state['geb']
        if '-' in geb:
          return str(geb[-2:]+'.'+geb[5:7]+'.'+geb[:4])
      return self.state[key]
    return None

  def save(self,key:str,value):
    s=self.read()
    data={key:value}
    s.update(data)
    with open(utils.path,'w') as storage:
      storage.write(json.dumps(s))
    self.refresh()
    return s

class ImpfBot:
  def __init__(self,system, url,t:int=0.3) -> None:
    self.driver = webdriver.Chrome(utils.driver_path[system])
    self.url = url
    self.vars = {}
    self.s = lambda: sleep(t)
  
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

  def anmeldung(self,store):
    self.driver.get(self.url)
    self.driver.find_element(By.CSS_SELECTOR, ".mat-checkbox-inner-container-no-side-margin").click()
    self.s()
    element = self.driver.find_element(By.XPATH, "//button[contains(.,\'Weiter\')]")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.s()
    self.driver.find_element(By.XPATH, "//button[contains(.,\'Weiter\')]").click()
    self.s()
    element = self.driver.find_element(By.CSS_SELECTOR, ".cdk-focused > .mat-button-wrapper")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, ".cdk-focused > .mat-button-wrapper").click()
    self.s()
    self.driver.find_element(By.ID, "mat-input-2").click()
    self.s()
    self.driver.find_element(By.ID, "mat-input-2").send_keys(store.load('geb',local='de'))
    self.s()
    self.driver.find_element(By.XPATH, "//span[contains(.,\'Weiter\')]").click()
    self.s()
    self.driver.find_element(By.ID, "mat-input-0").click()
    self.s()
    self.driver.find_element(By.ID, "mat-input-0").send_keys(store('plz'))

  def form(self, store):
    self.driver.find_element(By.CSS_SELECTOR, ".ng-tns-c108-12:nth-child(2)").click()
    sleep(1)
    self.driver.find_element(By.XPATH, "//span[contains(.,\'Divers\')]").click()
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, "#mat-input-8").click()
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, "#mat-input-8").send_keys(store('firstname'))
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, "#mat-input-9").click()
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, "#mat-input-9").send_keys(store('lastname'))
    self.s()
    self.driver.find_element(By.XPATH, "//div[3]/div/autocomplete/div[2]/mat-form-field/div/div/div/input").click()
    self.s()
    self.driver.find_element(By.XPATH, "//div[3]/div/autocomplete/div[2]/mat-form-field/div/div/div/input").send_keys(store('str'))
    sleep(1)
    self.driver.find_element(By.XPATH, "//mat-option").click()
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, "#mat-input-11").click()
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, "#mat-input-11").send_keys(store('hausnr'))
    self.s()
    #self.driver.find_element(By.CSS_SELECTOR, "#mat-input-12").click()
    #self.s()
    #self.driver.find_element(By.CSS_SELECTOR, "#mat-input-12").send_keys("zusatz")
    self.driver.find_element(By.CSS_SELECTOR, "#mat-checkbox-2 .mat-checkbox-inner-container").click()
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, "#mat-input-15").click()
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, "#mat-input-15").send_keys(store('mail'))
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, "#mat-input-19").click()
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, "#mat-input-19").send_keys(store('mail'))
    self.s()
    self.driver.find_element(By.CSS_SELECTOR, ".maxfill:nth-child(1) > .maxfill > div").click()