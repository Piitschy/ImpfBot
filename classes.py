from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class ImpfBot():
  def setup(self):
    self.driver = webdriver.Chrome('./chromedriver')
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
  
