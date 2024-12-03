import json
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

import time
from dotenv import find_dotenv, load_dotenv
import argparse
from argparse import Namespace

from process_document import extract_json, extract_markdown
load_dotenv(find_dotenv())

def get_perfil(file_path):
    # Obtiene el nombre del puesto del documento con el Perfil solicitado
    text, _, images = extract_markdown(file_path=file_path)

    json_perfil = extract_json(content=text)

    return json_perfil

def main(args):
    # json_perfil = get_perfil("docs/Perfil de Analista de Producción[1].pdf")
    json_perfil = get_perfil(args.perfil_doc)
    opciones = webdriver.ChromeOptions()

    opciones.add_experimental_option("excludeSwitches",['enable-automation'])
    prefs = {"credentials_enable_service": False,"profile.password_manager_enabled": False}
    opciones.add_experimental_option("prefs", prefs)
    opciones.add_argument("user-data-dir=C:\\Users\\\ytamayo\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3")

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=opciones)

    driver.maximize_window()
    wait = WebDriverWait(driver, 60)

    # Go to the Recruiter LinkedIn Login Page
    driver.get('https://www.linkedin.com/uas/login-cap?session_redirect=https%3A%2F%2Fwww.linkedin.com%2Ftalent%2Fhome&source_app=tsweb&trk=tsweb_signin')

    wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="app__container"]/main/div[2]/form/div[3]/button')))

    # Login
    username = driver.find_element(By.XPATH, '//*[@id="username"]')
    username.clear()
    username.send_keys("yhairt@hotmail.com")
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("dni29562275")
    driver.find_element(By.XPATH, '//*[@id="app__container"]/main/div[2]/form/div[3]/button').click()
    time.sleep(3)

    # Begin a Search for talent
    advanced_filters = driver.find_element(By.XPATH, '//*[@id="application-wrapper"]/div[5]/div/div/header/div[2]/ul/li[1]')
    wait.until(lambda d : advanced_filters.is_displayed())
    advanced_filters.click()
    time.sleep(5)

    # search_params = driver.find_elements(By.CSS_SELECTOR, 'section.facets-container>div>div>div>div>div>section.search-facet>button.facet-edit-button')
    # job_title = [p for p in search_params if p.text.startwith("Job title")][0]
    job_title = driver.find_elements(By.XPATH, 'html//body/div[4]/div[5]/div/div/div[5]/div[1]/section[3]/div/main/div/section/div[1]/div[1]/div/div/div/section/button')
    wait.until(lambda d : job_title[0].is_displayed())
    job_title[0].click()

    job_title_input = driver.find_element(By.XPATH, 'html//body/div[4]/div[5]/div/div/div[5]/div[1]/section[3]/div/main/div/section/div[1]/div[1]/div/div/div/section/form/div[1]/div[1]/div[1]/div/input')
    job_title_input.clear()
    job_title_input.send_keys(json_perfil['Perfil'])
    job_title_input.send_keys(Keys.ARROW_DOWN)
    first_option =wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "ul.typeahead-results li")))
    first_option.send_keys(Keys.RETURN)

    search = driver.find_element(By.XPATH, '//*[@id="search-wrapper"]/section[3]/header/div/button[2]')
    wait.until(lambda d : search.is_displayed())
    search.click()

    time.sleep(20)
    driver.quit()

def parse_opt():
    parser = argparse.ArgumentParser(description='Image Yolo Dataset Generator for TASA Fase 2 Project.')
    parser.add_argument('--perfil_doc', dest='perfil_doc', action='store', 
                        default="", 
                        help='PDF file, containing information about profile to search', required=True)
    return parser
    
if __name__ == "__main__":
    parser = parse_opt()
    args = parser.parse_args()
    if isinstance(args, Namespace):
        main(args)
    else:
        print("Error no se ha enviado ningún parámetro")