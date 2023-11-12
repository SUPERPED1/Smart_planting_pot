# import the module
import python_weather
import asyncio
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735
import socket
import re

import pyaudio #get source of the mic sound
import speech_recognition as sr #Recog the sound to text

'''
mic setup
'''
#print(sr.Microphone.list_microphone_names())
mic = sr.Microphone()
recog = sr.Recognizer()
recog.energy_threshold = 6000
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


'''
Draw LCD setup
'''
disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, width=128, height=160, rotation=90, invert=False)
WIDTH = disp.width
HEIGHT = disp.height

img = Image.new('RGB', (WIDTH, HEIGHT),(0,0,0))
draw = ImageDraw.Draw(img)

# Load default font.
font = ImageFont.load_default()
font1 = ImageFont.truetype("/home/bimu/Desktop/Project/Roboto-Black.ttf",13)
font2 = ImageFont.truetype("/home/bimu/Desktop/Project/Roboto-Black.ttf",20)
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

'''
UDP setup
'''
localPort=8888
bufferSize=1024
ip_client = ('192.168.19.21', 8888)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
def init():
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #enable broadcasting mode
    sock.bind(('', localPort))
    print("UDP server : {}:{}".format(get_ip_address(),localPort))
def get_ip_address():
    """get host ip address"""
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

'''
dataset
'''
Ascii_art_set = {
    "Cloudy":[["              "],
              ["              "],
              ["              "],
              ["              "],
              ["     _._      "],
              ["   .(   ).    "],
              ["  (  )    )_  "],
              [" (____),____) "],
              ["    (________)"],
              ["              "],
              ["              "],
              ["              "],
              ["              "],
              ["              "]],

    "Sunny":[["              "],
             ["              "],
             ["              "],
             ["              "],
             ["              "],
             ["    \   /     "],
             ["     .-.      "],
             ["  --(   )--   "],
             ["     '-'      "],
             ["    /   \     "],
             ["              "],
             ["              "],
             ["              "],
             ["              "]],

    "Light rain":[["              "],
                  ["              "],
                  ["              "],
                  ["              "],
                  ["              "],
                  ["     .-.      "],
                  ["    (   ).    "],
                  ["   (___)__)   "],
                  ["    ' ' ' '   "],
                  ["   ' ' ' '    "],
                  ["              "],
                  ["              "],
                  ["              "],
                  ["              "]],

    "Heavy rain":[["              "],
                  ["              "],
                  ["              "],
                  ["              "],
                  ["              "],
                  ["     .-.      "],
                  ["    (   ).    "],
                  ["   (___)__)   "],
                  ["   ''''''''   "],
                  ["  ''''''''    "],
                  ["              "],
                  ["              "],
                  ["              "],
                  ["              "]],

    "Partly cloudy":[["              "],
                     ["              "],
                     ["              "],
                     ["              "],
                     ["   \  /       "],
                     ["  _/\"\"\_._  "],
                     ["   \.-(   ).  "],
                     ["    (   (__)  "],
                     ["   (___)____) "],
                     ["              "],
                     ["              "],
                     ["              "],
                     ["              "],
                     ["              "]],            
}  


Show_weather_keyword = ["สภาพอากาศ","อากาศ","อุณหภูมิ"]
Show_Face_humidity_keyword = ["ชื้น","น้ำ"]
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


'''
function
'''

def Emoji_Face_set(Face):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0))
    if Face == "Smile":
        draw.rectangle(((WIDTH*0.30)-5, 20, (WIDTH*0.30)+5, 60), outline=(255, 255, 0), fill=(255, 255, 0))
        draw.rectangle(((WIDTH*0.70)-5, 20, (WIDTH*0.70)+5, 60), outline=(255, 255, 0), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.30)-5, 15, (WIDTH*0.30)+5, 25), outline=(255, 255, 0), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.30)-5, 55, (WIDTH*0.30)+5, 65), outline=(255, 255, 0), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.70)-5, 15, (WIDTH*0.70)+5, 25), outline=(255, 255, 0), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.70)-5, 55, (WIDTH*0.70)+5, 65), outline=(255, 255, 0), fill=(255, 255, 0))
        draw.ellipse((WIDTH*0.15, HEIGHT*0.65, WIDTH*0.85, HEIGHT*0.85), outline=(255, 255, 0,20))
        draw.rectangle((WIDTH*0.15, HEIGHT*0.65, WIDTH*0.85, HEIGHT*0.75),fill=(0, 0, 0))
        disp.display(img)
    
    elif Face == "Hot_need_Water":
        draw.ellipse(((WIDTH*0.3)-15, 30, (WIDTH*0.3)+15, 60), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.7)-15, 30, (WIDTH*0.7)+15, 60), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.23)-15, 10, (WIDTH*0.23)+15, 40), fill=(0, 0, 0))
        draw.ellipse(((WIDTH*0.77)-15, 10, (WIDTH*0.77)+15, 40), fill=(0, 0, 0))
        draw.ellipse(((WIDTH*0.50)-30, HEIGHT*0.60, (WIDTH*0.5)+30, HEIGHT*0.80), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.50)-20, HEIGHT*0.65, (WIDTH*0.5)+20, HEIGHT*0.9), fill=(0, 0, 200))
        draw.ellipse(((WIDTH*0.82)-5, 35, (WIDTH*0.82)+5, 50), fill=(255, 0, 0))
        draw.line(((WIDTH*0.50),HEIGHT*0.68, (WIDTH*0.50),HEIGHT*0.85 ), fill=(100, 100, 255))
        disp.display(img)
        
    elif Face == "Sunlight":
        draw.rectangle(((WIDTH*0.23), 30, (WIDTH*0.43), 60), fill=(50, 50, 50))
        draw.ellipse(((WIDTH*0.18)-20, 30, (WIDTH*0.18)+20, 70), fill=(0, 0, 0))
        draw.ellipse(((WIDTH*0.48)-20, 30, (WIDTH*0.48)+20, 70), fill=(0, 0, 0))
     
        draw.rectangle(((WIDTH*0.57), 30, (WIDTH*0.77), 60), fill=(50, 50, 50))
        draw.ellipse(((WIDTH*0.52)-20, 30, (WIDTH*0.52)+20, 70), fill=(0, 0, 0))
        draw.ellipse(((WIDTH*0.82)-20, 30, (WIDTH*0.82)+20, 70), fill=(0, 0, 0))
     
        draw.ellipse(((WIDTH*0.28)-11, 30, (WIDTH*0.28)+10, 60), fill=(50, 50, 50))
        draw.ellipse(((WIDTH*0.38)-10, 30, (WIDTH*0.38)+11, 60), fill=(50, 50, 50))
     
        draw.ellipse(((WIDTH*0.62)-11, 30, (WIDTH*0.62)+10, 60), fill=(50, 50, 50))
        draw.ellipse(((WIDTH*0.72)-10, 30, (WIDTH*0.72)+11, 60), fill=(50, 50, 50))
     
        draw.rectangle(((WIDTH*0.3), 32, (WIDTH*0.7), 35), fill=(50, 50, 50))
        draw.rectangle(((WIDTH*0.3), 39, (WIDTH*0.7), 40), fill=(50, 50, 50))
     
        draw.ellipse((WIDTH*0.25, HEIGHT*0.55, WIDTH*0.75, HEIGHT*0.75), outline=(255, 255, 0,20))
        draw.rectangle((WIDTH*0.15, HEIGHT*0.55, WIDTH*0.85, HEIGHT*0.65),fill=(0, 0, 0))
        disp.display(img)
        
    elif Face == "MuchWater":
        draw.ellipse(((WIDTH*0.3)-15, 30, (WIDTH*0.3)+15, 60), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.7)-15, 30, (WIDTH*0.7)+15, 60), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.23)-15, 10, (WIDTH*0.23)+15, 40), fill=(0, 0, 0))
        draw.ellipse(((WIDTH*0.77)-15, 10, (WIDTH*0.77)+15, 40), fill=(0, 0, 0))
     
        draw.ellipse(((WIDTH*0.5)-15, 75, (WIDTH*0.5)+15, 105), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.5)-15, 80, (WIDTH*0.5)+15, 110), fill=(0, 0, 0))
     
        draw.ellipse(((WIDTH*0.65)-10, 75, (WIDTH*0.65)+10, 95), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.67)-10, 75, (WIDTH*0.67)+10, 95), fill=(0, 0, 0))
     
        draw.ellipse(((WIDTH*0.35)-10, 75, (WIDTH*0.35)+10, 95), fill=(255, 255, 0))
        draw.ellipse(((WIDTH*0.33)-10, 75, (WIDTH*0.33)+10, 95), fill=(0, 0, 0))
        disp.display(img)
    
    elif Face == "Dark":
        draw.ellipse(((WIDTH*0.3)-15, 30, (WIDTH*0.3)+15, 60), fill=(100, 100, 0))
        draw.ellipse(((WIDTH*0.7)-15, 30, (WIDTH*0.7)+15, 60), fill=(100, 100, 0))
        disp.display(img)


async def getweather(place):
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.METRIC) as client:
    # fetch a weather forecast from a city
    weather = await client.get(place)
    
    return weather.current.temperature,weather.current.description

def show_Ascii_art_weather():
    # Temp , description = asyncio.run(getweather('ladkrabang'))
    Temp , description = asyncio.run(getweather('Lat krabang'))
    if description == "Patchy rain possible":
        description = "Light rain"
    elif description == "Clear":
        description = "Sunny"
    '''
    First design
    '''
    # for row in Emoji_set[description]:
    #     for char in row:
    #         print(char,end="")
    #     print()
    
    # print("    {}°C".format(Temp))
    # print(description)

    '''
    Second design
    '''
    #for i in range(len(Ascii_art_set[description])):
        #Ascii_row_str = "".join(Ascii_art_set[description][i]) #รวมตัวอักษรใน Row เดียวกันเข้าด้วยกัน
        #if i == 3:
            #print("" + Ascii_row_str + " " * 3 + description)
        #elif i == 4:
            #print(Ascii_row_str + " " * 8 + "{}°C".format(Temp))
        #else:
            #print(Ascii_row_str)
    '''
    For LCD
    '''
    print(description)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0))
    position = (WIDTH*0.45)
    draw.text((position, 20), description, font=font1, fill=(255, 255, 255))
    draw.text((WIDTH*0.60, 50), "{}°C".format(Temp), font=font2, fill=(0, 255, 255),font_size = 30)
    for i in range(len(Ascii_art_set[description])):
        Ascii_row_str = "".join(Ascii_art_set[description][i]) #รวมตัวอักษรใน Row เดียวกันเข้าด้วยกัน
        draw.text((2, (i*9)), Ascii_row_str , font=font, fill=(255, 255, 255))
    disp.display(img)

def get_Data():
    sock.sendto("Request".encode('utf-8'), ip_client)
    data, addr = sock.recvfrom(1024) # get data
    print("received message: {} from {}\n".format(data,addr))
    text = str(data)
    text_part = re.split('\s+',text)
    Moise = int(text_part[0][text_part[0].find(":")+1:])
    LDR = int(text_part[1][text_part[1].find(":")+1:])
    Temp = int(text_part[2][text_part[2].find(":")+1:text_part[2].find("'")])
    return Moise,LDR,Temp


def Dicision_Face():
    Moise,LDR,Temp = get_Data()
    if  Moise > 95:
        Emoji_Face_set("MuchWater")
    elif Moise < 40 or Temp > 30:
        Emoji_Face_set("Hot_need_Water")
    elif LDR < 200:
        Emoji_Face_set("Dark")
    elif LDR > 2000:
        Emoji_Face_set("Sunlight")
    else: Emoji_Face_set("Smile")
    
def Show_moise():
    Moise,LDR,Temp = get_Data()
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0))
    draw.text((2, HEIGHT/2-8), "Moiseture: "+str(Moise) +"%", font=font2, fill=(255, 255, 0))
    disp.display(img)
#สร้างfunctionรับค่าเซนเซอร์

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def main():
    print("Start")
    Emoji_Face_set("Smile")
    with mic as source:
        while True:
            #audio = recog.listen(source,timeout=10,phrase_time_limit = 10)
            audio = recog.record(source,duration = 5)
            try:
                text = recog.recognize_google(audio,language='th')
                #text = "อุณหภูมิ"
                print("Done")
                print(text)

                # make it in to function
                for keyword in Show_weather_keyword:
                    if keyword in text:
                        show_Ascii_art_weather()
                for keyword in Show_Face_humidity_keyword:
                    if keyword in text:
                        Show_moise()
                time.sleep(5)
            except:
                draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0))
                disp.display(img)
                Dicision_Face()
                continue
            draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0))
            disp.display(img)
            Dicision_Face()
    
init()   
main2()

