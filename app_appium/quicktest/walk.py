import time
import logging
import traceback
from travel import Travel
from selenium.common.exceptions import NoSuchElementException

class Walk(Travel):
    def walk_deposit(self):
        pass
    
    def walk_quickbet(self):
        """
        from: home (no outcome selected)
        to: home
        """
        logging.info("---- walk_quickbet begin")
        self.find_quick_entry("Sports").click()
        logging.info("goto sports page")
        sports_names = ["Football", "Basketball", "Tennis", "Rugby", "Cricket",
                        "Volleyball", "Ice Hockey", "Darts", "Beach Volley"]
        for sport_name in sports_names:
            el_tab = self.find_element_by_id_and_text(
                "com.sportybet.android:id/tab_name", sport_name
            )
            if el_tab is None:
                logging.info("no {} tab".format(sport_name))
                continue
            el_tab.click()
            logging.info("goto {} tab".format(sport_name))
            time.sleep(1)
            entry_text = "All {}".format(sport_name)
            el_entry = self.find_element_by_id_and_text(
                "com.sportybet.android:id/item_text_view", entry_text
            )
            if(el_entry is None):
                continue
            el_entry.click()
            logging.info("goto {}".format(entry_text))
            time.sleep(2)
            try:
                # self.find("com.sportybet.android:id/home_team").click()
                # logging.info("goto the first game")
                el_hometeams = self.driver.find_elements_by_id(
                    "com.sportybet.android:id/home_team"
                )
                el_hometeams[1].click()
                logging.info("goto game details")
            except NoSuchElementException:
                self.back().wait(0.5)
                logging.info("no games, back to sports page")
                continue
            time.sleep(2)
            self.quickbet_sport_detail_new()
            self.wait(1).back().wait(1).back().wait(1)
            logging.info("goto sports page")
        self.back()
        logging.info("goto home page")
        logging.info("---- walk_quickbet over")
        return self
                            
    def quickbet_sport_detail(self):
        """
        from: sport detail page
        to: sport detail page
        """
        el_top = self.find("com.sportybet.android:id/market_tab")
        is_end = False
        while not is_end:
            el_container = self.find("com.sportybet.android:id/event_recycler")
            el_market_containers = el_container.find_elements_by_class_name(
                "android.widget.LinearLayout"
            )
            for el_market_container in el_market_containers:
                if(el_market_container.location["x"] > 0):
                    continue
                try:
                    # 若不添加上面的过滤, 这里会找到多个重复的market_name, 原因未知
                    # 感觉像是appium的bug
                    el_market_name = el_market_container.find_elements_by_id(
                        "com.sportybet.android:id/title"
                    )[0]
                except IndexError:
                    # if no title, it's not market_container
                    continue
                el_grids = el_market_container.find_elements_by_id(
                    "com.sportybet.android:id/grid"
                )
                if(not el_grids):
                    el_market_name.click()
                    logging.info(
                        "expend market {}".format(el_market_name.text)
                    )
                    time.sleep(0.5)
                    el_grids = el_market_container.find_elements_by_id(
                        "com.sportybet.android:id/grid"
                    )
                el_outcomes = []
                if(el_grids):
                    el_outcomes = el_grids[0].find_elements_by_class_name(
                        "android.widget.ToggleButton"
                    )
                for el_outcome in el_outcomes:
                    time.sleep(1.5)
                    try:
                        odds = float(el_outcome.text)
                    except Exception:
                        # if text is not odds, skip
                        continue
                    el_outcome.click()
                    logging.info("select outcome, odds: {}".format(odds))
                    try:
                        el_quickbet_odds = self.find(
                            "com.sportybet.android:id/match_odds"
                        )
                    except NoSuchElementException:
                        self.find("com.sportybet.android:id/delete").click()
                        continue
                    odds_quickbet = float(el_quickbet_odds.text)
                    if(not self.check_equal(odds_quickbet, odds, "quickbet_odds")):
                        el_outcome.click()
                        time.sleep(1)
                        continue
                    el_pot_win = self.find("com.sportybet.android:id/pot_win_value")
                    pot_win_quickbet = el_pot_win.text
                    self.find("com.sportybet.android:id/place_bet_btn").click()
                    logging.info("click quickbet placebet btn")
                    el_pay = self.find("com.sportybet.android:id/payValue")
                    pay = el_pay.text[5:]
                    self.find("com.sportybet.android:id/confirm").click()
                    logging.info("click confirm btn")
                    time.sleep(1)
                    # success page
                    stake_suc = self.get_text_by_id(
                        "com.sportybet.android:id/total_stake_value"
                    )
                    self.check_equal(pay, stake_suc, "stake_suc") 
                    pot_win_suc = self.get_text_by_id(
                        "com.sportybet.android:id/potwin_value"
                    )
                    self.check_equal(pot_win_suc, pot_win_quickbet, "pot_win_suc")
                    self.find("com.sportybet.android:id/bet_history_btn").click()
                    logging.info("goto bet history page")
                    time.sleep(3)

                    # bet history
                    el_bet_item = self.find("com.sportybet.android:id/r_bet_root")
                    el_bet_stake = el_bet_item.find_element_by_id(
                        "com.sportybet.android:id/r_bet_total_stake_value"
                    )
                    bet_stake = el_bet_stake.text
                    self.check_equal(bet_stake, pay, "quickbet_stake")
                    el_bet_item.click()
                    logging.info("goto ticket detail page")
                    time.sleep(0.4)
                    ticket_stake = self.get_text_by_id(
                        "com.sportybet.android:id/td_ticket_stake_value"
                    )
                    self.check_equal(pay, ticket_stake, "quickbet_ticket_stake")
                    ticket_odds = self.get_text_by_id(
                        "com.sportybet.android:id/td_ticket_total_odds_value"
                    )
                    ticket_odds = float(ticket_odds)
                    self.check_equal(odds, ticket_odds, "quickbet_ticket_odds")
                    ticket_pot_win = self.get_text_by_id(
                        "com.sportybet.android:id/td_ticket_pot_win_value"
                    )
                    self.check_equal(pot_win_quickbet, ticket_pot_win,
                                     "quickbet_ticket_pot_win")
                    self.find("com.sportybet.android:id/td_ticket_bet_detail").click()
                    logging.info("goto bet detail page")
                    time.sleep(0.4)
                    bet_detail_stake = self.get_text_by_id(
                        "com.sportybet.android:id/bet_detail_total_stake_value"
                    )
                    self.check_equal(pay, bet_detail_stake, "bet_detail_stake")
                    bet_detail_odds = self.get_text_by_id(
                        "com.sportybet.android:id/bet_detail_odds_value"
                    )
                    bet_detail_odds = float(bet_detail_odds)
                    self.check_equal(odds, bet_detail_odds, "bet_detail_odds")
                    bet_details_pot_win = self.get_text_by_id(
                        "com.sportybet.android:id/bet_detail_pot_win_value"
                    )
                    self.check_equal(pot_win_quickbet, bet_details_pot_win,
                                     "bet_detail_pot_win")
                    self.back().wait(1).back().wait(1).back().wait(1)
                    logging.info("back to game detail page")
            source_old = self.driver.page_source
            try:
                self.swipe_element(el_market_name, el_top, 1000)
                logging.info("swipe up to see more market")
                self.wait(2)
            except NoSuchElementException:
                pass            
            source = self.driver.page_source
            if(source_old == source):
                # next group
                tabs = self.driver.find_elements_by_class_name(
                    "android.support.v7.app.ActionBar$Tab"
                )
                for i in range(len(tabs)):
                    if(tabs[i].is_selected()):
                        if(i >= len(tabs) - 1):
                            is_end = True
                            logging.info("no more market in this game")
                        else:
                            tabs[i+1].click()
                            logging.info("select next market group")
                            time.sleep(1)
                            self.back_to_top()
                            break
        return self

    def quickbet_sport_detail_new(self):
        """
        from: sport detail page
        to: sport detail page
        """
        el_market_tab = self.find("com.sportybet.android:id/market_tab")
        el_top = self.find("com.sportybet.android:id/title_container")
        self.swipe_element(el_market_tab, el_top, 2000)
        el_market_tab = self.find("com.sportybet.android:id/market_tab")
        is_end = False # dont have more market groups
        self.expand_all_markets()
        while not is_end:
            # find all outcome
            el_buttons = self.driver.find_elements_by_class_name(
                "android.widget.ToggleButton"
            )
            el_outcomes = []
            for el_button in el_buttons:
                try:
                    odds = float(el_button.text)
                except Exception:
                    continue
                resource_id = el_button.get_attribute("resourceId")
                if(resource_id == "com.sportybet.android:id/btn1"):
                    continue
                el_outcomes.append(el_button)
            
            for el_outcome in el_outcomes:
                time.sleep(1.5)
                try:
                    odds = float(el_outcome.text)
                except Exception:
                    # if text is not odds, skip
                    continue
                el_outcome.click()
                logging.info("select outcome, odds: {}".format(odds))
                try:
                    el_quickbet_odds = self.find(
                        "com.sportybet.android:id/match_odds"
                    )
                except NoSuchElementException:
                    # if clicked betslip by mistake
                    el_betslip_title = self.find_element_by_id_and_text(
                        "com.sportybet.android:id/title", "Betslip"
                    )
                    if(el_betslip_title is not None):
                        self.back().wait(1)
                        continue
                    # if unavailable/suspended
                    self.find("com.sportybet.android:id/delete").click()
                    continue
                odds_quickbet = float(el_quickbet_odds.text)
                if(not self.check_equal(odds_quickbet, odds, "quickbet_odds")):
                    el_outcome.click()
                    continue
                el_pot_win = self.find("com.sportybet.android:id/pot_win_value")
                pot_win_quickbet = el_pot_win.text
                self.find("com.sportybet.android:id/place_bet_btn").click()
                logging.info("click quickbet placebet btn")
                el_pay = self.find("com.sportybet.android:id/payValue")
                pay = el_pay.text[5:]
                self.find("com.sportybet.android:id/confirm").click()
                logging.info("click confirm btn")
                time.sleep(1)
                # success page
                el_suc_title = self.find_element_by_id_and_text(
                    "com.sportybet.android:id/textView4",
                    "Submission Successful!"
                )
                if(el_suc_title is None):
                    # not in success page, why?
                    el_btn_ok = self.find_element_by_id_and_text(
                        "android:id/button1", "OK"
                    )
                    if(el_btn_ok is not None):
                        ###
                        self.mark_err(
                            "error when bet, check screen for more info",
                            "err_when_bet"
                        )
                        el_btn_ok.click()
                        time.sleep(1)
                        el_outcome.click()
                        logging.info("remove outcome from quick_betslip")
                        logging.info("wait for 50s.")
                        self.wait(50)
                        continue
                stake_suc = self.get_text_by_id(
                    "com.sportybet.android:id/total_stake_value"
                )
                self.check_equal(pay, stake_suc, "stake_suc") 
                pot_win_suc = self.get_text_by_id(
                    "com.sportybet.android:id/potwin_value"
                )
                self.check_equal(pot_win_suc, pot_win_quickbet, "pot_win_suc")
                self.find("com.sportybet.android:id/bet_history_btn").click()
                logging.info("goto bet history page")
                time.sleep(3)

                # bet history
                el_bet_item = self.find("com.sportybet.android:id/r_bet_root")
                el_bet_stake = el_bet_item.find_element_by_id(
                    "com.sportybet.android:id/r_bet_total_stake_value"
                )
                bet_stake = el_bet_stake.text
                self.check_equal(bet_stake, pay, "quickbet_stake")
                el_bet_item.click()
                logging.info("goto ticket detail page")
                time.sleep(0.4)
                ticket_stake = self.get_text_by_id(
                    "com.sportybet.android:id/td_ticket_stake_value"
                )
                self.check_equal(pay, ticket_stake, "quickbet_ticket_stake")
                ticket_odds = self.get_text_by_id(
                    "com.sportybet.android:id/td_ticket_total_odds_value"
                )
                ticket_odds = float(ticket_odds)
                self.check_equal(odds, ticket_odds, "quickbet_ticket_odds")
                ticket_pot_win = self.get_text_by_id(
                    "com.sportybet.android:id/td_ticket_pot_win_value"
                )
                self.check_equal(pot_win_quickbet, ticket_pot_win,
                                    "quickbet_ticket_pot_win")
                self.find("com.sportybet.android:id/td_ticket_bet_detail").click()
                logging.info("goto bet detail page")
                time.sleep(0.4)
                bet_detail_stake = self.get_text_by_id(
                    "com.sportybet.android:id/bet_detail_total_stake_value"
                )
                self.check_equal(pay, bet_detail_stake, "bet_detail_stake")
                bet_detail_odds = self.get_text_by_id(
                    "com.sportybet.android:id/bet_detail_odds_value"
                )
                bet_detail_odds = float(bet_detail_odds)
                self.check_equal(odds, bet_detail_odds, "bet_detail_odds")
                bet_details_pot_win = self.get_text_by_id(
                    "com.sportybet.android:id/bet_detail_pot_win_value"
                )
                self.check_equal(pot_win_quickbet, bet_details_pot_win,
                                    "bet_detail_pot_win")
                self.back().wait(1).back().wait(1).back().wait(1)
                logging.info("back to game detail page")

            # check page end
            source_old = self.driver.page_source
            if(el_outcomes):
                self.swipe_element(el_outcomes[-1], el_market_tab, 2000)
                logging.info("swipe up to see more market")
            self.wait(2)
            source = self.driver.page_source
            if(source_old == source):
                # next group
                tabs = self.driver.find_elements_by_class_name(
                    "android.support.v7.app.ActionBar$Tab"
                )
                for i in range(len(tabs)):
                    if(tabs[i].is_selected()):
                        if(i >= len(tabs) - 1):
                            is_end = True
                            logging.info("no more market in this game")
                            return self
                        else:
                            # next group
                            tabs[i+1].click()
                            is_expanded = False
                            logging.info("select next market group")
                            time.sleep(2)
                            self.back_to_top().back_to_top()
                            self.expand_all_markets()
                            el_market_tab = self.find("com.sportybet.android:id/market_tab")
                            el_top = self.find("com.sportybet.android:id/title_container")
                            self.swipe_element(el_market_tab, el_top, 2000)
                            el_market_tab = self.find("com.sportybet.android:id/market_tab")
                            break

    def expand_all_markets(self):
        """
        from: sport detail page
        to: sport detail page
        """
        el_market_tab = self.find("com.sportybet.android:id/market_tab")
        el_top = self.find("com.sportybet.android:id/title_container")
        self.swipe_element(el_market_tab, el_top, 2000)
        time.sleep(2)
        el_market_tab = self.find("com.sportybet.android:id/market_tab")

        is_page_end = False
        while not is_page_end:
            time.sleep(2)
            el_markets = self.driver.find_elements_by_id(
                "com.sportybet.android:id/root_container"
            )
            markets_num = len(el_markets)
            for i in range(markets_num - 1):
                el_markets = self.driver.find_elements_by_id(
                    "com.sportybet.android:id/root_container"
                )
                if(i >= len(el_markets)):
                    break
                el_market_titles = el_markets[i].find_elements_by_id(
                    "com.sportybet.android:id/title"
                )
                if((not el_market_titles) or 
                    not self.element_contains(el_markets[i], el_market_titles[0])
                ):
                    # title is hidden above the window
                    continue
                el_outcomes = el_markets[i].find_elements_by_class_name(
                    "android.widget.ToggleButton"
                )
                #`el.find` method has some problem, cannot find child correctly.
                # may find outcomes that doesnt belong to this market
                # check if el_markets[i] contains outcome
                if((not el_outcomes) or 
                   (not self.element_contains(el_markets[i], el_outcomes[0]))
                ):
                    el_market_titles[0].click()

            source_old = self.driver.page_source
            el_outcomes = self.driver.find_elements_by_class_name(
                "android.widget.ToggleButton"
            )
            if(not el_outcomes):
                self.back_to_top().back_to_top()
                return self
            self.swipe_element(el_outcomes[-1], el_market_tab, 2000)
            time.sleep(2)
            source = self.driver.page_source
            if(source_old == source):
                el_outcomes_after_swipe = self.driver.find_elements_by_class_name(
                    "android.widget.ToggleButton"
                )
                if(el_outcomes_after_swipe and 
                    el_outcomes_after_swipe[0].location == el_outcomes[0].location 
                ):
                    is_page_end = True
                    self.back_to_top().back_to_top()
                    return self
    
    def fold_and_expand_markets(self):
        """
        from: sport detail page
        to: sport detail page
        if folded then expand
        if expand then folded
        """
        el_market_tab = self.find("com.sportybet.android:id/market_tab")
        el_top = self.find("com.sportybet.android:id/title_container")
        self.swipe_element(el_market_tab, el_top, 2000)
        el_market_tab = self.find("com.sportybet.android:id/market_tab")

        is_end = False
        while not is_end:
            el_markets = self.driver.find_elements_by_id(
                "com.sportybet.android:id/root_container"
            )
            markets_num = len(el_markets)
            for i in range(markets_num - 1):
                el_markets = self.driver.find_elements_by_id(
                    "com.sportybet.android:id/root_container"
                )
                if(i >= len(el_markets)):
                    break
                el_market_titles = el_markets[i].find_elements_by_id(
                    "com.sportybet.android:id/title"
                )
                if(not el_market_titles):
                    continue
                el_outcomes = el_markets[i].find_elements_by_class_name(
                    "android.widget.ToggleButton"
                )
                # check if el_markets[i] contains outcome
                if(not el_outcomes):
                    el_market_titles[0].click()
            source_old = self.driver.page_source
            el_outcomes = self.driver.find_elements_by_class_name(
                "android.widget.ToggleButton"
            )
            self.swipe_element(el_outcomes[-1], el_market_tab, 2000)
            source = self.driver.page_source
            if(source_old == source):
                is_end = True
                self.back_to_top().back_to_top()
                return self


    def walk_betslip(self):
        """
        from: home (no outcome selected)
        to: home
        """
        logging.info("---- walk_betslip begin")
        # singles
        logging.info("walk singles")
        balance = self.get_text_by_id("com.sportybet.android:id/login")[5:]
        balance = float(balance.replace(",", ""))
        self.from_home_to_football_list()
        els_home = self.driver.find_elements_by_id(
            "com.sportybet.android:id/o1"
        )
        els_draw = self.driver.find_elements_by_id(
            "com.sportybet.android:id/o2"
        )
        els_away = self.driver.find_elements_by_id(
            "com.sportybet.android:id/o3"
        )
        odds = []
        for el_home in els_home:
            el_home.click()
            odds.append(el_home.text)
            time.sleep(0.3)
        logging.info("{} outcomes selected".format(len(els_home)))
        self.find("com.sportybet.android:id/betslip_btn_layout_id").click()
        logging.info("goto betslip")
        time.sleep(2)
        self.accept_changes()
        self.find("com.sportybet.android:id/match_outcome_desc")
        self.swipe_up()
        self.find("com.sportybet.android:id/singles").click()
        logging.info("goto singles tab")
        el_stake_edit = self.find("com.sportybet.android:id/edit_text_ksh")
        el_stake_edit.click()
        logging.info("click stake input box")
        self.set_stake(self.min_stake + 1)
        self.swipe_up()
        total_stake = self.get_text_by_id(
            "com.sportybet.android:id/singles_total_stake"
        ).replace(",", "")
        total_stake = float(total_stake)
        
        pot_win = self.get_text_by_id("com.sportybet.android:id/win")
        pot_win = int(float(pot_win.split("~")[-1]))
        self.walk_palcebet(total_stake, pot_win)
        self.back().wait(0.5).back().wait(3)
        logging.info("goto home page")
        balance_new = self.get_text_by_id("com.sportybet.android:id/login")[5:]
        balance_new = float(balance_new.replace(",", ""))
        self.check_equal(balance, balance_new + total_stake, "balance")
        balance = balance_new

        # multiple
        logging.info("walk multiple")
        self.from_home_to_football_list()
        odds.clear()
        els_home = self.driver.find_elements_by_id(
            "com.sportybet.android:id/o1"
        )
        els_draw = self.driver.find_elements_by_id(
            "com.sportybet.android:id/o2"
        )
        for el_home in els_home:
            el_home.click()
            odds.append(el_home.text)
            time.sleep(0.3)
        for el_draw in els_draw:
            el_draw.click()
            odds.append(el_draw.text)
            time.sleep(0.3)
        logging.info("{} outcomes selected".format(len(els_home) + len(els_draw)))
        self.find("com.sportybet.android:id/betslip_btn_layout_id").click()
        logging.info("open betslip")
        time.sleep(2)
        self.accept_changes()
        self.find("com.sportybet.android:id/match_outcome_desc")
        self.swipe_up()
        self.find("com.sportybet.android:id/multiple").click()
        logging.info("goto multiple")
        try:
            self.find("com.sportybet.android:id/close_flexibet").click()
            logging.info("close flexibet tips")
        except NoSuchElementException:
            pass
        el_stake_edit = self.find("com.sportybet.android:id/edit_text_ksh")
        el_stake_edit.click()
        logging.info("click stake input box")
        self.set_stake(self.min_stake*11)
        self.swipe_up()
        total_stake = self.get_float_by_id(
            "com.sportybet.android:id/m_total_stake"
        )
        total_stake = float(total_stake)
        total_odds = self.get_text_by_id(
            "com.sportybet.android:id/multiple_total_odds"
        ).split("~")[-1].replace(",", "")
        total_odds = float(total_odds)
        bonus = self.get_float_by_id("com.sportybet.android:id/bonus")
        bonus = int(bonus)
        pot_win = self.get_text_by_id(
            "com.sportybet.android:id/win"
        ).split("~")[-1].replace(",", "")
        pot_win = int(float(pot_win))
        self.walk_palcebet(total_stake, pot_win, bonus)
        self.back().wait(0.5).back().wait(3)
        logging.info("goto home page")
        balance_new = self.get_text_by_id("com.sportybet.android:id/login")[5:]
        balance_new = float(balance_new.replace(",", ""))
        self.check_equal(balance, balance_new + total_stake, "balance")
        balance = balance_new

        # flexibet
        logging.info("walk flexibet")
        self.from_home_to_football_list()
        els_home = self.driver.find_elements_by_id(
            "com.sportybet.android:id/o1"
        )
        odds.clear()
        for el_home in els_home:
            el_home.click()
            odds.append(el_home.text)
            time.sleep(0.3)
        logging.info("{} outcomes selected".format(len(els_home)))
        self.swipe_up()
        els_home = self.driver.find_elements_by_id(
            "com.sportybet.android:id/o1"
        )
        for el_home in els_home:
            checked = el_home.get_attribute("checked")
            if(checked == "false"):
                el_home.click()
                logging.info("1 more outcome selected")
                odds.append(el_home.text)
                time.sleep(0.3)
        self.back_to_top()
        self.find("com.sportybet.android:id/betslip_btn_layout_id").click()
        logging.info("open betslip")
        time.sleep(2)
        self.accept_changes()
        self.find("com.sportybet.android:id/match_outcome_desc")
        self.swipe_up()
        self.find("com.sportybet.android:id/multiple").click()
        logging.info("goto multiple tab")
        try:
            self.find("com.sportybet.android:id/close_flexibet").click()
            logging.info("close flexibet tips")
        except NoSuchElementException:
            pass
        el_stake_edit = self.find("com.sportybet.android:id/edit_text_ksh")
        el_stake_edit.click()
        logging.info("click stake input box")
        total_stake = self.min_stake * 12
        self.set_stake(total_stake)
        try:
            self.find("com.sportybet.android:id/arrow_down").click()
            logging.info("click flexibet arrow_down")
            time.sleep(0.5)
        except NoSuchElementException:
            pass
        self.swipe_up()      
        total_odds = self.get_text_by_id(
            "com.sportybet.android:id/multiple_total_odds"
        ).split("~")[-1].replace(",", "")
        total_odds = float(total_odds)
        bonus = self.get_float_by_id("com.sportybet.android:id/bonus")
        bonus = int(bonus)
        pot_win = self.get_text_by_id(
            "com.sportybet.android:id/win"
        ).split("~")[-1].replace(",", "")
        pot_win = int(float(pot_win))
        self.walk_palcebet(total_stake, pot_win, bonus)
        self.back().wait(0.5).back().wait(3)
        logging.info("goto home page")
        balance_new = self.get_text_by_id("com.sportybet.android:id/login")[5:]
        balance_new = float(balance_new.replace(",", ""))
        self.check_equal(balance, balance_new + total_stake, "balance")
        balance = balance_new

        # system
        logging.info("walk system")
        self.from_home_to_football_list()
        els_home = self.driver.find_elements_by_id(
            "com.sportybet.android:id/o1"
        )
        els_draw = self.driver.find_elements_by_id(
            "com.sportybet.android:id/o2"
        )
        odds.clear()
        for el_home in els_home:
            el_home.click()
            odds.append(el_home.text)
            time.sleep(0.3)
        for el_draw in els_draw:
            el_draw.click()
            odds.append(el_draw.text)
            time.sleep(0.3)
        self.find("com.sportybet.android:id/betslip_btn_layout_id").click()
        logging.info("open betslip")
        time.sleep(2)
        self.accept_changes()
        self.find("com.sportybet.android:id/match_outcome_desc")
        self.swipe_up()
        self.find("com.sportybet.android:id/system").click()
        logging.info("goto system tab")
        total_stake = self.get_float_by_id(
            "com.sportybet.android:id/system_total_stake"
        )
        total_stake = float(total_stake)
        bonus = self.get_float_by_id("com.sportybet.android:id/bonus")
        bonus = int(bonus)
        pot_win = self.get_text_by_id(
            "com.sportybet.android:id/win"
        ).split("~")[-1].replace(",", "")
        pot_win = int(float(pot_win))
        self.walk_palcebet(total_stake, pot_win, bonus)
        self.back().wait(0.5).back().wait(3)
        logging.info("goto home page")
        balance_new = self.get_text_by_id("com.sportybet.android:id/login")[5:]
        balance_new = float(balance_new.replace(",", ""))
        self.check_equal(balance, balance_new + total_stake, "balance")
        balance = balance_new
        logging.info("---- walk_betslip over")
        return self

    def walk_palcebet(self, total_stake, pot_win, bonus=0):
        """
        from: betslip
        to: page before betslip
        """
        pay = self.get_text_by_id(
            "com.sportybet.android:id/place_bet_btn"
        ).split(":")[-1].strip().replace(",", "")
        pay = float(pay)
        self.check_equal(total_stake, pay, "total_stake_pay")
        self.find("com.sportybet.android:id/place_bet_btn").click()
        logging.info("click place bet btn")
        pay_confirm = self.get_text_by_id(
            "com.sportybet.android:id/payValue"
        )[5:].replace(",", "")
        pay_confirm = float(pay_confirm)
        self.check_equal(total_stake, pay_confirm, "total_stake_pay_confirm")
        time.sleep(0.1)
        self.find("com.sportybet.android:id/confirm").click()
        logging.info("click confirm btn")
        time.sleep(1)
        
        # success page
        total_stake_suc = self.get_text_by_id(
            "com.sportybet.android:id/total_stake_value"
        ).replace(",", "")
        total_stake_suc = float(total_stake_suc)
        self.check_equal(total_stake, total_stake_suc, "total_stake_success_page")
        pot_win_suc = self.get_float_by_id("com.sportybet.android:id/potwin_value")
        pot_win_suc = int(float(pot_win_suc))
        self.check_equal(pot_win, pot_win_suc, "pot_win_suc")
        self.find("com.sportybet.android:id/bet_history_btn").click()
        logging.info("goto bet_hisory page")
        time.sleep(1)

        # bet history
        el_bet_item = self.find("com.sportybet.android:id/r_bet_root")
        el_stake_history = el_bet_item.find_element_by_id(
            "com.sportybet.android:id/r_bet_total_stake_value"
        )
        stake_history = float(el_stake_history.text.replace(",",""))
        self.check_equal(total_stake, stake_history, "total_stake_history")
        el_bet_item.click()
        logging.info("goto ticket details page")
        time.sleep(0.4)
        stake_ticket = self.get_float_by_id(
            "com.sportybet.android:id/td_ticket_stake_value"
        )
        self.check_equal(total_stake, stake_ticket, "stake_ticket")
        ticket_odds = self.get_float_by_id(
            "com.sportybet.android:id/td_ticket_total_odds_value"
        )
        pot_win_ticket = self.get_float_by_id(
            "com.sportybet.android:id/td_ticket_pot_win_value"
        )
        pot_win_ticket = int(pot_win_ticket)
        self.check_equal(pot_win, pot_win_ticket, "pot_win_ticket")
        if(bonus != 0):
            try:
                ticket_bonus = self.get_float_by_id(
                    "com.sportybet.android:id/td_ticket_bonus_value"
                )
                ticket_bonus = int(ticket_bonus)
                self.check_equal(ticket_bonus, bonus, "bonus")    
            except NoSuchElementException:
                pass
        # back
        self.back().wait(1).back().wait(1)
        logging.info("goto the page before betslip")
        return self

    def check_equal(self, v1, v2, screen_name):
        """
        if v1 != v2, take screen.
        """
        result = (v1 == v2)
        if(result):
            logging.info("success: check_equal: {}: {}, {}".format(
                screen_name, v1, v2)
            )
        else:
            self.take_screen("check_equal_{}".format(screen_name))
            logging.error("failed: check_equal: {}: {}, {}".format(
                screen_name, v1, v2)
            )
        return result
    
    def mark_err(self, msg, screen_name):
        """
        """
        logging.error(msg)
        self.take_screen(screen_name)

    def from_home_to_football_list(self):
        self.find_quick_entry("Sports").click()
        logging.info("goto sports page")
        self.find_element_by_id_and_text(
                "com.sportybet.android:id/tab_name", "Football"
        ).click()
        time.sleep(1)
        self.find_element_by_id_and_text(
            "com.sportybet.android:id/item_text_view", "All Football"
        ).click()
        logging.info("goto football list page")
        time.sleep(1)
        return self

    def accept_changes(self, turn_on=True):
        """
        Turn on or Turn off ACCEPT_CHANGES switch. 
        if not in betlsip, do nothing.
        """
        action = "turn on" if turn_on else "turn off"
        try:
            el_switch = self.find("com.sportybet.android:id/auto_change_switch")
            checked = el_switch.get_attribute("checked")
            if(checked == "true"):
                checked = True
            else:
                checked = False
            logging.info(
                "accept_changes is {}".format("on" if checked else "off")
            )
            if(checked != turn_on):
                el_switch.click()
                logging.info("{} accept_changes".format(action))
        except NoSuchElementException:
            pass
        return self

if __name__ == '__main__':
    country = "ng"
    try:
        w = Walk(screen_folder="d:\\quicktest", country=country)
        w.wait(15).try_close_ads().set_country(country).wait(5).try_close_ads().login().walk_quickbet()
        # w.wait(10).try_close_ads().set_country("ke").try_close_ads().login().walk_betslip()
    except Exception as err:
        print(traceback.format_exc())
        w.take_screen("err")
    