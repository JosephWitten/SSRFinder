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

def printArray(array):
    for i in array:
        print(i)

def getSource(currentDomain):
    r = requests.get(currentDomain)
    return (r.text)
    

def getHref(html):
    #Split big html block into tags *kind of*
    html = html.replace("\n", "").replace("\r", "").replace(" ", "")
    lineArray = html.split(">")
    for i in range(0, len(lineArray)):
        #print(lineArray)

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
                temp = result.split("=")

                if (domain in temp[0]):

                    #check if already found
                    if (result not in foundURLs):
                        foundURLs.append(result)

                #Remember out of scope links   
                else:
                    if(result not in outOfScope):
                        outOfScope.append(result)
                        if (pipeMode == False):
                            print("URL found that did not contain original domain, could be out of scope : " + result)
            else:
                if(result not in outOfScope):
                    outOfScope.append(result)
                    if (pipeMode == False):
                        print("URL found that did not contain original domain, could be out of scope : " + result)


html = getSource(OGdomain)
getHref(html)




def sortURLs():
    count = 0
    if (pipeMode == False):
        print("sorting URLs")
    for i in range(0, len(foundURLs)):
        count = count + 1
        if (foundURLs[i].count("http") > 1):
            if (pipeMode == False):
                print("potentially interesting URL found : " + foundURLs[i])
            else:
                print(foundURLs[i])
            interestingURLs.append(foundURLs[i])
    if(count != 0):
        print("no interesting URLs")

def main():
    if (len(foundURLs) < 1):
        print("No URLs we're found, either this is a bug or the page may not have any links")
        sys.exit(1)
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
    print(interestingURLs)



try:
    main()
except KeyboardInterrupt:
    if (pipeMode == False):
        print("Keyboard interruptd")
    #print(foundURLs)
    #print(outOfScope)
    sortURLs()
