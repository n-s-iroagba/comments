import time
import random
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BotActions:
    def __init__(self, delay_range=(0.05, 0.1)):
        """
        Initialize BotActions with a delay range for typing.
        
        :param delay_range: Tuple (min, max) for random delays between keystrokes.
        """
        self.delay_range = delay_range

    def get_element(self, driver, by, value, multiple=False):
        """
        Find and return a web element or a list of elements.
        
        :param driver: Selenium WebDriver instance.
        :param by: Locator strategy (e.g., By.CSS_SELECTOR).
        :param value: Locator value.
        :param multiple: If True, return a list of elements.
        :return: WebElement or list of WebElements.
        """
        try:
            if multiple:
                logger.debug(f"Finding multiple elements: {by}={value}")
                return WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((by, value))
                )
            else:
                logger.debug(f"Finding single element: {by}={value}")
                return WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((by, value)))
        except Exception as e:
            logger.error(f"Element not found: {by}={value}. Error: {e}")
            raise

    def scroll_to_element(self, driver, element):
        """
        Scroll the page to bring the element into view.
        
        :param driver: Selenium WebDriver instance.
        :param element: WebElement to scroll to.
        """
        if element:
            try:
                logger.debug("Scrolling to element...")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            except Exception as e:
                logger.error(f"Failed to scroll to element. Error: {e}")
                raise


    def click_element(self, driver, by, value):
        """
        Click on a web element.
        
        :param driver: Selenium WebDriver instance.
        :param by: Locator strategy.
        :param value: Locator value.
        """
        element = None  # Initialize element to avoid reference errors

        try:
            # Wait for the element to be clickable
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )

            if not element:
                logger.error(f"Could not retrieve element: {by}={value}")
                return

            logger.info(f"Retrieved element: {by}={value}")
            self.scroll_to_element(driver, element)

            if element.is_displayed() and element.is_enabled():
                logger.info(f"Clicking element: {by}={value}")
                element.click()
                time.sleep(2)
                logger.info(f"Clicked element: {by}={value}")
            else:
                raise Exception("Element is not visible or enabled")
                
        except Exception as e:
            logger.error(f"Failed to click element: {by}={value}. Error: {e}")

            # Ensure element exists before attempting JavaScript click
            if element:
                try:
                    driver.execute_script("arguments[0].click();", element)
                    logger.info(f"Clicked element using JavaScript: {by}={value}")
                except Exception as js_e:
                    logger.error(f"Failed to click element using JavaScript: {by}={value}. Error: {js_e}")
            else:
                logger.error(f"Element not found: {by}={value}. Cannot perform JavaScript click.")

    def type_in_found_element(self, element, text):
        """
        Type text into an already found web element with randomized delays.
        
        :param element: WebElement to type into.
        :param text: Text to type.
        """
        try:
            self._type_text(element, text)
            logger.info("Typed text into found element.")
        except Exception as e:
            logger.error(f"Failed to type into found element. Error: {e}")
            raise

    def _type_text(self, element, text):
        """
        Internal method to type text into an element with randomized delays.
        
        :param element: WebElement to type into.
        :param text: Text to type.
        """
        for character in text:
            element.send_keys(character)
            time.sleep(random.uniform(*self.delay_range))

    def get_element_in_element(self, parent_element, by, value):
        """
        Find and return a child element within a parent element.
        
        :param parent_element: Parent WebElement.
        :param by: Locator strategy.
        :param value: Locator value.
        :return: Child WebElement.
        """
        try:
            logger.debug(f"Finding child element: {by}={value}")
            return parent_element.find_element(by, value)
        except Exception as e:
            logger.error(f"Child element not found: {by}={value}. Error: {e}")
            

    def type_in_element(self, driver, by, value, text):
        element = self.get_element(driver, by, value)
        self._type_text(element, text)
        return element