from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import smtplib
import gspread
import requests

chrome_options = Options() #creamos un objeto de la clase Options para ajustar la configuracion del driver


#chrome_options.add_argument("--headless")
#chrome_options.headless = True
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument('--ignore-certificate-errors')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=chrome_options)

def telegram_bot_sendtext(bot_message):
    bot_token = 'xxxxxxxxxxxxxx'
    bot_chatID = 'xxxxxxxxxxxxx'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)#peticion get con la concatenacion de la uri:url,token,id, y el mensaje que recibe como parametro

    return response.json()


start_url = ""

driver.get(start_url)#ejecucion la url de inicio declarada



time.sleep(5)



ofertas = False

while not ofertas: #bucle infinito

    gc = gspread.service_account(filename='stocksheet-xxxxxxxxxxxx.json') #ruta de las credenciales del usuario para consumir API GsPread
    sh = gc.open('StockSheet').sheet1 #selector de hoja

    print("----------------------------------------------------------------------------REFRESH----------------------------------------------------------------------------")


    sh.clear()

    Producto = "Producto"
    Precio = "Precio"
    Disponibilidad = "Disponibilidad"
    Enlace = "Enlace"
    PrecioD = "Precio Deseado"
    FotoP = "Foto"

    sh.append_row([Producto, Precio, Disponibilidad,Enlace, PrecioD, FotoP])#post de columnas creadas a la hoja


    driver.refresh()


    elements = driver.find_elements_by_xpath("//div[@class='xxxxxxxxxx']//a") #obtencion de los elementos hijos con etiqueta <a> de la etiqueta padre <div>



    for element in elements: #iteracion sobre los elementos

        time.sleep(1)

        href = element.get_attribute('href') #de cada etiqueta <a> obtencion del valor de <href>

        print(href)

        driver.execute_script("window.open('" + href + "');") #ejecucion en nueva pestaña de cada href

        driver.switch_to.window(driver.window_handles[1])

        try:

            time.sleep(1)

            addToCartButtonDisabled =  driver.find_element_by_class_name("disabled")

            print("No hay boton de compra")

            driver.close()

            driver.switch_to.window(driver.window_handles[0])

        except:

            AddtoCartEnabled = driver.find_element_by_class_name("buy-button")

            Precios = driver.find_element_by_xpath(
                "/html/body/div[4]/div[2]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]").get_attribute("data-price")

            Precios = float(Precios)

            PrecioDeseado = (500)

            titulo = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[3]/div/div/div[1]/h1/strong")

            Foto = driver.find_element_by_xpath(
                "/html/body/div[4]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div/a/img").get_attribute("src")

            DisponibilidadStock = "✅Disponible✅"


            if Precios <= PrecioDeseado:

                print("Precio deseado:", Precios, "------>", href)

                tg = telegram_bot_sendtext("ALERTA STOCK: " + href) #llamada a la función donde se hace la peticion http a telegram api

                mensaje = ("PRODUCTO EN OFERTA  ➡️" + href)

                asunto = 'STOCK A PRECIO OBJETIVO'

                mensaje = 'Subject: {}\n\n{}'.format(asunto, mensaje)

                server = smtplib.SMTP('smtp.gmail.com',587)#conexion al modulo smtplib para enviar e-mail con la notificacion
                server.starttls()
                server.login('xxxxx', 'xxxxx')#credenciales

                server.sendmail('xxxxxxx@gmail.com', 'xxxxx1@gmail.com', mensaje.encode('utf-8'))#destinatarios y formato

                server.quit()

                PrecioSiDeseado = "✔💲"

                sh.append_row([titulo, Precios, DisponibilidadStock, href, PrecioSiDeseado, Foto])#post a la hoja

                time.sleep(3)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])


            else:

                now = datetime.now()

                current_time = now.strftime("%H:%M:%S")

                print("Precio no deseado:", Precios, "---->", current_time)

                PrecioNoDeseado = "❌💲"

                sh.append_row([titulo, Precios, DisponibilidadStock, href, PrecioNoDeseado, Foto])

                time.sleep(3)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])







