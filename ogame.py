from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep    
from Attack import Attack
from datetime import datetime

def wait_and_click(locator):
    WebDriverWait(driver, 2000).until(EC.presence_of_element_located((By.XPATH, locator)))
    iniciar_sesion_tab = driver.find_element_by_xpath(locator)
    iniciar_sesion_tab.click()

iniciar_sesion_tab_locator = "//*[@id='loginRegisterTabs']/ul/li[1]/span"
jugado_por_ultima_vez_button_locator = "//*[@id='joinGame']/button/span[1]"
flota_button_locator = "//*[@id='menuTable']/li[8]/a/span"
cantidad_pcarga_locator = "//*[@id='civil']/li[1]/span/span/span[1]"
galaxy_input_locator = "//*[@id='galaxy']"
system_input_locator = "//*[@id='system']"
position_input_locator = "//*[@id='position']"
aceptar_cookies_button_locator = "/html/body/div[4]/div/div/span[2]/button[2]"


#-------------------------- SETUP AND LOGIN STAGE

driver = webdriver.Chrome()
driver.get("https://lobby.ogame.gameforge.com/es_AR/?language=ar")
main_window = driver.current_window_handle
sleep(2)
driver.find_element_by_xpath(aceptar_cookies_button_locator).click()
wait_and_click(iniciar_sesion_tab_locator)
driver.find_element_by_name("email").send_keys("your_email")
sleep(1)
driver.find_element_by_name("password").send_keys("your_password")
sleep(1)
driver.find_element_by_xpath("//*[@id='loginForm']/p/button[1]/span").click()
sleep(3)
driver.get("https://s135-ar.ogame.gameforge.com/game/index.php?page=ingame&component=overview&relogin=1")
sleep(3)
wait_and_click(jugado_por_ultima_vez_button_locator)
driver.switch_to.window(main_window)
sleep(2)


#------------CONFIGURATION


attacks = [
           #Expediciones
           Attack("33684507", "2:384:16", datetime(2021, 6, 2), "expedition", "9999", "9999"), # Uruguay
           Attack("33684545", "2:385:16", datetime(2021, 6, 2), "expedition", "9999", "9999"), # Madara
           Attack("33684546", "2:383:16", datetime(2021, 6, 2), "expedition", "9999", "9999"), # Itachi

           #Ataques
           Attack("33684549", "1:327:7", datetime(2021, 6, 2), "attack", "150", "0", "0", "0"), # Sakura -> Kr3 [1:327:7]
           Attack("33684549", "2:136:11", datetime(2021, 6, 2), "attack", "150", "0", "0", "0"), # Sakura -> Pomelo [2:136:11]
           Attack("33684566", "1:21:8", datetime(2021, 6, 2), "attack", "250", "0", "0", "0"), # Kiba -> Banana [1:21:8]
           Attack("33684566", "1:327:9", datetime(2021, 6, 2), "attack", "250", "0", "0", "0"), # Kiba -> Kr2 [1:327:9]
           Attack("33684722", "2:148:9", datetime(2021, 6, 2), "attack", "200", "0", "0", "0"), # Obito -> Mandarina [2:148:9]
           Attack("33684722", "4:145:8", datetime(2021, 6, 2), "attack", "200", "0", "0", "0"), # Obito -> Sandia [4:145:8]
           Attack("33684797", "2:125:8", datetime(2021, 6, 2), "attack", "150", "0", "0", "0"), # Deidara -> Mango [2:125:8]
           Attack("33684797", "2:131:12", datetime(2021, 6, 2), "attack", "150", "0", "0", "0"), # Deidara -> Limon [2:131:12]
           ]

#------------BUCLE

while 1==1:
    now = datetime.now()
    print("-------------CONTROL BOARD----------------  CONTROL TIME : " +str(now))
    for attack in attacks:
        print("Origin : " + attack.origin + "       Target : " + attack.target + "       Time : " + str(attack.time) + "       pcarga : " + attack.pcarga)
        
        if now > attack.time:
            driver.get("https://s135-ar.ogame.gameforge.com/game/index.php?page=ingame&component=overview")
            sleep(3)
            driver.get("https://s135-ar.ogame.gameforge.com/game/index.php?page=ingame&component=fleetdispatch&cp=" + attack.origin)

            try:
                sleep(3)
                cantidad_pcarga = driver.find_element_by_xpath(cantidad_pcarga_locator).get_attribute('innerText')
            except:
                sleep(3)
                wait_and_click(jugado_por_ultima_vez_button_locator)
                driver.switch_to.window(main_window)
                sleep(2)
                driver.get("https://s135-ar.ogame.gameforge.com/game/index.php?page=ingame&component=fleetdispatch&cp=" + attack.origin)
                sleep(3)
                cantidad_pcarga = driver.find_element_by_xpath(cantidad_pcarga_locator).get_attribute('innerText')

            if attack.method == "attack":
                if int(cantidad_pcarga) >= int(attack.pcarga):
                    sleep(1)
                    driver.find_element_by_xpath("//*[@id='civil']/li[1]/input").send_keys(attack.pcarga)
                    sleep(1)
                    driver.execute_script("window.scrollTo(0, 1080)")

                    driver.find_element_by_xpath("//*[@id='continueToFleet2']/span").click()

                    galaxy = attack.target.split(":")[0]
                    system = attack.target.split(":")[1]
                    position = attack.target.split(":")[2]

                    sleep(1)
                    driver.find_element_by_xpath(galaxy_input_locator).send_keys(galaxy)
                    driver.find_element_by_xpath(system_input_locator).send_keys(system)
                    driver.find_element_by_xpath(position_input_locator).send_keys(position)
                    driver.find_element_by_xpath(position_input_locator).send_keys(Keys.ENTER)

                    # Apretar en selección de misión, ataque
                    sleep(2)
                    wait_and_click("//*[@id='missionButton1']")

                    sleep(2)
                    returnTime = driver.find_element_by_xpath("//*[@id='returnTime']").get_attribute('innerText')

                    fecha = returnTime.split(" ")[0]
                    horario = returnTime.split(" ")[1]

                    dia = int(fecha.split(".")[1])
                    mes = int(fecha.split(".")[0])
                    ano = int("20" + fecha.split(".")[2])

                    hora = int(horario.split(":")[0])
                    minuto = int(horario.split(":")[1])
                    segundo = int(horario.split(":")[2])

                    attack.time = datetime(ano, dia, mes, hora, minuto, segundo)

                    # Apretar Atacar
                    sleep(2)
                    driver.find_element_by_xpath("//*[@id='deuterium']").send_keys(Keys.ENTER)
                    print("ATAQUE EJECUTADO, regreso planificado: " + returnTime)

            if attack.method == "expedition":
                sleep(1)
                driver.find_element_by_xpath("//*[@id='military']/li[3]/input").send_keys(attack.crucero)
                driver.find_element_by_xpath("//*[@id='civil']/li[1]/input").send_keys(attack.pcarga)
                driver.find_element_by_xpath("//*[@id='civil']/li[2]/input").send_keys(attack.gcarga)
                driver.find_element_by_xpath("//*[@id='civil']/li[5]/input").send_keys(attack.sondaespionaje)
                driver.find_element_by_xpath("//*[@id='military']/li[10]/input").send_keys("1")
                sleep(1)
                driver.execute_script("window.scrollTo(0, 1080)")

                driver.find_element_by_xpath("//*[@id='continueToFleet2']/span").click()

                galaxy = attack.target.split(":")[0]
                system = attack.target.split(":")[1]
                position = attack.target.split(":")[2]

                sleep(1)
                driver.find_element_by_xpath(galaxy_input_locator).send_keys(galaxy)
                driver.find_element_by_xpath(system_input_locator).send_keys(system)
                driver.find_element_by_xpath(position_input_locator).send_keys(position)
                driver.find_element_by_xpath(position_input_locator).send_keys(Keys.ENTER)

                # Apretar en selección de misión, ataque
                sleep(2)
                wait_and_click("//*[@id='missionButton15']")

                sleep(2)
                returnTime = driver.find_element_by_xpath("//*[@id='returnTime']").get_attribute('innerText')

                fecha = returnTime.split(" ")[0]
                horario = returnTime.split(" ")[1]

                dia = int(fecha.split(".")[1])
                mes = int(fecha.split(".")[0])
                ano = int("20" + fecha.split(".")[2])

                hora = int(horario.split(":")[0])
                minuto = int(horario.split(":")[1])
                segundo = int(horario.split(":")[2])

                attack.time = datetime(ano, dia, mes, hora, minuto, segundo)

                # Enviar Flota
                sleep(2)
                driver.find_element_by_xpath("//*[@id='deuterium']").send_keys(Keys.ENTER)
                print("EXPEDICION EJECUTADA regreso planificado: " + returnTime)

    print("-------------------------------------------------------------")
    sleep(300)
