from operator import truediv

from selenium.webdriver.ie.webdriver import WebDriver
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from data import card_number
import time

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    #Direccion
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    #Tarrifa
    book_a_taxi_button = (By.CSS_SELECTOR, '.button.round')
    select_comfort_rate = (By.XPATH, '//div[@class="tcard-title"][text()="Comfort"]')
    comfort_rate_selected = (By.CSS_SELECTOR, '.tcard.active')
    #Telefono
    phone_input_button = (By.CLASS_NAME, 'np-button')
    phone_input_field = (By.XPATH, '//*[@id="phone"]')
    phone_input_send = (By.XPATH, '//div[@class="buttons"]/button[text()="Siguiente"]')
    input_sms_code = (By.XPATH, '//input[@placeholder="xxxx"]')
    send_sms_code = (By.XPATH, '//*[@class="button full"][text()="Confirmar"]')
    #Metodo de pago
    payment_method_button = (By.CSS_SELECTOR, '.pp-text')
    add_card_button = (By.CSS_SELECTOR, '.pp-plus')
    add_card_field = (By.ID, 'number')
    card_code_field = (By.NAME, 'code')
    change_focus_click_card_field = (By.ID, 'number')
    send_card_info = (By.XPATH, '//*[@class="button full"][text()="Agregar"]')
    card_added_text = (By.XPATH, '//*[@class="pp-title"][text()="Tarjeta"]')
    close_add_payment_window = (By.XPATH, '//div[@class="payment-picker open"]/div[@class="modal"]/div[@class="section active"]/button')
    #Mensaje para conductor
    message_for_driver_field = (By.CSS_SELECTOR, '#comment')
    #Pedir manta/panuelo y helado
    slider_for_blanket_and_cloth  = (By.XPATH, '(//*[@class="slider round"])[1]')
    blanket_cloth_selected = (By.XPATH, '(//*[@type="checkbox"][@class="switch-input"])[1]')
    counter_add_for_icecream = (By.XPATH , '(//*[@class="counter-plus"])[1]')
    ice_cream_counter_value_2 = (By.XPATH, '//*[@class="counter-value"][text()="2"]')
    #Modal para buscar taxi
    request_taxi_button = (By.CSS_SELECTOR, '.smart-button-main')
    taxi_requested_window = (By.CLASS_NAME, 'order-header-title')


    def __init__(self, driver):
        self.driver = driver
#1 Configurar direccion
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

                 # Paso set_route
    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')
#2 Seleccionar tarifa comfort
    def click_book_a_taxi_button(self):
        self.driver.find_element(*self.book_a_taxi_button).click()

    def click_comfort_rate(self):
        self.driver.find_element(*self.select_comfort_rate).click()

    def check_comfort_rate_selected(self):
        return self.driver.find_element(*self.comfort_rate_selected).is_displayed()


                # Paso comfort_rate_request
    def comfort_rate_request(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.button.round')))
        self.click_book_a_taxi_button()
        self.click_comfort_rate()

#3 Rellenar el numero de telefono
    def click_phone_input_button(self):
        self.driver.find_element(*self.phone_input_button).click()

    def fill_phone_input_field(self, phone_number):
        self.driver.find_element(*self.phone_input_field).send_keys(phone_number)

    def submit_phone_number(self):
        self.driver.find_element(*self.phone_input_send).click()

    def get_phone_input_field(self):
        return self.driver.find_element(*self.phone_input_field).get_property('value')

    def fill_sms_field(self):
        self.driver.find_element(*self.input_sms_code).send_keys(retrieve_phone_code(self.driver))

    def confirm_sms_code(self):
        self.driver.find_element(*self.send_sms_code).click()


                # Paso send_phone_number
    def send_phone_number(self):
        self.click_phone_input_button()
        self.fill_phone_input_field(data.phone_number)
        self.submit_phone_number()
        self.fill_sms_field()
        self.confirm_sms_code()

#4 Agregar tarjeta de credito
    def click_payment_method_button(self):
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card_button(self):
        self.driver.find_element(*self.add_card_button).click()

    def fill_add_card_field(self):
        self.driver.find_element(*self.add_card_field).send_keys(data.card_number)

    def fill_card_code_field(self):
        self.driver.find_element(*self.card_code_field).send_keys(data.card_code)

    def change_card_code_focus(self):
        self.driver.find_element(*self.change_focus_click_card_field).click()

    def submit_card_info(self):
        self.driver.find_element(*self.send_card_info).click()

    def get_card_field(self):
        return self.driver.find_element(*self.add_card_field).get_property('value')

    def check_card_added_text(self):
        return self.driver.find_element(*self.card_added_text).is_displayed()

    def click_close_add_payment_window(self):
        self.driver.find_element(*self.close_add_payment_window).click()


                # Paso send_credit_card
    def send_credit_card(self):
        self.click_payment_method_button()
        self.click_add_card_button()
        self.fill_add_card_field()
        self.fill_card_code_field()
        self.change_card_code_focus()
        self.submit_card_info()




#5 Mensaje para conductor
    def fill_message_for_driver_field(self):
        self.driver.find_element(*self.message_for_driver_field).send_keys(data.message_for_driver)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.message_for_driver_field).get_property('value')

#6 Pedir manta y panuelo
    def select_cloth_and_blanket(self):
        self.driver.find_element(*self.slider_for_blanket_and_cloth).click()

    def check_cloth_and_blanket_is_selected(self):
         return self.driver.find_element(*self.blanket_cloth_selected).is_selected()


#7 Pedir 2 helados
    def select_add_ice_cream_button(self):
       self.driver.find_element(*self.counter_add_for_icecream).click()
       self.driver.find_element(*self.counter_add_for_icecream).click()

    def check_ice_cream_counter_value_2(self):
       return self.driver.find_element(*self.ice_cream_counter_value_2).is_displayed()


#8 Aparece modal para buscar taxi
    def click_request_taxi_button(self):
        self.driver.find_element(*self.book_a_taxi_button).click()

    def check_taxi_requested_window_visible(self):
        return self.driver.find_element(*self.taxi_requested_window).is_displayed()



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
#1
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.ID, 'to')))
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

#2
    def test_comfort_rate_request(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_set_route()
        routes_page.comfort_rate_request()
        assert routes_page.check_comfort_rate_selected() == True

#3
    def test_send_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_comfort_rate_request()
        routes_page.send_phone_number()
        assert routes_page.get_phone_input_field() == data.phone_number

#4
    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_send_phone_number()
        routes_page.send_credit_card()
        assert routes_page.get_card_field() == data.card_number
        assert routes_page.check_card_added_text() == True


#5
    def test_send_message_for_driver(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_add_credit_card()
        routes_page.click_close_add_payment_window()
        routes_page.fill_message_for_driver_field()
        assert  routes_page.get_message_for_driver() == data.message_for_driver

#6
    def test_request_blanket_and_cloth(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_send_message_for_driver()
        routes_page.select_cloth_and_blanket()
        assert routes_page.check_cloth_and_blanket_is_selected() == True

#7
    def test_request_2_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_request_blanket_and_cloth()
        routes_page.select_add_ice_cream_button()
        assert routes_page.check_ice_cream_counter_value_2() == True

#8
    def test_request_taxi_pop_up_window(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_request_2_ice_cream()
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '.smart-button-main')))
        routes_page.click_request_taxi_button()
        assert routes_page.check_taxi_requested_window_visible() == True




    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
