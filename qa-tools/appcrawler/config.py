APPIUM_MAIN = r'C:\Users\jiayongchao.000\AppData\Roaming\npm\node_modules\appium\build\lib\main.js'

def get_countries(pkg_name):
    tail = pkg_name.split('.')[-1]
    if tail == 'common':
        countries = [
            'Tanzania | English',
            'Tanzania | Swahili',
            'DR Congo | Français',
            'ليبيا'
        ]
    elif tail == 'more':
        countries = [
            'Nigeria',
            'Kenya | Swahili',
            'مصر',
            "Côte d'Ivoire"
        ]
    else:
        countries = [None,]
    return countries
