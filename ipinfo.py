#!/usr/bin/env python3
"""ipinfo - Gets information about an IP from ipinfo.io's API"""
#
# (c) 2018 Alex Merkel
# @alexandermerkel
#
# See LICENSE file
#


# --------------------------------------------------------------------------- #
# IMPORTS
import sys
from ipaddress import ip_address
from urllib.parse import urlparse
import socket
import requests
import colored
# ########################################################################### #


# --------------------------------------------------------------------------- #
# VERSION
NAME = "ipinfo"
VERSION = "0.1.0"
# ########################################################################### #


# --------------------------------------------------------------------------- #
# CONSTANTS
API = "https://ipinfo.io/%/json"
HEADERS = {'User-Agent': NAME+'/'+VERSION}
BOLD = colored.attr("bold")
RESET = colored.attr("reset")
RED = colored.fg("red")
GREEN = colored.fg("green")
# ########################################################################### #


# --------------------------------------------------------------------------- #
def main(items):
    """Main function

    Args:
        items (list): List of IPs or domains for which to get infos
    """
    if items:
        for item in items:
            getInfos(item)
    else:
        while True:
            try:
                item = input("Enter IP or domain: ")
                getInfos(item)
            except KeyboardInterrupt:
                print(BOLD+"\nGoodbye..."+RESET)
                break
# ########################################################################### #


# --------------------------------------------------------------------------- #
def getInfos(item):
    """Prints infos for item (IP or URL)
    Args:
        item (string): IP or URL for witch to get infos
    """
    try:
        ip_address(item)
        getIPInfos(item)
    except ValueError:
        getDomainInfos(item)
# ########################################################################### #


# --------------------------------------------------------------------------- #
def getIPInfos(ip):
    """Prints infos of an IP
    Args:
        ip (string): The IP
    """
    url = API.replace('%', ip)
    try:
        infos = requests.get(url, headers=HEADERS, timeout=5).json()
    except Exception:
        print(BOLD+RED+"Connection error!"+RESET)
        return
    if not infos:
        print(RED+"No information found for IP "+BOLD+ip+RESET)
        return
    if infos.get("hostname"):
        print("Hostname: "+BOLD+infos.get("hostname")+RESET)
    if infos.get("org"):
        print("Organization: "+BOLD+infos.get("org")+RESET)
    if infos.get("city"):
        print("City: "+BOLD+infos.get("city")+RESET)
    if infos.get("region"):
        print("Region: "+BOLD+infos.get("region")+RESET)
    if infos.get("country"):
        print("Country: "+BOLD+infos.get("country")+RESET)
# ########################################################################### #


# --------------------------------------------------------------------------- #
def getDomainInfos(domain):
    """Searches A-Record of domain and if it finds one, calls getIPInfos for that IP
    Args:
        domain (string): The domain
    """
    name = urlparse(domain).netloc
    name = name.split(':')[0]
    if name:
        print("Domain: "+BOLD+name+RESET)
    else:
        name = domain
    try:
        ips = [str(i[4][0]) for i in socket.getaddrinfo(name, 80)]
    except OSError:
        print(RED+"Domain not found "+BOLD+name+RESET)
        return
    try:
        ip = ips[0]
    except IndexError:
        print(RED+"No IPs found for domain "+BOLD+domain+RESET)
        return

    print("IP: "+BOLD+ip+RESET)
    try:
        reverse = socket.gethostbyaddr(ip)[0]
        if reverse:
            print("Reverse DNS: "+BOLD+reverse+RESET)
    except (OSError, IndexError):
        pass
    getIPInfos(ip)
# ########################################################################### #


# --------------------------------------------------------------------------- #
# Default
if __name__ == "__main__":
    main(sys.argv[1:])
# ########################################################################### #
