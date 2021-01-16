#!/usr/bin/python
import os
import sys
import requests
import time

foundURLs = []
outOfScope = []
interestingURLs = []

if("--help" in sys.argv or "-h" in sys.argv):
    print("Help page")
    print("Usage: python SSRFinder.py <DOMAIN> <OPTIONS>")
    print("--help: show this help page")
    print("-p : Pipe mode, only shows final interesting URLs, ideal for piping into a file")
    sys.exit(1)

#Check if correct arguments
if (len(sys.argv) <= 1):
    print("Usage: python SSRFinder.py <DOMAIN> <OPTIONS>")
    print("-h for more")
    sys.exit(1)

pipeMode = False
if ("-p" in sys.argv):
    pipeMode = True

domain = sys.argv[1]
OGdomain = "http://" + domain

def getSource(currentDomain):
    r = requests.get(currentDomain)
    return (r.text)
    

def getHref(html):
    #Split big html block into tags *kind of*
    lineArray = html.split(">")
    for i in range(0, len(lineArray)):

        #Find <a tags
        if ("<a" in lineArray[i]):
            temp = lineArray[i]
            #Yoink href link out of tag
            result = (temp[temp.find("href=\"")+len("href=\""):temp.rfind("\"")])

            #make sure link is not relative
            if (result != ""):
                if (result[0] == "/"):
                    result = OGdomain + result

            if (result.find("\"") != -1):
                result = result[:(result.find("\""))]
            
            #check if in scope
            if (domain in result):

                #check if already found
                if (result not in foundURLs):
                    foundURLs.append(result)

            #Remember out of scope links   
            else:
                if (domain not in outOfScope):
                    outOfScope.append(domain)
                    if (pipeMode == False):
                        print("URL found that did not contain original domain, could be out of scope : " + result)
                


html = getSource(OGdomain)
getHref(html)



def sortURLs():
    for i in range(0, len(foundURLs)):
        if (foundURLs[i].count("http") > 1):
            if (pipeMode == False):
                print("potentially interesting URL found : " + foundURLs[i])
            interestingURLs.append(foundURLs[i])

def main():
    i = 0
    while(i < len(foundURLs)):
        try:
            if (pipeMode == False):
                print("Currently on " + foundURLs[i])
            html = getSource(foundURLs[i])
            getHref(html)
            if (pipeMode == False):
                print("Currently found " + str(len(foundURLs)) + " URLs")
            i = i + 1
        except ValueError:
            i = i + 1
    
    sortURLs()
    for i in interestingURLs:
        print(i)
    



try:
    main()
except KeyboardInterrupt:
    if (pipeMode == False):
        print("Keyboard interruptd")
    #print(foundURLs)
    #print(outOfScope)
    sortURLs()
    for i in interestingURLs:
        print(i)