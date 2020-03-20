#!/usr/bin/python3  

import urllib.request

# reference url for an item that is available
# url = 'https://www.carlroth.com/de/de/buersten-reinigungsschwaemme/reinigungsbuerste-rotilabo/p/xk76.1'

# desired url of an item that is currently not available
url = 'https://www.carlroth.com/de/de/loesungen-fuer-die-gram-faerbung/ethanol-96-%25-vergaellt/p/t171.4'

# if this string is in the html body, the item is unavailable
target = '<divclass="stock-container"><spanclass="stockstock--X"></span>Nichtverf'

html = urllib.request.urlopen(url).read()

# remove newline and whitespace
html = str(html).replace(' ', '').replace('\\n', '')

if not target in html:
    print('Success!')
