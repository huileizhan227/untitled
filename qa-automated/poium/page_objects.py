import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from appium.webdriver.common.mobileby import MobileBy


# Map PageElement constructor arguments to webdriver locator enums
LOCATOR_LIST = {
    # selenium
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME,
    # appium
    'ios_uiautomation': MobileBy.IOS_UIAUTOMATION,
    'ios_predicate': MobileBy.IOS_PREDICATE,
    'ios_class_chain': MobileBy.IOS_CLASS_CHAIN,
    'android_uiautomator': MobileBy.ANDROID_UIAUTOMATOR,
    'android_viewtag': MobileBy.ANDROID_VIEWTAG,
    'accessibility_id': MobileBy.ACCESSIBILITY_ID,
    'image': MobileBy.IMAGE,
    'custom': MobileBy.CUSTOM,
}


class PageObject:
    """Page Object pattern."""

    def __init__(self, driver, url=None):
        """
        :param driver: `selenium.webdriver.WebDriver` Selenium webdriver instance
        :param url: `str`
            Root URI to base any calls to the ``PageObject.get`` method. If not defined
            in the constructor it will try and look it from the webdriver object.
        """
        self.driver = driver
        self.root_uri = url if url else getattr(self.driver, 'url', None)

    def get(self, uri):
        """
        :param uri:  URI to GET, based off of the root_uri attribute.
        """
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)


class PageElement(object):
    """Page Element descriptor.

    :param css:    `str`
        Use this css locator
    :param id_:    `str`
        Use this element ID locator
    :param name:    `str`
        Use this element name locator
    :param xpath:    `str`
        Use this xpath locator
    :param link_text:    `str`
        Use this link text locator
    :param partial_link_text:    `str`
        Use this partial link text locator
    :param tag:    `str`
        Use this tag name locator
    :param class_name:    `str`
        Use this class locator
    :param context: `str` or `bool`
        This element will be found with context. context can be a element name
        or bool. If context is `True`, this attribute will be callable.

    Page Elements are used to access elements on a page. The are constructed
    using this factory method to specify the locator for the element.
        >>> from page_objects import PageObject, PageElement
        >>> class MyPage(PageObject):
                elem1 = PageElement(css='div.myclass')
                elem2 = PageElement(id_='foo')
                elem_with_context_1 = PageElement(name='bar', context='elem1')
                elem_with_context_2 = PageElement(name='bar', context=True)
        >>> page = MyPage(driver)
        >>> test_elem1 = page.elem1
        >>> test_elem2 = page.elem_with_context_1
        # if context is True, then this elem must be called with a parameter.
        >>> test_elem3 = page.elem_with_context_2(elem2)

    Page Elements act as property descriptors for their Page Object, you can get
    and set them as normal attributes.
    """
    def __init__(self, context=None, timeout=10, **kwargs):
        self.timeout = timeout
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        k, v = next(iter(kwargs.items()))
        try:
            self.locator = (LOCATOR_LIST[k], v)
        except KeyError:
            raise ValueError(
                "locator name error: {}. Available locator name: {}".format(
                    k, list(LOCATOR_LIST)
                )
            )
        self.context = context

    def get_element(self, context):
        try:
            return context.find_element(*self.locator)
        except NoSuchElementException:
            return None

    def find(self, context, delay=0):
        time_start = time.time()
        while True:
            el = self.get_element(context)
            if el is not None:
                time.sleep(delay)
                return el
            else:
                if time.time() - time_start > self.timeout:
                    return None
                time.sleep(1)
        return None

    def __get__(self, instance, owner):
        if not instance:
            return None
        delay = getattr(instance, 'delay', 0)
        if type(self.context) is str:
            context = instance.__getattribute__(self.context)
        elif self.context:
            return lambda ctx: self.find(ctx, delay)
        else:
            context = instance.driver

        return self.find(context, delay)

    def __set__(self, instance, value):
        elem = self.__get__(instance, instance.__class__)
        if(callable(elem)):
            raise ValueError("Sorry, the set descriptor doesn't support callable element.")
        if not elem:
            raise ValueError("Can't set value, element not found")
        elem.send_keys(value)


class PageElements(PageElement):
    """Like `PageElement` but returns multiple results.
    
    >>> from page_objects import PageObject, PageElements
    >>> class MyPage(PageObject):
            all_table_rows = PageElements(tag='tr')
            elem2 = PageElement(id_='foo')
            elem_with_context = PageElement(tag='tr', context=True)
    """
    def find(self, context, delay=0):
        try:
            els = context.find_elements(*self.locator)
            time.sleep(delay)
            return els
        except NoSuchElementException:
            return []

    def __set__(self, instance, value):
        if(self.context is True):
            raise ValueError("Sorry, the set descriptor doesn't support callable_with_context element.")
        elems = self.__get__(instance, instance.__class__)
        if not elems:
            raise ValueError("Can't set value, no elements found")
        [elem.send_keys(value) for elem in elems]
