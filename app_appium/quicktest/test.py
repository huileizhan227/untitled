from walk import Walk
w = Walk(screen_folder="d:\\quicktest")
w.wait(10)
w.find_quick_entry("Sports").click()
w.find_element_by_id_and_text("com.sportybet.android:id/item_text_view", "All Football").click()
w.find("com.sportybet.android:id/home_team").click()

el_container = w.find("com.sportybet.android:id/event_recycler")
el_market_containers = el_container.find_elements_by_class_name(
    "android.widget.LinearLayout"
)

for el_market_container in el_market_containers:
    if(el_market_container.location["x"] > 0):
        continue
    el_market_name = []
    el_market_name = el_market_container.find_elements_by_id(
        "com.sportybet.android:id/title"
    )
    if(el_market_name):
        print(el_market_container.location)
        print(el_market_name[0].text)
