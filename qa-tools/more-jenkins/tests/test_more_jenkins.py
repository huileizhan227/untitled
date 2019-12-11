from more_jenkins import Jenkins
from more_jenkins import master
from more_jenkins import dev

def test_get_all_apk_links():
    # master.request()
    links = master.get_all_apk_links()
    print(links)
    links = dev.get_all_apk_links()
    print(links)
    master.request_stable()
    dev.request_stable()
    links = master.get_all_apk_links()
    print(links)
    assert links
    links = dev.get_all_apk_links()
    print(links)
    assert links
    
def test_get_apk_link():
    # master.request()
    master.get_apk_link()
    dev.get_apk_link()
    master.request_stable()
    link = master.get_apk_link()
    print(link)
    assert link
    dev.request_stable()
    link = dev.get_apk_link()
    print(link)
    assert link
