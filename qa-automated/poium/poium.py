from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from appium.webdriver.common.touch_action import TouchAction

from .page_objects import PageObject


class Page(PageObject):
    """
    Implement the APIs with javascript,
    and selenium/appium extension APIs。
    """

    def run_script(self, js=None):
        """
        run JavaScript script
        """
        if js is None:
            raise ValueError("Please input js script")
        else:
            self.driver.execute_script(js)

    def window_scroll(self, width=None, height=None):
        """
        JavaScript API, Only support css positioning
        Setting width and height of window scroll bar.
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = "window.scrollTo({w},{h});".format(w=width, h=height)
        self.run_script(js)

    def display(self, css_selector):
        """
        JavaScript API, Only support css positioning
        Display hidden elements
        """
        js = 'document.querySelector("{css}").style.display = "block";'.format(css=css_selector)
        self.run_script(js)

    def remove_attribute(self, css_selector, attribute):
        """
        JavaScript API, Only support css positioning
        Remove element attribute, Only support css positioning
        """
        js = 'document.querySelector("{css}").removeAttribute("{attr}");'.format(css=css_selector,
                                                                                 attr=attribute)
        self.run_script(js)

    def get_attribute(self, css_selector, attribute):
        """
        JavaScript API, Only support css positioning
        Get element attribute, Only support css positioning
        :return:
        """
        js = 'return document.querySelector("{css}").getAttribute("{attr}");'.format(
            css=css_selector, attr=attribute)
        return self.driver.execute_script(js)

    @property
    def get_title(self):
        """
        JavaScript API
        Get page title.
        """
        js = 'return document.title;'
        return self.driver.execute_script(js)

    @property
    def get_url(self):
        """
        JavaScript API
        Get page URL.
        """
        js = "return document.URL;"
        return self.driver.execute_script(js)

    def get_text(self, css_selector):
        """
        JavaScript API, Only support css positioning
        Get element text, Only support css positioning
        """
        js = 'return document.querySelector("{css}").textContent;'.format(css=css_selector)
        return self.driver.execute_script(js)

    def set_attribute(self, css_selector, attribute, type_):
        """
        JavaScript API, Only support css positioning
        Setting element attribute, Only support css positioning
        """
        js = 'document.querySelector("{css}").setAttribute("{attr}", "{type}");'.format(css=css_selector,
                                                                                        attr=attribute,
                                                                                        type=type_)
        self.run_script(js)

    def click(self, css_selector):
        """
        JavaScript API, Only support css positioning
        Click element.
        """
        js = 'document.querySelector("{css}").click();'.format(css=css_selector)
        self.run_script(js)

    def set_text(self, css_selector, value):
        """
        JavaScript API, Only support css positioning
        Simulates typing into the element.
        """
        js = 'document.querySelector("{css}").value = "{value}";'.format(css=css_selector, value=value)
        self.run_script(js)

    def clear(self, css_selector):
        """
        JavaScript API, Only support css positioning
        Clears the text if it's a text entry element, Only support css positioning
        """
        js = 'document.querySelector("{css}").value = "";'.format(css=css_selector)
        self.run_script(js)

    def switch_to_frame(self, frame_reference):
        """
        selenium API
        Switches focus to the specified frame, by id, name, or webelement.
        """
        self.driver.switch_to.frame(frame_reference)

    def switch_to_frame_out(self):
        """
        selenium API
        Switches focus to the parent context.
        Corresponding relationship with switch_to_frame () method.
        """
        self.driver.switch_to.parent_frame()

    def switch_to_app(self):
        """
        appium API
        Switch to native app.
        """
        self.driver.switch_to.context('NATIVE_APP')

    def switch_to_web(self, context=None):
        """
        appium API
        Switch to web view.
        """
        if context is not None:
            self.driver.switch_to.context(context)
        else:
            all_context = self.driver.contexts
            for context in all_context:
                if "WEBVIEW" in context:
                    self.driver.switch_to.context(context)

    def accept_alert(self):
        """
        selenium API
        Accept warning box.
        """
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        selenium API
        Dismisses the alert available.
        """
        self.driver.switch_to.alert.dismiss()

    @property
    def get_alert_text(self):
        """
        selenium API
        Get warning box prompt information.
        """
        return self.driver.switch_to.alert.text

    def move_to_element(self, elem):
        """
        selenium API
        Moving the mouse to the middle of an element
        """
        ActionChains(self.driver).move_to_element(elem).perform()

    def context_click(self, elem):
        """
        selenium API
        Performs a context-click (right click) on an element.
        """
        ActionChains(self.driver).context_click(elem).perform()

    def drag_and_drop_by_offset(self, elem, x, y):
        """
        selenium API
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.
        :param elem: The element to mouse down.
        :param x: X offset to move to.
        :param y: Y offset to move to.
        """
        ActionChains(self.driver).drag_and_drop_by_offset(elem, xoffset=x, yoffset=y).perform()

    def refresh_element(self, elem, timeout=10):
        """
        selenium API
        Refreshes the current page, retrieve elements.
        """
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError("Type 'timeout' error, must be type int() ")

        for i in range(timeout_int):
            if elem is not None:
                try:
                    elem
                except StaleElementReferenceException:
                    self.driver.refresh()
                else:
                    break
            else:
                sleep(1)
        else:
            raise TimeoutError("stale element reference: element is not attached to the page document.")

    def swipe_in_element(self, elem, from_x=0.5, to_x=0.5, from_y=0.8, to_y=0.2, delay=500):
        '''
        for appium
        :param elem `WebElement`
            swipe in this element
        :param delay `int`
            delay time in ms

        example:
            self.swipe_in_element(elem_a, from_x=0.5, to_x=0.5, from_y=0.8, to_y=0.2, delay=1000)
            # swipe in elem_a, from 80% to 20% (from bottom to top)

            self.swipe_in_element(elem_b, from_x=0.1, to_x=0.9, from_y=0.5, to_y=0.5, delay=1000)
            # swipe in elem_b, from 10% to 90% (from left to right)
        '''
        elem_location = elem.location
        elem_size = elem.size
        from_x = elem_location['x'] + (elem_size['width'] * from_x)
        to_x = elem_location['x'] + (elem_size['width'] * to_x)
        from_y = elem_location['y'] + (elem_size['height'] * from_y)
        to_y = elem_location['y'] + (elem_size['height'] * to_y)
        action = TouchAction(self.driver)
        action.press(x=from_x, y=from_y)
        action.wait(delay)
        action.move_to(x=to_x, y=to_y)
        action.release()
        action.perform()
