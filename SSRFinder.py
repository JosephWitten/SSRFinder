#!/usr/bin/python
import os
import sys
import requests
import time

foundURLs = []
outOfScope = []
interestingURLs = []
blacklist = []


if("--help" in sys.argv or "-h" in sys.argv):
    print("Help page")
    print("Usage: python SSRFinder.py <DOMAIN> <OPTIONS>")
    print("--help: show this help page")
    print("-p : Pipe mode, only shows final interesting URLs, ideal for piping into a file")
    print("-b : blacklist subdomains eg, '-b www,noscope,admin,internal")
    sys.exit(1)

#Check if correct arguments
if (len(sys.argv) <= 1):
    print("Usage: python SSRFinder.py <DOMAIN> <OPTIONS>")
    print("-h for more")
    sys.exit(1)

pipeMode = False
if ("-p" in sys.argv):
    pipeMode = True

blacklistOn = False
if ("-b" in sys.argv):
    indexOfTag = sys.argv.index("-b")
    temp = sys.argv[indexOfTag + 1]
    temp = temp.split(",")
    for i in temp:
        blacklist.append(i)
    blacklistOn = True

domain = sys.argv[1]
OGdomain = "http://" + domain

def printArray(array):
    for i in array:
        print(i)

def writeToFile(newURL):
    f = open("outputOf" + domain, "a")
    f.write(newURL + "\n")
    f.close()

def getSource(currentDomain):
    try:
        r = requests.get(currentDomain)
        return (r.text)
    except requests.exceptions.Timeout:
        print("connection timed out : " + currentDomain)
        return ""
    except requests.exceptions.TooManyRedirects:
        print("to many redirects : " + currentDomain)
        return ""
    except ConnectionResetError:
        print("connection reset by peer")
        return ""
    except:
        return ""

def checkScope(foundURL):
    cont = False
    parts = foundURL.split("=")
    #Check if domain in URL (and if its in base url)
    if (domain in parts[0]):

        #Check if there is a blacklisted subdomain in base url
        cont = True
        for i in blacklist:
            if (i in parts[0]):
                cont = False
        
    if(cont):
        return foundURL
    else:
        if (foundURL not in outOfScope):
            outOfScope.append(foundURL)
            if (pipeMode == False):
                print("Found URL possibly not in scope : " + foundURL)
        return ""

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
            
            #Check scope
            inScope = checkScope(result)
            if (len(inScope) > 0 and (inScope not in foundURLs)):
                foundURLs.append(inScope)
     

html = getSource(OGdomain)
getHref(html)


def sortURLs():
    count = 0
    if (pipeMode == False):
        print("sorting URLs")
    for i in range(0, len(foundURLs)):
        if (foundURLs[i].count("http") > 1):
            if (pipeMode == False):
                print("potentially interesting URL found : " + foundURLs[i])
            else:
                print(foundURLs[i])
                if(foundURLs[i] not in interestingURLs):
                    interestingURLs.append(foundURLs[i])
            count = count + 1
            writeToFile(foundURLs[i])
    if(count == 0):
        print("no interesting URLs")

def checkURL(currentURL):
    if (currentURL.count("http" > 1)):
        print("potentially interesting URL found : " + currentURL)
    interestingURLs.append(currentURL)
    


def main():
    if (len(foundURLs) < 1):
        print("No URLs we're found, either this is a bug or the page may not have any links")
        sys.exit(1)
    i = 0
    while(i < len(foundURLs)):
        try:
            if ((i % 50 == 0) and (i != 0)):
                print("on link " + str(i) + "/" + str(len(foundURLs)))

            if (pipeMode == False):
                print("Currently on " + foundURLs[i])
            html = getSource(foundURLs[i])
            getHref(html)
            if (pipeMode == False):
                print("Currently found " + str(len(foundURLs)) + " URLs")
            i = i + 1

        except ValueError:
            i = i + 1

    print("---------")
    sortURLs()


start_time = time.time()
try:
    main()
    print("--- " + str(time.time() - start_time) + " seconds ----")
except KeyboardInterrupt:
    if (pipeMode == False):
        print("Keyboard interruptd")
    #print(foundURLs)
    #print(outOfScope)
    print("----------\n")
    sortURLs()
    print("--- " + str(time.time() - start_time) + " seconds ----")
except:
    print("----------\n")
    sortURLs()
    print("--- " + str(time.time() - start_time) + " seconds ----")