import json
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import json_repair
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import time
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv
import argparse
from argparse import Namespace
from bs4 import BeautifulSoup
import pandas as pd

from process_document import extract_json, extract_markdown
load_dotenv(find_dotenv())

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[TimedRotatingFileHandler('logs/log.log', when="D", backupCount=10,)],
                    datefmt='%Y-%m-%dT%H:%M:%S')
logger = logging.getLogger(__name__)
logging.getLogger("seleniumwire.server").setLevel(level=logging.WARNING)
logging.getLogger("seleniumwire.handler").setLevel(level=logging.WARNING)
logging.getLogger("hpack.hpack").setLevel(level=logging.WARNING)

def __extract_json_from_response(response: str):
    json = response[response.index("```json"):-3]
    return json_repair.loads(json)

def get_perfil(file_path):
    # Obtiene el nombre del puesto del documento con el Perfil solicitado
    text, _, images = extract_markdown(file_path=file_path)

    json_perfil = extract_json(content=text)

    return __extract_json_from_response(json_perfil)


def save_results(file_path, notifications, id_name_part):   
    os.makedirs(file_path, exist_ok=True)
    # with open(f'{file_path}/perfiles_{id_name_part}_{datetime.now().strftime("%Y.%m.%d_%H.%M.%S")}.json', 'w') as json_file:
    #     json.dump(notifications, json_file, indent=4)

    df = pd.DataFrame(notifications)
    df.to_excel(f"{file_path}/perfiles_{id_name_part}_{datetime.now().strftime('%Y.%m.%d_%H.%M.%S')}.xlsx")

def main(args):
    # json_perfil = get_perfil("docs/Perfil de Analista de Producción[1].pdf")
    json_perfil = get_perfil(args.perfil_doc)
    logger.info("Finished process of Perfil document")

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
    time.sleep(8)

    # Begin a Search for talent
    advanced_filters = driver.find_element(By.XPATH, '//*[@id="application-wrapper"]/div[5]/div/div/header/div[2]/ul/li[1]')
    wait.until(lambda d : advanced_filters.is_displayed())
    advanced_filters.click()
    time.sleep(5)
    logger.info("time.sleep(5)")

    # search_params = driver.find_elements(By.CSS_SELECTOR, 'section.facets-container>div>div>div>div>div>section.search-facet>button.facet-edit-button')
    # job_title = [p for p in search_params if p.text.startwith("Job title")][0]
    job_title = driver.find_elements(By.XPATH, 'html//body/div[4]/div[5]/div/div/div[5]/div[1]/section[3]/div/main/div/section/div[1]/div[1]/div/div/div/section/button')
    wait.until(lambda d : job_title[0].is_displayed())
    job_title[0].click()

    job_title_input = driver.find_element(By.XPATH, 'html//body/div[4]/div[5]/div/div/div[5]/div[1]/section[3]/div/main/div/section/div[1]/div[1]/div/div/div/section/form/div[1]/div[1]/div[1]/div/input')
    job_title_input.clear()
    job_title_input.send_keys(json_perfil['Perfil'])
    job_title_input.send_keys(Keys.ARROW_DOWN)
    job_title_list_items = wait.until(ec.visibility_of_any_elements_located((By.CSS_SELECTOR, "ul[aria-label='Typeahead results'][role='listbox'].typeahead-results li")))
    first_option = job_title_list_items[0]
    job_title_input.send_keys(Keys.RETURN)

    logger.info("Before click search button")
    search = driver.find_element(By.XPATH, '//*[@id="search-wrapper"]/section[3]/header/div/button[2]')
    wait.until(lambda d : search.is_displayed())
    search.click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    pages_index = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "ol.pagination__list")))
    wait.until(lambda d : pages_index.is_displayed())
    time.sleep(20)

    logger.info("Before process of the search results")
    # Scrap the results
    search_result = wait.until(ec.visibility_of_all_elements_located((By.XPATH, '//*[@id="results-container"]/span/div/form/ol/li')))
    items = []
    for item in search_result:
        logger.debug(item.get_attribute("outerHTML"))
        try:
            soup = BeautifulSoup(item.find_element(By.CSS_SELECTOR, "div.row__card").get_attribute("outerHTML"), 'html.parser')

            result_item_info = {
                "Nombre": soup.find("img").attrs['aria-label'],
                "Fotografia": soup.find("img").attrs['src'],
                "Url_Perfil": soup.find("a").attrs['href'],
                "Puesto": soup.find("div", class_="artdeco-entity-lockup__subtitle ember-view").find("span").text.strip(),
                "Ubicacion": soup.find("div", class_="artdeco-entity-lockup__subtitle ember-view").find_next_sibling().find_next("div").select("div:nth-of-type(1)")[0].text.strip(),
                "Sector": soup.find("div", class_="artdeco-entity-lockup__subtitle ember-view").find_next_sibling().find_next("span").text.strip(),
                "Experiencia": "\n".join([item.text.strip() for item in soup.find("div", class_="history").find_all("ol")[0].find_all("li")]),
                "Educacion": "\n".join([p.text for p in soup.find("div", class_="history").find_all("ol")[1].find_all("li")])
            }
            items.append(result_item_info)
        except Exception as ex:
            logger.error(ex)    

    logger.info("Before saving the results")
    save_results('./results', items, json_perfil['Perfil'])
    time.sleep(20)
    driver.quit()
    logger.info("Finish process")

def parse_opt():
    parser = argparse.ArgumentParser(description='Image Yolo Dataset Generator for TASA Fase 2 Project.')
    parser.add_argument('--perfil_doc', dest='perfil_doc', action='store', 
                        default="", 
                        help='PDF file, containing information about profile to search', required=True)
    return parser
    
if __name__ == "__main__":
    parser = parse_opt()
    args = parser.parse_args()
    logger.info(f"Args: {args}")
    if isinstance(args, Namespace):
        main(args)
    else:
        print("Error no se ha enviado ningún parámetro")