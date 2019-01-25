#!python3
# coding=utf-8

import getopt
import os
import sys
import time
import traceback
import logging

from selenium.common.exceptions import NoSuchElementException
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

import deviceinfo
import util


class Travel:
    def __init__(
        self, driver=None, screen_folder="" , ip="localhost",
        version="", time_out=5, log_file="", log_level=logging.INFO,
        country="ke", method_name="quicktest"
    ):
        if(log_file == ""):
            logging.basicConfig(level=log_level)
        else:
            log_dir = os.path.dirname(log_file)
            if(not os.path.exists(log_dir)):
                os.makedirs(log_dir)
            logging.basicConfig(filename=log_file, level=log_level)
        # deviceinfo.restart_adb_server()
        if(version == ""):
            version = deviceinfo.get_android_version()
        if(driver is None):
            opts = {
                "platformName": "Android",
                "platformVersion": version,
                "deviceName": "Android",
                "appPackage": "com.sportybet.android",
                "appActivity": "com.sportybet.android.home.MainActivity",
                "automationName": "appium",
                "autoGrantPermissions": "true"
            }
            url = "http://{}:4723/wd/hub".format(ip)
            driver = webdriver.Remote(url, opts)
            driver.implicitly_wait(time_out)
        screen_folder = (
            "{}\\{}_{}_{}_{}\\".format(
                screen_folder,
                country,
                method_name, 
                time.strftime("%Y%m%d_%H%M",time.localtime()),
                version
            )
        )
        print(screen_folder)
        if(type(driver) != webdriver.Remote):
            raise Exception("type(driver) != webdriver.Remote")
        self.driver = driver
        self.screen_folder = screen_folder
        self.outcome_num = 3
        self.stake = 100

        self.screen_size = driver.get_window_size()
        self.screen_width = self.screen_size["width"]
        self.screen_height = self.screen_size["height"]
        self.density = deviceinfo.get_density()
        self.screen_index = 0
        self.has_screen_index = True
        self.country = country
        self.method_name = method_name

    def run(self):
        try:
            time.sleep(15)
            self.try_close_ads()
            self.set_country(self.country)
            time.sleep(15)
            self.try_close_ads()
            self.try_close_gift_pop()
            self.home()
            self.login()
            self.try_close_ads()
            self.az()
            self.deposit_and_withdraw()
            self.sports_list_details_choose_outcomes()
            self.open_betslip()
            self.place_bet()
            self.bet_history()
            self.cashout_page()
            self.live_betting()
            self.live_detail()
            self.bingo()
            self.roulette()
        except Exception as err:
            self.take_screen("error")
            raise err
        return self

    

    def run_online(self):
        try:
            self.wait(10)
            self.try_close_update().try_close_ads().try_close_update()\
                .set_country(self.country).wait(10)\
                .try_close_update().try_close_ads().try_close_update()\
                .login().try_close_ads().az()\
                .sports_list_details_choose_outcomes()\
                .open_betslip().betslip_no_order()\
                .live_betting().live_detail().bingo().roulette()
        except Exception as err:
            self.take_screen("error")
            raise err
        return self

    def quit(self):
        self.driver.quit()

    def set_country(self, country):
        """
        from: top page
        to: home
        """
        country = country.lower()
        if(country == "ke"):
            self.phone = "0792338137"
            self.passwd = "qwe123"
            region_text = "Kenya"
            self.min_stake = 50
        elif(country == "ng"):
            self.phone = "8146610183"
            self.passwd = "qwe123"
            region_text = "Nigeria"
            self.min_stake = 400
        elif(country == "gh"):
            self.phone = "240087457"
            self.passwd = "qwe123"
            self.min_stake = 1
            region_text = "Ghana"
        else:
            raise Exception("region not defined: {}".format(country))

        el_bottom = self.driver.find_element_by_id("android:id/tabs")
        els = el_bottom.find_elements_by_class_name(
            "android.widget.RelativeLayout"
        )
        els[-1].click()
        time.sleep(5)
        el = self.driver.find_element_by_id("com.sportybet.android:id/general")
        time.sleep(5) # wait for deposit pop
        el.click()
        el = self.driver.find_element_by_id("com.sportybet.android:id/country")
        if(el.text == region_text):
            # back to homepage
            self.back()
            els[0].click()
        else:
            ##
            el = self.driver.find_element_by_id(
                "com.sportybet.android:id/change_region"
            )
            el.click()
            resource_id = "com.sportybet.android:id/{}".format(country)
            try:
                el = self.driver.find_element_by_id(resource_id)
                self.take_screen("change_region")
                el.click()
                time.sleep(10)
                el = self.driver.find_element_by_id("com.sportybet.android:id/skip")
                el.click()
            except expression as identifier:
                raise Exception("can not find country: ".format(country))
        time.sleep(1)
        return self

    def before(self):
        """
        from: splash_screen
        to: home
        """
        self.take_screen("splash_screen")
        el = self.driver.find_element_by_id("com.sportybet.android:id/skip")
        el.click()
        time.sleep(1)
        return self

    def login(self):
        """
            from: home, not loged in
            to: home
        """
        el = self.driver.find_element_by_id("com.sportybet.android:id/login")
        el.click()
        time.sleep(2)
        el = self.driver.find_element_by_id("com.sportybet.android:id/mobile")
        el.set_value(self.phone)
        time.sleep(1)
        self.try_hide_keyboard()
        time.sleep(1)
        self.take_screen("login")
        el = self.driver.find_element_by_id("com.sportybet.android:id/next")
        el.click()

        el = self.driver.find_element_by_id("com.sportybet.android:id/password")
        el.set_value(self.passwd)
        time.sleep(1)
        self.try_hide_keyboard()
        time.sleep(1)
        self.take_screen("password")
        el = self.driver.find_element_by_id("com.sportybet.android:id/log_in")
        time.sleep(1)
        el.click()
        time.sleep(2)
        return self
    
    def chose_outcomes(self):
        """
            from: home
            to: home (not top)
        """
        for x in range(4):
            self.swipe_up()
            time.sleep(0.2)
        el_parent = self.driver.find_element_by_id(
            "com.sportybet.android:id/highlights"
        )
        els = el_parent.find_elements_by_id(
            "com.sportybet.android:id/o1"
        )
        num = min(self.outcome_num, len(els))
        for el in els[0:num]:
            el.click()
        self.take_screen("home_select_outcomes")
        time.sleep(1)
        return self
    
    def open_betslip(self):
        """
            from: home
            to: betslip
        """
        betslip_x = self.screen_width - deviceinfo.dp_to_px(12, self.density)
        betslip_y = self.screen_height - deviceinfo.dp_to_px(66, self.density)
        actions = TouchAction(self.driver)
        actions.tap(x=betslip_x, y=betslip_y)
        actions.perform()
        time.sleep(2)
        return self

    def betslip_no_order(self):
        """check betslip without placing bet
        from: betslip
        to: back
        """
        time.sleep(5)
        for x in range(2):
            self.swipe_up()
            time.sleep(2)
        el_stake = self.driver.find_element_by_id(
            "com.sportybet.android:id/edit_text_ksh"
        )
        el_stake.click()
        for x in range(8):
            self.driver.press_keycode(util.key_code_backspace)
            self.driver.press_keycode(util.key_code_del_forward)
            time.sleep(0.1)
        el_stake.set_value(self.stake)
        self.try_hide_keyboard()
        time.sleep(1)
        self.swipe_up()
        self.take_screen("betslip")
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/back_icon"
        )
        # back 
        el.click()
        time.sleep(3)
        self.back_to_top()
        time.sleep(1)
        return self

    def place_bet(self):
        """
            from: betslip page
            to: home
        """
        time.sleep(5)
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/auto_change_switch"
        )
        el.click()
        self.take_screen("betslip")
        for x in range(2):
            self.swipe_up()
            time.sleep(2)
        try:
            el_stake = self.driver.find_element_by_id(
                "com.sportybet.android:id/edit_text_ksh"
            )
            # el_stake.click()
        except Exception:
            # if there is no stake textbox, back to home page
            self.back()
            time.sleep(3)
            return self

        # for x in range(8):
        #     self.driver.press_keycode(util.key_code_backspace)
        #     self.driver.press_keycode(util.key_code_del_forward)
        #     time.sleep(0.1)
        # el_stake.set_value(self.stake)
        # self.try_hide_keyboard()
        time.sleep(1)
        self.swipe_up()
        el_place_bet = self.driver.find_element_by_id(
            "com.sportybet.android:id/place_bet_btn"
        )
        el_place_bet.click()
        el_confirm = self.driver.find_element_by_id(
            "com.sportybet.android:id/confirm"
        )
        el_confirm.click()
        try:
            el = self.driver.find_element_by_id(
                "com.sportybet.android:id/ok"
            )
            self.take_screen("place_bet_seccuss")
            # back home
            el.click()
        except:
            el = None
            el = self.find_element_by_id_and_text("android:id/button1", "OK")
            if(el is not None):
                self.take_screen("place_bet_fail")
                el.click()
                self.back()
        time.sleep(3)
        return self
                
    
    def deposit_and_withdraw(self):
        """
            from: top page
            to: home
        """
        el_bottom = self.driver.find_element_by_id(
            "android:id/tabs"
        )
        els = el_bottom.find_elements_by_class_name(
            "android.widget.RelativeLayout"
        )
        els[-1].click()

        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/deposit"
        )
        el.click()

        if(self.country == "ke"):
            el_tab = self.driver.find_element_by_id(
                "com.sportybet.android:id/deposit_tab"
            )
            els = el_tab.find_elements_by_class_name(
                "android.support.v7.app.ActionBar$Tab"
            )
            if(not els):
                print("deposit page: cannot find tab")
                return self
            els[0].click()
            el = self.driver.find_element_by_id(
                "com.sportybet.android:id/amount_edit_text"
            )
            el.set_value("10")
            self.try_hide_keyboard()
            time.sleep(1)
            self.take_screen("deposit")
            # el = self.driver.find_element_by_id(
            #     "com.sportybet.android:id/deposit_btn"
            # )
            # el.click()

            time.sleep(1)
            
            els[1].click()
            self.take_screen("deposit_paybill")
            self.back()
        elif(self.country == "ng"):
            el_tab = self.driver.find_element_by_id(
                "com.sportybet.android:id/tab"
            )
            els = el_tab.find_elements_by_class_name(
                "android.support.v7.app.ActionBar$Tab"
            )
            if(not els):
                print("deposit page: cannot find tab")
                return self
            tab_index = 0
            for el in els:
                el.click()
                time.sleep(1)
                self.take_screen("deposit_{}".format(tab_index))
                tab_index += 1
            self.back()
        elif(self.country == "gh"):
            el_tab = self.driver.find_element_by_id(
                "com.sportybet.android:id/deposit_tab"
            )
            els = el_tab.find_elements_by_class_name(
                "android.support.v7.app.ActionBar$Tab"
            )
            if(not els):
                print("deposit page: cannot find tab")
                return self
            tab_index = 0
            for el in els:
                el.click()
                time.sleep(1)
                self.take_screen("deposit_{}".format(tab_index))
                tab_index += 1
            self.back()

        # withdraw
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/withdraw"
        )
        el.click()
        if(self.country == "ke" or self.country == "gh"):
            time.sleep(3)
            self.take_screen("withdraw")
            time.sleep(0.5)
            self.back()
        elif(self.country == "ng"):
            el_tab = self.driver.find_element_by_id(
                "com.sportybet.android:id/tab"
            )
            els = el_tab.find_elements_by_class_name(
                "android.support.v7.app.ActionBar$Tab"
            )
            if(not els):
                print("withdraw page: cannot find tab")
                return self
            tab_index = 0
            for el in els:
                el.click()
                time.sleep(1)
                self.take_screen("withdraw_{}".format(tab_index))
                tab_index += 1
            self.back()

        # transactions
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/balance_container"
        )
        el.click()
        time.sleep(3)
        self.take_screen("transactions")
        time.sleep(1)

        el_title = self.find("com.sportybet.android:id/title")
        el_title.click()
        time.sleep(1)
        self.take_screen("transactions_filter")

        el_items = self.driver.find_elements_by_id(
            "com.sportybet.android:id/item"
        )
        self.back()
        for x in range(1, len(el_items)):
            time.sleep(1)
            self.find("com.sportybet.android:id/title").click()
            el_items[x].click()
            time.sleep(2)
            try:
                el = self.find("com.sportybet.android:id/balance")
                el.click()
                time.sleep(1)
                self.find("com.sportybet.android:id/status")
                time.sleep(1)
                self.take_screen("transactions_details_{}".format(x))
                self.back()
            except NoSuchElementException:
                pass
            
        self.back()
        self.back_home_from_top_page()
        time.sleep(1)
        return self
        # if(country == "ke"):
        #     el = self.driver.find_element_by_id(
        #         "com.sportybet.android:id/amount_edit_text"
        #     )
        #     el.set_value("10")
        #     self.try_hide_keyboard()
        #     time.sleep(1)
        #     self.take_screen("withdraw")

        #     el = self.driver.find_element_by_id(
        #         "com.sportybet.android:id/withdraw_btn"
        #     )
        #     el.click()

        #     el = self.driver.find_element_by_id(
        #         "com.sportybet.android:id/confirm"
        #     )
        #     el.click()
        #     time.sleep(3)
        #     els = self.driver.find_elements_by_id(
        #         "android:id/button1"
        #     )
        #     self.take_screen("withdraw_result")

        #     success = False
        #     # go to transactions
        #     if(not els):
        #         els = self.driver.find_elements_by_id(
        #             "com.sportybet.android:id/check_status"
        #         )
        #         success = True
        #     if(not els):
        #         print("unexcepted withdraw result.")
        #         self.take_screen("unexcepted_withdraw_result")
        #         sys.exit()
        #     els[0].click()
        #     time.sleep(5)
        #     el = self.driver.find_element_by_id(
        #         "com.sportybet.android:id/goback"
        #     )
        #     self.take_screen("transactions")
        #     el.click()
        #     time.sleep(2)
        #     if(not success):
        #         self.back()
        #         time.sleep(1)
        #     self.back_home_from_top_page()
        # else:
        #     time.sleep(3)
        #     self.take_screen("withdraw")
        #     self.back()

        # el_bottom = self.driver.find_element_by_id(
        #     "android:id/tabs"
        # )
        # els = el_bottom.find_elements_by_class_name(
        #     "android.widget.RelativeLayout"
        # )
        # # go home
        # els[0].click()

    def sports_list_details_choose_outcomes(self):
        """
            from: home
            to: home
        """
        #### sports menu
        el_container = self.driver.find_element_by_id(
            "com.sportybet.android:id/entry_container"
        )
        el = el_container.find_element_by_android_uiautomator(
            'new UiSelector().text("Sports")'
        )
        # go to sports menu
        el.click()
        time.sleep(1)
        el = self.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("All Football")'
        )
        self.take_screen("sports_menu")
        el.click()

        #### sports list
        el_sort = self.driver.find_element_by_id(
            "com.sportybet.android:id/sort"
        )
        time.sleep(5)
        self.take_screen("sports")
        els = self.driver.find_elements_by_id(
            "com.sportybet.android:id/o1"
        )
        num = min(self.outcome_num, len(els))
        for el in els[0:num]:
            el.click()
            time.sleep(0.5)
        el_sort.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/sort_league"
        )
        el.click()
        time.sleep(5)
        self.take_screen("sports_list")

        #### sports details
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/away_team"
        )
        el.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/top_info_container"
        )
        self.take_screen("prematch_details")
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/tab_stats"
        )
        el.click()
        time.sleep(10)
        self.take_screen("prematch_stats")
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/tab_comments"
        )
        el.click()
        time.sleep(5)
        self.take_screen("prematch_comments")

        # back to sports menu page
        self.back().wait(2).back().wait(2)

        # expand first category
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/root"
        )
        el.click()
        time.sleep(1)

        #### tournament
        # open first tournament
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/sports_event_tournament_layout"
        )
        el.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/o1"
        )
        self.take_screen("sports_tournament")
        time.sleep(1)
        # back to home page
        self.back().wait(1).back().wait(3)

    def sports_list(self, do_choose_outcomes=False):
        """
            from: home
            to: home
        """
        el_container = self.driver.find_element_by_id(
            "com.sportybet.android:id/entry_container"
        )
        el = el_container.find_element_by_android_uiautomator(
            'new UiSelector().text("Sports")'
        )
        # go to sports menu
        el.click()
        time.sleep(1)
        el = self.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("All Football")'
        )
        self.take_screen("sports_menu")
        el.click()
        el_sort = self.driver.find_element_by_id(
            "com.sportybet.android:id/sort"
        )
        time.sleep(5)
        self.take_screen("sports")
        if(do_choose_outcomes):
            els = self.driver.find_elements_by_id(
                "com.sportybet.android:id/o1"
            )
            num = min(self.outcome_num, len(els))
            for el in els[0:num]:
                el.click()
                time.sleep(0.5)
        el_sort.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/sort_league"
        )
        el.click()
        time.sleep(5)
        self.take_screen("sports_list")

        # back to sports menu page
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/back_icon"
        )
        el.click()
        time.sleep(1)
        # expand first category
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/root"
        )
        el.click()
        time.sleep(1)
        # open first tournament
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/sports_event_tournament_layout"
        )
        el.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/o1"
        )
        self.take_screen("sports_tournament")
        # back home
        for x in range(2):
            el = self.driver.find_element_by_id(
                "com.sportybet.android:id/back_icon"
            )
            el.click()
            time.sleep(2)
        return self

    def sports_detail(self):
        """
        from: home
        to: home
        """
        for x in range(3):
            self.swipe_up()
            time.sleep(1)
        # click home team name. go to pre match details
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/home"
        )
        el.click()
        time.sleep(5)
        self.take_screen("prematch_details")
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/tab_stats"
        )
        el.click()
        time.sleep(20)
        self.take_screen("prematch_stats")
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/tab_comments"
        )
        el.click()
        time.sleep(5)
        self.take_screen("prematch_comments")
        # back home
        self.back()
        time.sleep(3)
        self.back_to_top().back_to_top()
        time.sleep(1)
        return self

    def live_betting(self):
        """
        from: home
        to: home
        """
        el_container = self.driver.find_element_by_id(
            "com.sportybet.android:id/entry_container"
        )
        el = el_container.find_element_by_android_uiautomator(
            'new UiSelector().text("Live")'
        )
        # go to live list page
        el.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/cancel_btn"
        )
        self.take_screen("live_list_0")
        el.click()
        # 7 tabs: Live/Schedule/Football/Basketball/Tennis/Rugby/Cricket
        els = self.driver.find_elements_by_class_name(
            "android.support.v7.app.ActionBar$Tab"
        )
        n_left = len(els)
        for x in range(2, n_left):
            els[x].click()
            time.sleep(5)
            self.take_screen("live_list_{}".format(x))
        if(n_left < 7):
            n_right = 7 - n_left
            actions = TouchAction(self.driver)
            actions.press(els[n_left-1])
            actions.move_to(els[2])
            actions.release()
            actions.perform()
            els = self.driver.find_elements_by_class_name(
                "android.support.v7.app.ActionBar$Tab"
            )
            for x in range(-n_right, 0):
                els[x].click()
                time.sleep(5)
                self.take_screen("live_list_{}".format(
                    6 + x
                ))
        els[1].click()
        time.sleep(5)
        self.take_screen("schedule")
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/goback"
        )
        el.click()
        time.sleep(1)
        return self
    
    def live_detail(self):
        """
        from: home
        to: home
        """
        el_destination = self.driver.find_element_by_id(
            "com.sportybet.android:id/logo"
        )
        
        el_container = self.driver.find_element_by_id(
            "com.sportybet.android:id/entry_container"
        )
        self.driver.drag_and_drop(el_container, el_destination)
        time.sleep(5)
        els = self.driver.find_elements_by_id(
            "com.sportybet.android:id/live_title"
        )
        if(els == []):
            print("no live match")
            return 0
        self.driver.drag_and_drop(els[0], el_destination)
        el_live_panel = self.driver.find_element_by_id(
            "com.sportybet.android:id/live_panel"
        )
        el = el_live_panel.find_element_by_id(
            "com.sportybet.android:id/team1"
        )
        el.click()
        time.sleep(2)
        els = self.driver.find_elements_by_class_name(
            "android.support.v7.app.ActionBar$Tab"
        )
        for x in range(len(els)):
            els[x].click()
            time.sleep(2)
            self.take_screen("live_detail_{}".format(x))
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/change_match"
        )
        el.click()
        time.sleep(1)
        els = self.driver.find_elements_by_id(
            "com.sportybet.android:id/team"
        )
        self.take_screen("live_detail_change")
        if(len(els) > 1):
            els[1].click()
            time.sleep(2)
            el = self.driver.find_element_by_class_name(
                "android.support.v7.app.ActionBar$Tab"
            )
            self.take_screen("live_detail_changed")
        else:
            self.back()
            time.sleep(1)
        self.back()
        time.sleep(2)
        self.back_to_top()
        time.sleep(1)
        return self

    def az(self):
        """
        from: top pages
        to: home
        """
        el_bottom = self.driver.find_element_by_id(
            "android:id/tabs"
        )
        els = el_bottom.find_elements_by_class_name(
            "android.widget.RelativeLayout"
        )
        els[1].click()
        time.sleep(2)
        self.try_hide_keyboard()
        el_tab_container = self.driver.find_element_by_id(
            "com.sportybet.android:id/tab_layout"
        )
        el_tabs = el_tab_container.find_elements_by_class_name(
            "android.support.v7.app.ActionBar$Tab"
        )
        for el_tab in el_tabs:
            els_sports = self.driver.find_elements_by_id(
                "com.sportybet.android:id/az_menu_sports_item_text"
            )
            for x in range(len(els_sports)):
                els_sports[x].click()
                time.sleep(0.5)
                self.take_screen("az_menu_{}".format(x))

        els[0].click()
        time.sleep(2)
        return self

    def cashout_page(self):
        """
        from: home
        to: home
        """
        el_bottom = self.driver.find_element_by_id(
            "android:id/tabs"
        )
        els = el_bottom.find_elements_by_class_name(
            "android.widget.RelativeLayout"
        )
        els[-2].click()
        time.sleep(3)
        self.take_screen("cashout")
        els[0].click()
        time.sleep(1)
        return self

    def bingo(self):
        """
        from: home
        to: home
        """
        el = self.find_quick_entry("SportyBingo")
        el.click()
        for x in range(10):
            el = self.driver.find_element_by_id(
                "com.sportybet.plugin.yyg:id/join_btn"
            )
            if(x == 0):
                self.take_screen("sportybingo")
            el.click()
            el = self.driver.find_element_by_id(
                "com.sportybet.plugin.yyg:id/join_container"
            )
            el.click()
            els = self.driver.find_elements_by_id("android:id/button1")
            if(not els):
                break
            btn1_text = els[0].text
            el = els[0]
            if(btn1_text == "OK"):
                self.take_screen("sportybingo_buy_err")
                el.click()
                continue
            else:
                els2 = self.driver.find_elements_by_id("android:id/button2")
                if(els2):
                    btn2_text = els2[0].text
                    if(btn2_text == "CANCEL" or btn2_text == "LATER"):
                        el = els2[0]
            self.take_screen("sportybingo_buy_err")
            el.click()
            break

        el_top_tab = self.driver.find_element_by_id(
            "com.sportybet.plugin.yyg:id/tabLayout"
        )
        el_tabs = el_top_tab.find_elements_by_class_name(
            "android.support.v7.app.ActionBar$Tab"
        )
        el_published = el_tabs[1]
        el_published.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.plugin.yyg:id/status"
        )
        self.take_screen("sportybingo_published")
        el_mine = el_tabs[2]
        el_mine.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.plugin.yyg:id/on_going"
        )
        self.take_screen("sportybingo_mine")
        el.click()
        time.sleep(3)
        self.take_screen("sportybingo_mine_ongoing")
        el = self.driver.find_element_by_id(
            "com.sportybet.plugin.yyg:id/published"
        )
        el.click()
        time.sleep(3)
        self.take_screen("sportybingo_mine_published")
        self.back()
        time.sleep(1)
        return self

    def roulette(self):
        """
        from: home
        to: home
        """
        el = self.find_quick_entry("Roulette")
        el.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.plugin.roulette:id/bet_16"
        )
        el.click()
        time.sleep(1)
        el = self.driver.find_element_by_id(
            "com.sportybet.plugin.roulette:id/bet_19"
        )
        el.click()
        time.sleep(1)
        self.take_screen("roulette")
        el = self.driver.find_element_by_id(
            "com.sportybet.plugin.roulette:id/spin"
        )
        el.click()
        time.sleep(2)
        self.take_screen("roulette_spin")
        time.sleep(10)
        el = self.driver.find_element_by_id(
            "com.sportybet.android:id/auto"
        )
        el.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.plugin.roulette:id/play"
        )
        self.take_screen("roulette_auto")
        el.click()
        time.sleep(10)
        self.take_screen("roulette_auto_play")
        time.sleep(40)
        self.take_screen("roulette_1")
        el = self.driver.find_element_by_id(
            "com.sportybet.plugin.roulette:id/order"
        )
        el.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.plugin.roulette:id/result"
        )
        self.take_screen("roulette_history")
        el.click()
        el = self.driver.find_element_by_id(
            "com.sportybet.plugin.roulette:id/rebet"
        )
        self.take_screen("roulette_history_details")
        self.back()
        time.sleep(2)
        self.back()
        time.sleep(2)
        return self

    def home(self):
        time.sleep(1)
        self.take_screen("home")
        for x in range(5):
            self.swipe_up(1000)
            time.sleep(1)
            try:
                el = self.find("com.sportybet.android:id/highlight_title")
                el_logo = self.find("com.sportybet.android:id/logo")
                self.driver.drag_and_drop(el, el_logo)
                break
            except NoSuchElementException:
                if(x >= 4):
                    return self
                continue
        el_tab = self.find("com.sportybet.android:id/highlight_tab")
        els = el_tab.find_elements_by_class_name(
            "android.support.v7.app.ActionBar$Tab"
        )
        for x in range(len(els)):
            els[x].click()
            time.sleep(3)
            self.take_screen("home_prematch_{}".format(x))
            time.sleep(0.5)
        self.back_to_top()
        time.sleep(1)
        return self

    def bet_history(self):
        """
        from: home
        to: home
        """
        el_bottom = self.driver.find_element_by_id(
            "android:id/tabs"
        )
        els = el_bottom.find_elements_by_class_name(
            "android.widget.RelativeLayout"
        )
        els[-1].click()
        time.sleep(6)
        self.find("com.sportybet.android:id/bets").click()
        time.sleep(1)
        el_tab_container = self.find("com.sportybet.android:id/tab_line")
        el_unsettled = self.find_child_text(el_tab_container, "Unsettled")
        el_cashout = self.find_child_text(el_tab_container, "Cashout")
        el_settled = self.find_child_text(el_tab_container, "Settled")
        el_all = self.find_child_text(el_tab_container, "All")
        el_unsettled.click()
        time.sleep(2)
        self.take_screen("bet_history_unsettled")
        el_cashout.click()
        time.sleep(2)
        self.take_screen("bet_history_cashout")
        time.sleep(2)
        el_settled.click()
        time.sleep(2)
        self.take_screen("bet_history_settled")
        el_all.click()
        time.sleep(2)
        self.take_screen("bet_history_all")
        self.find("com.sportybet.android:id/r_bet_root").click()
        self.wait(3).take_screen("ticket_details")
        self.swipe_up().wait(2).swipe_up().wait(2).swipe_up().wait(2)
        self.take_screen("ticket_details_1")
        self.find("com.sportybet.android:id/td_ticket_bet_detail").click()
        self.wait(2).take_screen("bet_details")
        self.back().wait(1).back().wait(1)
        el_win_switch = self.find("com.sportybet.android:id/win_switch")
        el_win_switch.click()
        self.take_screen("bet_history_win")
        self.back().wait(1).back_home_from_top_page().wait(1)
        return self

    ###########################################################################
    def take_screen(self, screen_name):
        if(self.has_screen_index):
            screen_name = "travel_{0:03d}_{1}.png".format(self.screen_index, screen_name)
        else:
            screen_name = "travel_{}.png".format(screen_name)
        screen_path = os.path.join(self.screen_folder, screen_name)
        util.base64_to_img(self.driver.get_screenshot_as_base64(), screen_path)
        self.screen_index += 1
        return self
    
    def try_close_ads(self):
        try:
            el = self.driver.find_element_by_id(
                "com.sportybet.android:id/close"
            )
            el.click()
        except:
            pass
        time.sleep(2)
        return self

    def try_close_gift_pop(self):
        try:
            el = self.driver.find_element_by_id(
                "com.sportybet.android:id/get_gifts_close"
            )
            el.click()
        except NoSuchElementException:
            pass
        time.sleep(1)
        return self

    def swipe_up(self, wait_time=500):
        self.driver.swipe(
            self.screen_width/2, self.screen_height*3/4, 
            self.screen_width/2, self.screen_height/4, 
            wait_time
        )
        return self
    
    def swipe_element(self, origin_el, destination_el, wait_time=500):
        action = TouchAction(self.driver)
        action.press(origin_el).wait(wait_time).move_to(destination_el).release().perform()
        return self

    def back_to_top(self):
        for x in range(4):
            self.driver.swipe(
                self.screen_width/2, self.screen_height/2, 
                self.screen_width/2, self.screen_height*4/5, 
                150
            )
            time.sleep(2)
        return self
    
    def try_hide_keyboard(self):
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    def find_quick_entry(self, entry_name):
        el_container = self.driver.find_element_by_id(
            "com.sportybet.android:id/entry_container"
        )
        el = el_container.find_element_by_android_uiautomator(
            'new UiSelector().text("{}")'.format(entry_name)
        )
        return el

    def find_element_by_id_and_text(self, id, text):
        els = self.driver.find_elements_by_id(id)
        if(not els):
            return None
        for el in els:
            if(el.text == text):
                return el
        return None
    
    def try_close_update(self):
        el = self.find_element_by_id_and_text("android:id/button2", "CANCEL")
        if(el is not None):
            el.click()
            time.sleep(1)
        return self

    def back(self):
        self.driver.press_keycode(util.key_code_back)
        return self
    
    def back_home_from_top_page(self):
        el_bottom = self.driver.find_element_by_id(
            "android:id/tabs"
        )
        els = el_bottom.find_elements_by_class_name(
            "android.widget.RelativeLayout"
        )
        els[0].click()
        return self
    
    def wait(self, seconds):
        time.sleep(seconds)
        return self

    def find(self, id):
        return self.driver.find_element_by_id(id)

    def find_child_text(self, parent, text):
        els = parent.find_elements_by_class_name("android.widget.TextView")
        for el in els:
            if(el.text == text):
                return el
        return None

    def get_text_by_id(self, id):
        try:
            el = self.driver.find_element_by_id(id)
        except NoSuchElementException:
            return ""
        return el.text
    
    def get_float_by_id(self, id):
        """
        return float. 
        if no element, return 0.
        """
        try:
            el = self.driver.find_element_by_id(id)
        except NoSuchElementException:
            return 0
        return float(el.text.replace(",", ""))
    
    def set_stake(self, stake_num=""):
        """
        set stake
        make sure only one keyboard in screen
        """
        stake_num = str(stake_num)
        el_del_key = self.find("com.sportybet.android:id/rl_del")
        action = TouchAction(self.driver)
        action.long_press(el_del_key).perform()
        logging.info("clear stake input box")
        for digital in stake_num:
            self.find_element_by_id_and_text(
                "com.sportybet.android:id/tv_key", digital
            ).click()
            time.sleep(0.15)
        logging.info("input stake: {}".format(stake_num))
        self.find_element_by_id_and_text(
            "com.sportybet.android:id/tv_key", "Done"
        ).click()
        return self

    def element_contains(self, el_parent, el_child):
        """if el_parent contains el_child
        """
        # rect "x","y","height","weight"
        rect_parent = el_parent.rect
        rect_child = el_child.rect
        if(rect_parent["x"] - 1 > rect_child["x"] or rect_parent["y"] - 1 > rect_child["y"]):
            return False
        if(rect_parent["x"] + rect_parent["width"] + 1 < rect_child["x"] + rect_child["width"]):
            return False
        if(rect_parent["y"] + rect_parent["height"] + 1 < rect_child["y"] + rect_child["height"]):
            return False
        return True
