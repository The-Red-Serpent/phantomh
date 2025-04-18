import os
import sys
import stem
import time
import json
import requests
import platform
import pyfiglet
import subprocess
from stem import Signal
from rich.text import Text
from rich.console import Console
from stem.control import Controller
sys.stdout.reconfigure(encoding='utf-8')

def check_sys_type():
    print("[+] Checking for System Type.....")
    if os.name=="nt" and platform.system()=="Windows":
        print("This is a Windows System")
    elif os.name=="posix" and platform.system()=="Linux":
        print("This is a Linux System")
    else:
        print("Unknown System Type This Script Can Only Run on Windows and Linux Halting the Program......")
        sys.exit(1)


# you can check if a service is running using the 
# subprocess module to execute shell commands and capture the output.
def is_service_running():
    print("[+]Making sure tor service is running.......")
    if os.name=="posix" and platform.system()=="Linux":
        try:

            check_tor = subprocess.check_output('which tor', shell=True)
        except subprocess.CalledProcessError:

            print('[+] tor is not installed !')
            subprocess.check_output('sudo apt update',shell=True)
            subprocess.check_output('sudo apt install tor -y',shell=True)
            print('[!] tor is installed succesfully ')
        
    else:
        try:
            result = subprocess.run(['tasklist', '/v'], stdout=subprocess.PIPE, text=True)
            if 'tor.exe' in result.stdout.lower():  # Case-insensitive check
            # Use regex to ensure we match the exact process name "tor.exe"
                if subprocess.run(['findstr', '/r', r'\<tor\.exe\>'], input=result.stdout, text=True, stdout=subprocess.PIPE).stdout:
                    return True  # Tor process is running
            return False  # Tor process is not running
        except Exception as e:
            print(f"[-] Error occurred while checking Tor process on Windows: {e}")
            return False
        
# SOCKS5 is a type of proxy that allows for the forwarding of network packets, typically used for 
# routing traffic through proxies to conceal the source IP address.
def enable_tor_proxy():
    os.environ["http_proxy"] = "socks5h://127.0.0.1:9050"
    os.environ["https_proxy"] = "socks5h://127.0.0.1:9050"
    print("[+] Enabled tor Proxies Successfully..........." )

def rotate_ip_addresses():
    try:
        with Controller.from_port(port=9051) as Connection:
            Connection.authenticate(password="hello")
            try:
                Connection.signal(Signal.NEWNYM)  # Request a new IP
                print("New IP requested")
                time.sleep(20)
            except stem.ControllerError as E:
                print(f"Can't connect: {E}")
    except ConnectionRefusedError as e:
        # Handle connection errors (e.g., Tor is not running, or control port is blocked)
        print(f"Connection error: {e}")

import requests
import json

def get_public_ip_and_geo_location():
    ip_address = ""
    try:
        # Fetch the public IP address
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            ip_address = response.text
            print(f"Your Current IP Address is: {ip_address}")
        else:
            print("Error: Unable to fetch IP address.")
            return
        
        # Fetch geolocation information using the public IP address
        geo_response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        
        if geo_response.status_code == 200:
            # Parse the response as JSON
            data = geo_response.json()

            # Extract the location data
            country = data.get('country_name', 'Not found')
            city = data.get('city', 'Not found')
            region = data.get('region', 'Not found')
            country_code = data.get('country_code', 'Not found')
            latitude = data.get('latitude', 'Not found')
            longitude = data.get('longitude', 'Not found')

            # Print the location data
            print(f"IP Address: {ip_address}")
            print(f"Country: {country}")
            print(f"Region: {region}")
            print(f"City: {city}")
            print(f"Country Code: {country_code}")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
        else:
            print(f"Error: Unable to fetch geolocation for IP {ip_address}. Status code: {response.status_code}")
    
    except requests.RequestException as e:
        print(f"Error fetching geolocation data: {e}")

        


def main():
    
    console = Console()
    #ascii_art = pyfiglet.figlet_format("Tor Spoof", font="slant")
    ascii_banner='''
                                                                                                                                    ......                                                      
                              .:-=+**#############**+=-:.                                           
                         .-=*#############################+=:.                                      
                      -+######################################*=:                                   
                   -+#############################################+:                                
                :+###################################################=.                             
              -*#######################################################+:                           
            :*#########################*++=---::::::--==+*###############*:                         
          .*####################*+-:.                      .:=+############+.                       
         =###################=:      .::-==+***######**++=-.    :+###########-                      
        *##################=.   .-+*#*=-::..        ...:-=*##*=:   -*#########+                     
      .*#################+.  .-*###+                        :=###+:  -#########*                    
     .################*=. .-*#####+                            -*##*: .*########*.                  
    .#############*+-. :=*+-.  ...             ..::::::::.       -###+  +########*                  
    *#########+-:  :-==-.              .-=====--::..::::::::::..  .*##*. *########+                 
   =#######=. .-==-: .::-=++******+:   .:  .-=++*############*+=:   +##*..#########-                
  .######*  =*-.:::=##########*++*##    :*########################*- +##* =#########                
  =######* =#:-#+=:.=######*-:=###*#.   #############################-*##-.##*######-               
  ########+:.+*###*+++###*:.+#####-#   =####***+++===---::-=+*########*### ##+######*               
 :##########+-.+########= :######+==   ###################*+-:.:=*########:*#+*######               
 -#############*#######: -######*.#.  =########################+: :*######=*#*=######.              
 -###################+. =######*.==   ###########################*. -#####+##*:######:              
 -##################-  -####*=-:-*   :#############################: :####*##*:######:              
 :################+.  -######====   .*##############################  =######=:######.              
 .##############=.   =########+=--=*################################- .######:-######               
  *#######*+=-.    .+###############################################-  #####* +#####+               
  -########***+-..=#################################################. :#####:.######:               
   *######*+==-+*##############################################++##:  +####= +#####+                
   :#######################################################*=-=*#*.  -####= :######.                
    =##################################################*=:.-+##*-   =####= .######-                 
     +############################################+=-. .-*###+:   -*###*: .######=                  
      +####################################*+=-:   :-+####+-   .-*####=  :######=                   
       =##############################=-:.    :-+*####+-.    -+#####=   =######-                    
        -############################:  :-=+#####*=-.    .=*######:   :*#####*:                     
         .+#########################**#####*=-:.     .-+#########+  .+######+                       
           :*#####################**+=-:.       .:=*#############..+######*:                        
             -#################*.          .:=+##################*######*-                          
               -*#############-      .:-=*############################*:                            
                 :+#########+. .:-+*################################=.                              
                    :+######*###################################*=:                                 
                       .-+###################################+-.                                    
                           .-=+*#######################*+=:.                                        
'''
    console = Console()
    console.print(ascii_banner, style="bold red")
    text = Text()
    text.append("Author:", style="bold green") 
    text.append("The_Red_Serpent", style="bold red")
    console.print(text)
    check_sys_type()
    if is_service_running():
        print("Tor Service is Running")
    else:
        print("Tor Service is not running. Pls Enable it")
        sys.exit(1)
    print("[+] Enabling  tor proxy........................" )
    enable_tor_proxy()
    print("entering a infinte loop of IP rotation")
    while(True):
        try: 
            get_public_ip_and_geo_location()
            rotate_ip_addresses()
            
        except KeyboardInterrupt:
            print("exiting the program")
            sys.exit(0)

if __name__ == "__main__":
    main()
