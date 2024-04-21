import random
from picamera import PiCamera
import tkinter as tk
import tkinter.font as font
from time import sleep
from subprocess import call
from filestack import Client
import requests
import time
import RPi.GPIO as GPIO
import pickle
import csv
import cv2
import re
import numpy as np
import Adafruit_DHT
from pandas import read_csv

############################## Initializing #####################################################
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.AM2302
# Set GPIO sensor is connected to
gpio=18
nobody_out_counter = 0 
total_counter = 0
temp_humid_counter = 0
total_temp = 0;
total_humid = 0;
final_start_time = time.time()
ending_time = time.time()
humidity = 0
temperature = 0

################Importing machine model
with open('adaboosted_decisiontree.pickle', "rb") as file:
    model = pickle.load(file)

#################Initializing ultrasonic
move_list = [];
no_set = 1
counter = 0;
velocity = 0;
data_distance = [];
data_velocity = [];
direction_array = []
direction = 0

time_before = time.time()
time_after = time.time()
time_counter = time_after - time_before
out_counter = 0

#initialise distance
distance1 = 100
distance2 = 100 
distance3 = 100
output_distance = 0
#while time_counter <(15*60):
counter_velo = 0
counter_velo_2 = 0

flag = 0
second_pause_flag = 0
randomlist = []
real_code = ''
getFile_temp = 0

master = tk.Tk()
myfont = font.Font(family = "helvetica", size = 13, weight = "bold")
master.title("Welcome to My IoT House")
myfontsmall = font.Font(family = "helvetica", size = 4)

pause = 0

#######################Initializing excel
cur_day = time.strftime("%y %b %d")
cur_file = "temp_" + time.strftime("%y%b%d_%H%M%S")+'.csv'
encrypt_excel = []

csvfile = open(cur_file, "w", newline = "")
fieldnames = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','class']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()  

flag_excel = 1      

deactivated = 0

key_excel = '127'

######################Password & ID database
username = 'ZQG'
pw = 'JaSfaBhaCGldDGrE'

#######################Initiate GUI
tk.Label(master, text="Login ID:", font = myfont).grid(row=0)
tk.Label(master, text="Password:", font = myfont).grid(row=1)
tk.Label(master, text="Key:", font = myfont).grid(row=2)

ID = tk.Entry(master)
ID.grid(row = 0, column = 1)

Password = tk.Entry(master)
Password.grid(row = 1, column = 1)

Key = tk.Entry(master)
Key.grid(row = 2, column = 1)

filename = ''
getFile_button = 0
# ID.focus_set()
# Password.focus_set()


# slave = tk.Tk()
# slave.title('Excel Decryption')
# filename = tk.Entry(slave)
# filename.grid(row = 0, column = 1)

# Password1 = tk.Entry(slave)
# Password1.grid(row = 1, column = 1)
################################################################################################
def splitting_excel(string, L):
    if (L == 8):
        final_split = ' '.join(string[i:i+4] for i in range(0,L+1,4))
            
    elif (L == 9):
        split1 = ' '.join(string[i:i+4] for i in range(0,3,4))
        split2 = ' '.join(string[i:i+5] for i in range(4,9,5))
        final_split = ''.join(split1+" "+split2)
        
    elif (L == 10):
        split1 = ' '.join(string[i:i+5] for i in range(0,4,5))
        split2 = ' '.join(string[i:i+5] for i in range(5,9,5))
        final_split = ''.join(split1+" "+split2)
    elif (L == 6):
        final_split = string
        
    return final_split

#################################################################################################
def sendTempHumid(temp,humid,percentage):
     # print(distance1)
     # client = Client("Ah5gtbg2AT8em79PQeS0Nz") #filestack api key = abcdefghijk
     # #camera = PiCamera();
     # camera.capture('/home/pi/Desktop/image.jpg') #path to your image
     # new_filelink = client.upload(filepath="/home/pi/Desktop/image.jpg") #path to you image
     # print(new_filelink.url)
     r = requests.post("https://maker.ifttt.com/trigger/temperature_humid/with/key/cOo7hc8qG2ke4w0Qv9ZWL6",
     json={"value1" : temp,"value2" : humid,"value3" : percentage}) #one line # ifttt api key = hjklyuioi
     if r.status_code == 200:
         print("Temperature and Humidity Sent")
     else:
         print("Error")


#################################################################################################
def send2FA(code):
     # print(distance1)
     # client = Client("Ah5gtbg2AT8em79PQeS0Nz") #filestack api key = abcdefghijk
     # #camera = PiCamera();
     # camera.capture('/home/pi/Desktop/image.jpg') #path to your image
     # new_filelink = client.upload(filepath="/home/pi/Desktop/image.jpg") #path to you image
     # print(new_filelink.url)
     r = requests.post(
     "https://maker.ifttt.com/trigger/code/with/key/cOo7hc8qG2ke4w0Qv9ZWL6",
     json={"value1" : code}) #one line # ifttt api key = hjklyuioi
     if r.status_code == 200:
         print("Alert Sent")
     else:
         print("Error")

def convert(file_h264, file_mp4,cause):
    ###################Initiate the camera module with pre-defined settings.
   # Record a 15 seconds video.
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.rotation = 180
    camera.framerate = 30
    print("Intruder Alert!\n")
    client = Client("AXqtYYgvRAWAY4uEllVn0z") #filestack api key = abcdefghijk
    filename = "video" + (time.strftime("%y%b%d_%H%M%S"))
    camera.start_preview() 
    camera.start_recording("/home/pi/"+filename+'.h264')
    sleep(60)
    camera.stop_recording()
    camera.stop_preview()
    camera.close()
    print("Rasp_Pi => Video Recorded! \r\n")
    # Convert the h264 format to the mp4 format.
    command = "MP4Box -add " + "/home/pi/"+filename+'.h264' + " " + "/home/pi/"+filename+'.mp4'
    call([command], shell=True)
    #command = "MP4Box -add pythonVideo.h264 convertedVideo.mp4"
    # Execute our command
    #call([command], shell=True)
    print("\r\nRasp_Pi => Video Converted! \r\n")
    new_filelink = client.upload(filepath="/home/pi/"+filename+'.mp4') #path to you image
    print(new_filelink.url)
    r = requests.post(
     "https://maker.ifttt.com/trigger/intruder/with/key/cOo7hc8qG2ke4w0Qv9ZWL6",
     json={"value1" : new_filelink.url,"value2" : cause}) #one line # ifttt api key = hjklyuioi
    if r.status_code == 200:
        print("Alert Sent")
    else:
        print("Error")

# Close the GUI
def close():
    master.destroy()
    # slave.destroy()
    

def ultrasonic():
    global no_set, counter, velocity, data_distance, data_velocity, direction_array, direction, move_list, out_counter
    global distance1, distance2, distance3, csvfile, writer, cur_day, key_excel, encrypt_excel,nobody_out_counter,total_counter,ending_time,final_start_time,temperature,humidity,temp_humid_counter,total_temp,total_humid,flag_excel
    
    ending_time = time.time()
    if (time.strftime("%y %b %d") != cur_day) or (flag_excel == 0):
        if (flag_excel != 0):    
            csvfile.close()
            
        flag_excel = 1
        cur_day = time.strftime("%y %b %d")
        new_file = "temp_" + time.strftime("%y%b%d_%H%M%S") +'.csv' 
        cur_file = new_file
        csvfile = open(cur_file, "w")
        fieldnames = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','class']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
    #operation["text"] = "Ultrasonic sensing"
    print('FIRST START')
    sleep(1)
    print('GO')
    
    for count1 in range(no_set): #20 sets of data per action 
        print()    
        print("........ START NOW ....................................................")
        print()
        print(count1)
        sleep(5)
        
        for count in range(31): #use 31 distance points to construct 30 velocity point
            #Setting up the GPIO pins connected to the sensor       
            if(out_counter == 0):
                GPIO.setmode(GPIO.BOARD)
                PIN_TRIGGER = 35
                PIN_ECHO = 37
                GPIO.setup(PIN_TRIGGER, GPIO.OUT)
                GPIO.setup(PIN_ECHO, GPIO.IN)
                GPIO.output(PIN_TRIGGER, GPIO.LOW)
                #print("Waiting for the sensor to settle")
                time.sleep(0.1)
                #Calculate the distance 
                #print("Calculating Distance")
                GPIO.output(PIN_TRIGGER, GPIO.HIGH)
                time.sleep(0.00001) #setting trigger pin to high for 10 us
                GPIO.output(PIN_TRIGGER, GPIO.LOW)
                while GPIO.input(PIN_ECHO) == 0:
                    start_time = time.time()
                while GPIO.input(PIN_ECHO) == 1:
                    end_time = time.time()
                pluse_duration = end_time - start_time
                distance1 = round(pluse_duration * 17150, 2)
                
                GPIO.cleanup()
                
            elif(out_counter == 1):
                GPIO.setmode(GPIO.BOARD)
                PIN_TRIGGER = 7
                PIN_ECHO = 11
                GPIO.setup(PIN_TRIGGER, GPIO.OUT)
                GPIO.setup(PIN_ECHO, GPIO.IN)
                GPIO.output(PIN_TRIGGER, GPIO.LOW)
                #print("Waiting for the sensor to settle")
                #print("HELLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLO")
                time.sleep(0.1)
                #Calculate the distance 
                #print("Calculating Distance")
                GPIO.output(PIN_TRIGGER, GPIO.HIGH)
                time.sleep(0.00001) #setting trigger pin to high for 10 us
                GPIO.output(PIN_TRIGGER, GPIO.LOW)
                while GPIO.input(PIN_ECHO) == 0:
                    start_time = time.time()
                while GPIO.input(PIN_ECHO) == 1:
                    end_time = time.time()
                pluse_duration = end_time - start_time
                distance2 = round(pluse_duration * 17150, 2)
                
                GPIO.cleanup()
                
            elif(out_counter == 2):
                GPIO.setmode(GPIO.BOARD)
                PIN_TRIGGER = 13
                PIN_ECHO = 15
                GPIO.setup(PIN_TRIGGER, GPIO.OUT)
                GPIO.setup(PIN_ECHO, GPIO.IN)
                GPIO.output(PIN_TRIGGER, GPIO.LOW)
                #print("Waiting for the sensor to settle")
                #print("HELLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLO")
                time.sleep(0.1)
                #Calculate the distance 
                #print("Calculating Distance")
                GPIO.output(PIN_TRIGGER, GPIO.HIGH)
                time.sleep(0.00001) #setting trigger pin to high for 10 us
                GPIO.output(PIN_TRIGGER, GPIO.LOW)
                while GPIO.input(PIN_ECHO) == 0:
                    start_time = time.time()
                while GPIO.input(PIN_ECHO) == 1:
                    end_time = time.time()
                pluse_duration = end_time - start_time
                distance3 = round(pluse_duration * 17150, 2)
                
                GPIO.cleanup()
            
            output_distance = min(distance1,distance2,distance3)
            data_distance.append(output_distance); 
            #print(output_distance)
            
            if(output_distance == distance1):
                #print("From direction 1")
                direction = 1
            
            elif(output_distance == distance2):
                #print("From direction 2")
                direction = 2
                
            elif(output_distance == distance3):
                #print("From direction 3")
                direction = 3 
            
            direction_array.append(direction)
            
            
            if (out_counter == 0):
                out_counter = 1;
                
            elif (out_counter == 1):
                out_counter = 2;
                
            elif (out_counter == 2):
                out_counter = 0;
                
        
        for count2 in range(30):
            velocity = round((data_distance[counter_velo+count2+1]-data_distance[counter_velo+count2])/0.1,1)
            data_velocity.append(velocity)
    
        data_velocity.extend(direction_array)
        
        x = [data_velocity]
       
        movement = model.predict(x)
        avg_dist = sum(data_distance)/31
        
        if (movement == ['Nobody'] or movement == ['stand still']):
            #print("auto correction")
            if(avg_dist > 80):
                movement = ['Nobody']
            
            else:
                movement = ['stand still']
                
        print(movement)
        move_list.append(movement)
        movement = ''.join(movement) #converting array to string
        movement = movement.replace(" ","") #joining the string
        
        count_excel = 0
        
        #excel 
        for eachEle in data_velocity:    
            eachEle = str(int(eachEle))
            print(eachEle)
            #encrypt_excel.append(caesar_encrypt(eachEle,3))          
            for eachKey in key_excel:
                 if (int(eachKey) == 0):
                     eachEle = caesar_encrypt(eachEle, 1)
                     #movement = caesar_encrypt(movement, 1)
                
                 elif (int(eachKey) == 1):
                     eachEle = caesar_encrypt(eachEle, 4)
                     #movement = caesar_encrypt(movement, 4)
                
                 elif (int(eachKey) == 2):
                     eachEle = caesar_encrypt(eachEle, 8)
                     #movement = caesar_encrypt(movement, 8)
                
                 elif (int(eachKey) == 3):
                     eachEle = transposition(eachEle,key_excel,4)
                     #movement = transposition(movement,key_excel,4)
                
                 elif (int(eachKey) == 4):
                     eachEle = transposition(eachEle,key_excel,7)
                     #movement = transposition(movement,key_excel,7)
                
                 elif (int(eachKey) == 5):
                     eachEle = transposition(eachEle,key_excel,9)
                     #movement = transposition(movement,key_excel,9)
                
                 elif (int(eachKey) == 6):
                     eachEle = transposition(eachEle,key_excel,5)
                     #movement = transposition(movement,key_excel,5)
                
                 elif (int(eachKey) == 7):
                     eachEle = substitution(eachEle,key_excel,7)
                     #movement = substitution(movement,key_excel,7)
                
                 elif (int(eachKey) == 8):
                     eachEle = substitution(eachEle,key_excel,8)
                     #movement = substitution(movement,key_excel,8)
                
                 elif (int(eachKey) == 9):
                     eachEle = substitution(eachEle,key_excel,9)
                     #movement = substitution(movement,key_excel,9)
            
            count_excel = count_excel + 1
            
            if (count_excel == 61):
                temp_excel = transposition(movement,key_excel,4)
                count_excel = 0
                                          
                if (movement == 'standstill'):
                    movement = splitting_excel(temp_excel, 10)
                    
                elif (movement == 'PastLeft'):
                    movement = splitting_excel(temp_excel, 8)
                    
                elif (movement == 'PastRight'):
                    movement = splitting_excel(temp_excel, 9)
                else:
                    movement = temp_excel
                    
            
            encrypt_excel.append(eachEle)
            
            print("Encrypted Text:",encrypt_excel)
            
            print(data_velocity)
            
            
            
            
        #print(encrypt_excel)
        writer.writerow({'1': encrypt_excel[0],'2':encrypt_excel[1],'3':encrypt_excel[2],'4':encrypt_excel[3],'5':encrypt_excel[4],'6':encrypt_excel[5],'7':encrypt_excel[6],'8':encrypt_excel[7],'9':encrypt_excel[8],'10':encrypt_excel[9],
                          '11':encrypt_excel[10],'12':encrypt_excel[11],'13':encrypt_excel[12],'14':encrypt_excel[13],'15':encrypt_excel[14],'16':encrypt_excel[15],'17':encrypt_excel[16],'18':encrypt_excel[17],'19':encrypt_excel[18],'20':encrypt_excel[19],
                          '21':encrypt_excel[20],'22':encrypt_excel[21],'23':encrypt_excel[22],'24':encrypt_excel[23],'25':encrypt_excel[24],'26':encrypt_excel[25],'27':encrypt_excel[26],'28':encrypt_excel[27],'29':encrypt_excel[28],'30':encrypt_excel[29],
                          '31':encrypt_excel[30],'32':encrypt_excel[31],'33':encrypt_excel[32],'34':encrypt_excel[33],'35':encrypt_excel[34],'36':encrypt_excel[35],'37':encrypt_excel[36],'38':encrypt_excel[37],'39':encrypt_excel[38],'40':encrypt_excel[39],
                          '41':encrypt_excel[40],'42':encrypt_excel[41],'43':encrypt_excel[42],'44':encrypt_excel[43],'45':encrypt_excel[44],'46':encrypt_excel[45],'47':encrypt_excel[46],'48':encrypt_excel[47],'49':encrypt_excel[48],'50':encrypt_excel[49],
                          '51':encrypt_excel[50],'52':encrypt_excel[51],'53':encrypt_excel[51],'54':encrypt_excel[53],'55':encrypt_excel[54],'56':encrypt_excel[55],'57':encrypt_excel[56],'58':encrypt_excel[57],'59':encrypt_excel[58],'60':encrypt_excel[59],'61':encrypt_excel[60],'class': movement })
        
        
        ##resetting 
        direction_array = []
        data_velocity =[]    
        data_distance =[]
        encrypt_excel = []
        
        ##initialise distance
        distance1 = 200
        distance2 = 200
        distance3 = 200
    
    
    
        if (len(move_list) == 5):
            humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
            print(humidity)
            print(temperature)

            
            nobody_count = move_list.count(['Nobody'])
            standstill_count = move_list.count(['stand still'])
            left_count = move_list.count(['Past Left'])
            right_count = move_list.count(['Past Right'])
            nobody_out_counter = nobody_out_counter + nobody_count
            total_counter = total_counter + 5
            
            total_humid = total_humid + humidity
            total_temp = total_temp + temperature
            temp_humid_counter = temp_humid_counter + 1
            
            if(humidity>80 or (temperature>28 and temperature<40)): ## normal operation
                if (nobody_count >= 3):
                    print("No suspicious movement")
                else:
                    print("Start Recording")
                    convert('/home/pi/testhello.h264', '/home/pi/testhello.mp4','Suspecious activity detected in front of the door.')
            elif temperature > 40: ## FIRE
                if (nobody_count >= 3):
                    print("No suspicious movement")
                elif (left_count + right_count)>=3:
                    print("Start Recording")
                    convert('/home/pi/testhello.h264', '/home/pi/testhello.mp4','Something has probably caught on FIRE !!!')
                else :
                    print("Start Recording")
                    convert('/home/pi/testhello.h264', '/home/pi/testhello.mp4','Suspecious activity detected in front of the door.')
            else: #rainy day 
                if (nobody_count + standstill_count>= 3):
                    print("No suspicious movement")
                else:
                    print("Start Recording")
                    convert('/home/pi/testhello.h264', '/home/pi/testhello.mp4','Suspecious activity detected in front of the door.')
            
            #Resetting move_list                   
            move_list = []
            
            if ((ending_time-final_start_time) > 60*1 ): #10 mins update once 
                percentage = (nobody_out_counter/total_counter)*100
                percentage = round(percentage,2)
                avg_temp = total_temp/temp_humid_counter
                avg_humid = total_humid/temp_humid_counter
                output_temp = round(avg_temp,2)
                output_humidity = round(avg_humid,2)
                
                # resetting count
                nobody_out_counter=0
                total_counter = 0
                total_humid = 0
                total_temp = 0
                temp_humid_counter = 0
                final_start_time = time.time()
                
                sendTempHumid(output_temp,output_humidity,percentage)

       

# Scan QR code function here 
def Login():
    global pause,csvfile,username,pw,getFile_button,getFile_temp,deactivated
    master.update()
    key = str(Key.get())
    user = str(ID.get())
    password = str(Password.get())
    user = main_encryption(user,key)
    password = main_encryption(password,key)
    
    if (password == pw and user == username):
        pause = 0
        print("correct password")
        print()
        operation["text"] = "Ultrasonic sensing"
        ID.delete(0,'end')
        Password.delete(0,'end')
        Key.delete(0,'end')
        if (deactivated == 1):
            getFile_button.destroy()
            deactivated = 0
        master.update()
        
        while(pause == 0):
            operation["text"] = "Ultrasonic sensing"
            master.update()
#             pause_button = tk.Button(master, text="Pause", command=pause_func, font = myfont, height=1, width=10)
#             pause_button.grid(row = 3, column = 5)

            ultrasonic()
#            QRcode_button = tk.Button(master, text="Scan QRcode", command=QRcode, font = myfont, height=1, width=10)
#            QRcode_button.grid(row = 2, column = 5)
            master.update()

        
    else:
        print("Please register")
        print()
        
def pause_func():
    global pause,flag
    flag = 1
    operation["text"] = "Enter password to deactivate"
    master.update()
    
        
    # ID1 = tk.Entry(slave)
    # ID1.grid(row = 0, column = 1)
    
    # Password1 = tk.Entry(slave)
    # Password1.grid(row = 1, column = 1)
    # user = str(ID.get())
    # password = str(Password.get())
    time_before = time.time()
    
    while flag == 1:
        time_after = time.time()
        time_counter = time_after - time_before
        if(time_counter >60):
            flag = 0
            operation["text"] = "Session expired"
            #master.update
            sleep(2)
        #enter_button = tk.Button(master, text="-->", command=enter_func, font = myfont, height=1, width=5)
        #enter_button.grid(row = 1, column = 5)
        master.update()
    
    # user = input("Login ID")
    # password = input("Password")

    # if (password == "ABC" and user == "123"):
    #     print("correct password")
    #     print()
    #     operation["text"] = "Deactivated"
    #     master.update()
    #     pause = 1

def second_pause_func():
    global second_pause_flag
    second_pause_flag = 1
    while second_pause_flag == 1: 
        master.update()        
        
    
    # while(flag):
    #     enter_button = tk.Button(master, text="-->", command=enter_func, font = myfont, height=1, width=5)
    #     enter_button.grid(row = 1, column = 5)
        
def enter_func():
    print("HELLO")
    global flag,pause,second_pause_flag,randomlist,real_code,deactivated,flag_excel,username,pw,filename,getFile_temp,getFile_button

    
    key = str(Key.get())
    user = str(ID.get())
    password = str(Password.get())
    user = main_encryption(user,key)
    password = main_encryption(password,key)
    
    
    ID.delete(0,'end')
    Password.delete(0,'end')
    Key.delete(0,'end')
    
    if (password == pw and user == username):
        print("correct password")
        print()
        operation["text"] = "2FA sent."
        master.update()
        for i in range(4):
            n = random.randint(0,9)
            randomlist.append(n)
        #print(randomlist)
        real_code = np.array(randomlist)
        real_code = ''.join(str(e) for e in real_code)
        
        #print(real_code)

        send2FA(randomlist)
        randomlist = [] ##resetting
        second_pause_func()
        #pause = 1
    elif(second_pause_flag == 1):
        if(password == real_code):
            pause = 1
            deactivated = 1
            operation["text"] = "Deactivated."
            csvfile.close()
            flag_excel = 0
            
            filename = tk.Entry(master)
            filename.grid(row = 10, column = 1)
            getFile_temp = 1
            getFile_button = tk.Button(master, text="Get File", command=decrypt_func, font = myfont, height=1, width=5)
            getFile_button.grid(row = 11, column = 1)
            master.update()
        else:
            operation["text"] = "Invalid code."
            master.update()
            sleep(2)
        second_pause_flag = 0
      
    else:
        operation["text"] = "Wrong password"
        master.update()
    
    flag = 0
          
def QRcode():
    operation["text"] = "Scanning QRcode now"
    master.update()
    # the QRcode scanner code here
    cap = cv2.VideoCapture(0)
    ret = cap.set(3,320)
    ret = cap.set(4,240)
    detector = cv2.QRCodeDetector()

    print("Reading QR code using Raspberry Pi camera")

    while True:
        print("QR scanner in operation")
        _, img = cap.read()
        img2 = cv2.flip(img,0)
        cv2.imshow("code detector", img2)
        cv2.waitKey(1)
        data, bbox, _ = detector.detectAndDecode(img)
        
        if bbox is not None:
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                         0, 0), thickness=2)
                
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
            
            if data:
                #sw1Press = False
                #buzzer.beep(0.1, 0.1, 1)
                print("Data found: " + data)
                #led.off()
                
                if (data == "1234"):
                    print("Access granted")
                    operation["text"] = "Pop box is opened"

                    
                    break
                data = ""
                
        
    cap.read()
    cap.release()
    cv2.destroyAllWindows() 
    master.update()
    sleep(2)
    
def caesar_encrypt(realText, step):
    outText = []
    cryptText = []
    uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numb_list = ['0','1','2','3','4','5','6','7','8','9','-']
    for eachLetter in realText:
        if eachLetter in uppercase:
            index = uppercase.index(eachLetter)
            crypting = (index + step) % 26
            cryptText.append(crypting)
            newLetter = uppercase[crypting]
            outText.append(newLetter)
        elif eachLetter in lowercase:
            index = lowercase.index(eachLetter)
            crypting = (index + step) % 26
            cryptText.append(crypting)
            newLetter = lowercase[crypting]
            outText.append(newLetter)
        elif eachLetter in numb_list:
            index = numb_list.index(eachLetter)
            crypting = (index + step) % 11
            cryptText.append(crypting)
            newLetter = numb_list[crypting]
            outText.append(newLetter)
            
    outText = ''.join(outText)
    print("CaesarText:",outText)
    return outText

def substitution(realText,key,choice):
    caps = 1
    if (choice == 7):
        if (key == '000'):
            key = '111'
            
        newText = ''
        count = 0
        count_outer = 0
        uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        numb_list = ['0','1','2','3','4','5','6','7','8','9','-']
        
        my_dict1_A = ['B','G','T','N','H','Y','M','J','U','V','F','R','C','D','E','X','S','W','K','I','L','P','O','Q','Z','A']
        my_dict1_a = ['b','g','t','n','h','y','m','j','u','v','f','r','c','d','e','x','s','w','k','i','l','p','o','q','z','a']
        
        my_dict2_A = ['N','V','D','U','C','M','L','E','K','A','P','F','O','R','J','Z','W','B','S','G','T','I','H','Q','X','Y']
        my_dict2_a = ['n','v','d','u','c','m','l','e','k','a','p','f','o','r','j','z','w','b','s','g','t','i','h','q','x','y']
        
        for eachLetter in realText:
            if eachLetter in uppercase:
                index = uppercase.index(eachLetter)
                caps = 1
                
            elif eachLetter in lowercase:
                index = lowercase.index(eachLetter)
                caps = 0
            #print(index)
            
            elif eachLetter in numb_list:
                index = numb_list.index(eachLetter)
                
            if(count<int(key[0]) and count_outer<int(key[0]) and int(key[0])!=0):
               # print("key[0]")
                
                if(caps == 1):
                    newLetter = my_dict1_A[index]
                elif(caps == 0):
                    newLetter = my_dict1_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[0])):
                    #print("count reset")
                    count = 0 
                    
                #if(key[1]==0):
                    #count_outer = 0
                    
            elif(count<int(key[1]) and count_outer<(int(key[0])+int(key[1])) and int(key[1])!=0):
                #print("key[1]")
                
                if(caps == 1):
                    newLetter = my_dict2_A[index]
                elif(caps == 0):
                    newLetter = my_dict2_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[1])):
                    #print("count reset")
                    count = 0 
                    
            elif(count<int(key[2]) and count_outer<(int(key[0])+int(key[1])+int(key[2]))):
                #print("key[2]")
                
                if(caps == 1):
                    newLetter = my_dict1_A[index]
                elif(caps == 0):
                    newLetter = my_dict1_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[2])):
                    #print("count reset")
                    count = 0 
                    
            if(count_outer == (int(key[0])+int(key[1])+int(key[2]))):  #when got 2 zeros and one 1 and also to reset
                count_outer = 0
                    
        #print(newText)
    
    if (choice == 8):
        if (key == '000'):
            key = '111'
            
        newText = ''
        count = 0
        count_outer = 0
        uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        numb_list = ['0','1','2','3','4','5','6','7','8','9','-']
        
        my_dict1_A = ['Q','A','Z','W','S','X','E','D','C','R','F','V','T','G','B','Y','H','N','U','J','M','I','K','O','L','P']
        my_dict1_a = ['q','a','z','w','s','x','e','d','c','r','f','v','t','g','b','y','h','n','u','j','m','i','k','o','l','p']
        
        my_dict2_A = ['P','O','I','U','Y','T','R','E','W','Q','Z','X','C','V','B','N','M','L','K','J','H','G','F','D','S','A']     
        my_dict2_a = ['p','o','i','u','y','t','r','e','w','q','z','x','c','v','b','n','m','l','k','j','h','g','f','d','s','a']
        
        for eachLetter in realText:
            if eachLetter in uppercase:
                index = uppercase.index(eachLetter)
                caps = 1
                
            elif eachLetter in lowercase:
                index = lowercase.index(eachLetter)
                caps = 0
            #print(index)
            
            elif eachLetter in numb_list:
                index = numb_list.index(eachLetter)
            
            if(count<int(key[0]) and count_outer<int(key[0]) and int(key[0])!=0):
                #print("key[0]")
                
                if(caps == 1):
                    newLetter = my_dict1_A[index]
                elif(caps == 0):
                    newLetter = my_dict1_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[0])):
                   # print("count reset")
                    count = 0 
                    
                #if(key[1]==0):
                    #count_outer = 0
                    
            elif(count<int(key[1]) and count_outer<(int(key[0])+int(key[1])) and int(key[1])!=0):
                #print("key[1]")
                
                if(caps == 1):
                    newLetter = my_dict2_A[index]
                elif(caps == 0):
                    newLetter = my_dict2_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[1])):
                    #print("count reset")
                    count = 0 
                    
            elif(count<int(key[2]) and count_outer<(int(key[0])+int(key[1])+int(key[2]))):
               # print("key[2]")
                
                if(caps == 1):
                    newLetter = my_dict1_A[index]
                elif(caps == 0):
                    newLetter = my_dict1_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[2])):
                    #print("count reset")
                    count = 0 
                    
            if(count_outer == (int(key[0])+int(key[1])+int(key[2]))):  #when got 2 zeros and one 1
                count_outer = 0
                    
        #print(newText)
    
    if(choice == 9):
        if (key == '000'):
            key = '111'
            
        newText = ''
        count = 0
        count_outer = 0
        uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        numb_list = ['0','1','2','3','4','5','6','7','8','9','-']
        
        my_dict1_A = ['P','H','Q','G','I','U','M','E','A','Y','L','N','O','F','D','X','J','K','R','C','V','S','T','Z','W','B']
        my_dict1_a = ['p','h','q','g','i','u','m','e','a','y','l','n','o','f','d','x','j','k','r','c','v','s','t','z','w','b']
        
        my_dict2_A = ['V','J','Z','B','G','N','F','E','P','L','I','T','M','X','D','W','K','Q','U','C','R','Y','A','H','S','O']
        my_dict2_a = ['v','j','z','b','g','n','f','e','p','l','i','t','m','x','d','w','k','q','u','c','r','y','a','h','s','o']
        
        for eachLetter in realText:
            if eachLetter in uppercase:
                index = uppercase.index(eachLetter)
                caps = 1
                
            elif eachLetter in lowercase:
                index = lowercase.index(eachLetter)
                caps = 0
            #print(index)
            elif eachLetter in numb_list:
                index = numb_list.index(eachLetter)
            
            if(count<int(key[0]) and count_outer<int(key[0]) and int(key[0])!=0):
               # print("key[0]")
                
                if(caps == 1):
                    newLetter = my_dict1_A[index]
                elif(caps == 0):
                    newLetter = my_dict1_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[0])):
                   # print("count reset")
                    count = 0 
                    
                #if(key[1]==0):
                    #count_outer = 0
                    
            elif(count<int(key[1]) and count_outer<(int(key[0])+int(key[1])) and int(key[1])!=0):
                #print("key[1]")
                
                if(caps == 1):
                    newLetter = my_dict2_A[index]
                elif(caps == 0):
                    newLetter = my_dict2_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[1])):
                    #print("count reset")
                    count = 0 
                    
            elif(count<int(key[2]) and count_outer<(int(key[0])+int(key[1])+int(key[2]))):
               # print("key[2]")
                
                if(caps == 1):
                    newLetter = my_dict1_A[index]
                elif(caps == 0):
                    newLetter = my_dict1_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[2])):
                    #print("count reset")
                    count = 0 
                    
            if(count_outer == (int(key[0])+int(key[1])+int(key[2]))):  #when got 2 zeros and one 1
                count_outer = 0
    print("Substitution: ", newText)                
    return newText


def transposition(realText,key,size):
    ##ONLY APPLICABLE FOR SIZE 4,5,7,9#########################################
    uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    #extra_letter = ''
    key = int(key)
    
    if size == 4 :
        # if (len(realText)%4 != 0):
        #     length = 4-len(realText)%4
        #     for i in range(length):
                
        #         index_extra = uppercase.index('A')
        #         newLetter_extra = uppercase[index_extra]
        #         extra_letter = extra_letter + newLetter_extra;
                
                
        #realText = realText+extra_letter
                
                
        choice = key%10 #to generate the choice that will be used for transposition 
        pattern = []
        pattern1 = [0,1,2,3]
        pattern2 = [1,0,2,3]
        pattern3= [2,0,1,3]
        pattern4= [0,2,1,3]
        pattern5= [1,2,0,3]
        pattern6= [2,1,0,3]
        pattern7= [2,1,3,0]
        pattern8= [1,2,3,0]
        pattern9= [3,2,1,0]
        pattern10= [2,3,1,0]
        
        if (choice == 0):
            pattern = pattern10
        elif (choice == 1):
            pattern = pattern1
        elif (choice == 2):
            pattern = pattern2
        elif (choice == 3):
            pattern = pattern3
        elif (choice == 4):
            pattern = pattern4
        elif (choice == 5):
            pattern = pattern5
        elif (choice == 6):
            pattern = pattern6
        elif (choice == 7):
            pattern = pattern7
        elif (choice == 8):
            pattern = pattern8
        elif (choice == 9):
            pattern = pattern9        
            
        #print(pattern)
        count = 0; 
        column0 =[]
        column1 =[]
        column2 =[]
        column3 =[]
        outText=[]
        
        for eachLetter in realText:  
                
            if count == 0:
                #print("HELLO0\n")
                column0.append(eachLetter)
                #print("column0 = %f\n"column0)
                
            elif count == 1:
                #print("HELLO1\n")
                column1.append(eachLetter)
                
            elif count == 2:
                #print("HELLO2\n")
                column2.append(eachLetter)
                
            elif count == 3:
                #print("HELLO3\n")
                column3.append(eachLetter)
                
            count = (count +1)%4;
        #print(column0)
        #print(column1)
       # print(column2)
        #print(column3)
        for i in range(4):
            if i == pattern[0]:
                outText = outText+column0
            elif i == pattern[1]:
                outText = outText+column1
            elif i == pattern[2]:
                outText = outText+column2
            elif i == pattern[3]:
                outText = outText+column3

        outText = ''.join(outText)
        
    elif size == 5 :
        # if (len(realText)%5 != 0):
        #     length = 5-len(realText)%5
        #     #print(length)
        #     for i in range(length):
                
        #         index_extra = uppercase.index('A')
        #         newLetter_extra = uppercase[index_extra]
        #         extra_letter = extra_letter + newLetter_extra;
                
                
       # realText = realText+extra_letter
        #print(realText)
    
        choice = key%10 #to generate the choice that will be used for transposition 
        pattern = []
        pattern1 = [0,1,2,3,4]
        pattern2 = [1,0,2,3,4]
        pattern3= [2,0,1,3,4]
        pattern4= [0,2,1,3,4]
        pattern5= [1,2,0,3,4]
        pattern6= [2,1,0,3,4]
        pattern7= [2,1,3,0,4]
        pattern8= [1,2,3,0,4]
        pattern9= [3,2,1,0,4]
        pattern10= [2,3,1,0,4]
        
        if (choice == 0):
            pattern = pattern1
        elif (choice == 1):
            pattern = pattern2
        elif (choice == 2):
            pattern = pattern3
        elif (choice == 3):
            pattern = pattern4
        elif (choice == 4):
            pattern = pattern5
        elif (choice == 5):
            pattern = pattern6
        elif (choice == 6):
            pattern = pattern7
        elif (choice == 7):
            pattern = pattern8
        elif (choice == 8):
            pattern = pattern9
        elif (choice == 9):
            pattern = pattern10        
            
        #print(pattern)
        count = 0; 
        column0 =[]
        column1 =[]
        column2 =[]
        column3 =[]
        column4 = []
        outText=[]
        
        for eachLetter in realText:
            if eachLetter in uppercase:
                index = uppercase.index(eachLetter)
                newLetter = uppercase[index]
            elif eachLetter in lowercase:
                index = lowercase.index(eachLetter)
                newLetter = lowercase[index]       
            if count == 0:
                #print("HELLO0\n")
    
                column0.append(newLetter)
                #print("column0 = %f\n"column0)
            elif count == 1:
                #print("HELLO1\n")
                column1.append(newLetter)
            elif count == 2:
                #print("HELLO2\n")
                column2.append(newLetter)
            elif count == 3:
                #print("HELLO3\n")
                column3.append(newLetter)
            elif count == 4:
                #print("HELLO3\n")
                column4.append(newLetter)
            count = (count +1)%5;
            
        for i in range(5):
            if i == pattern[0]:
                outText = outText+column0
            elif i == pattern[1]:
                outText = outText+column1
            elif i == pattern[2]:
                outText = outText+column2
            elif i == pattern[3]:
                outText = outText+column3
            elif i == pattern[4]:
                outText = outText+column4

        outText = ''.join(outText)
        #print(outText)
        
    elif size == 7 :
        #print("I am in size = 7")
        # if (len(realText)%7 != 0):
        #     length = 7-len(realText)%7
        #     #print(length)
        #     for i in range(length):
                
        #         index_extra = uppercase.index('A')
        #         newLetter_extra = uppercase[index_extra]
        #         extra_letter = extra_letter + newLetter_extra;
                
                
        #realText = realText+extra_letter
        #print(realText)
                
                
                
        
        choice = key%10 #to generate the choice that will be used for transposition 
        pattern = []
        pattern1 = [1,3,2,0,4,5,6]
        pattern2 = [3,0,2,1,4,5,6]
        pattern3= [0,2,3,1,4,5,6]
        pattern4= [2,4,1,0,3,5,6]
        pattern5= [2,4,0,1,3,5,6]
        pattern6= [3,0,1,4,2,5,6]
        pattern7= [4,0,3,2,1,5,6]
        pattern8= [1,2,3,4,0,5,6]
        pattern9= [1,4,0,3,5,6,2]
        pattern10= [6,2,3,1,5,4,0]
        
        if (choice == 0):
            pattern = pattern1
        elif (choice == 1):
            pattern = pattern2
        elif (choice == 2):
            pattern = pattern3
        elif (choice == 3):
            pattern = pattern4
        elif (choice == 4):
            pattern = pattern5
        elif (choice == 5):
            pattern = pattern6
        elif (choice == 6):
            pattern = pattern7
        elif (choice == 7):
            pattern = pattern8
        elif (choice == 8):
            pattern = pattern9
        elif (choice == 9):
            pattern = pattern10        
            
        #print(pattern)
        count = 0; 
        column0 =[]
        column1 =[]
        column2 =[]
        column3 =[]
        column4 = []
        column5 = []
        column6 = []
        outText=[]
        
        for eachLetter in realText:  
                
            if count == 0:
                #print("HELLO0\n")
                column0.append(eachLetter)
                #print("column0 = %f\n"column0)
                
            elif count == 1:
                #print("HELLO1\n")
                column1.append(eachLetter)
                
            elif count == 2:
                #print("HELLO2\n")
                column2.append(eachLetter)
                
            elif count == 3:
                #print("HELLO3\n")
                column3.append(eachLetter)
                
            elif count == 4: #pattern[4]:
                #print("HELLO4\n")
                column4.append(eachLetter)
                
            elif count == 5 : #pattern[5]:
                #print("HELLO5\n")
                column5.append(eachLetter)
                
            elif count == 6: #pattern[6]
                #print("HELLO6\n")
                column6.append(eachLetter)
            
            #print(count)

            count = (count +1)%7;
        #print(column0)
       # print(column1)
        #print(column2)
        #print(column3)
        #print(column4)
        #print(column5)
        #print(column6)    
        
        for i in range(7):
            if i == pattern[0]:
                outText = outText+column0
            elif i == pattern[1]:
                outText = outText+column1
            elif i == pattern[2]:
                outText = outText+column2
            elif i == pattern[3]:
                outText = outText+column3
            elif i == pattern[4]:
                outText = outText+column4
            elif i == pattern[5]:
                outText = outText+column5
            elif i == pattern[6]:
                outText = outText+column6
            
        #outText = column1+column2+column4+column0+column3+column5+column6
        outText = ''.join(outText)
        
    elif size == 9 :
        #print("I am in size = 9")
        # if (len(realText)%9 != 0):
        #     length = 9-len(realText)%9
        #     #print(length)
        #     for i in range(length):
                
        #         index_extra = uppercase.index('A')
        #         newLetter_extra = uppercase[index_extra]
        #         extra_letter = extra_letter + newLetter_extra;
                
                
        # realText = realText+extra_letter
        #print(realText)
                
                
                
        
        choice = key%10 #to generate the choice that will be used for transposition 
        pattern = []
        pattern1 = [0,1,2,3,5,4,6,7,8]
        pattern2 = [3,4,7,8,1,5,0,6,2]
        pattern3= [4,7,2,8,3,6,1,5,0]
        pattern4= [5,3,6,2,0,8,4,1,7]
        pattern5= [4,8,3,7,2,0,5,1,6]
        pattern6= [7,1,6,3,8,4,2,0,5]
        pattern7= [6,8,5,4,3,1,0,7,2]
        pattern8= [7,6,8,3,2,0,1,5,4]
        pattern9= [8,1,4,3,0,2,7,6,5]
        pattern10= [8,7,5,6,1,2,4,3,0]
        
        if (choice == 0):
            pattern = pattern1
        elif (choice == 1):
            pattern = pattern2
        elif (choice == 2):
            pattern = pattern3
        elif (choice == 3):
            pattern = pattern4
        elif (choice == 4):
            pattern = pattern5
        elif (choice == 5):
            pattern = pattern6
        elif (choice == 6):
            pattern = pattern7
        elif (choice == 7):
            pattern = pattern8
        elif (choice == 8):
            pattern = pattern9
        elif (choice == 9):
            pattern = pattern10        
            
        #print(pattern)
        count = 0; 
        column0 =[]
        column1 =[]
        column2 =[]
        column3 =[]
        column4 = []
        column5 = []
        column6 = []
        column7 =[]
        column8 = []
        outText=[]
        
        for eachLetter in realText: 
                
            if count == 0 :#pattern[0]:
                #print("HELLO0\n")
                column0.append(eachLetter)
                #print("column0 = %f\n"column0)
                
            elif count == 1 :#pattern[1]:
                #print("HELLO1\n")
                column1.append(eachLetter)
                
            elif count == 2: #pattern[2]:
                #print("HELLO2\n")
                column2.append(eachLetter)
                
            elif count == 3 :#pattern[3]:
                #print("HELLO3\n")
                column3.append(eachLetter)
                
            elif count == 4: #pattern[4]:
                #print("HELLO4\n")
                column4.append(eachLetter)
                
            elif count == 5 : #pattern[5]:
                #print("HELLO5\n")
                column5.append(eachLetter)
                
            elif count == 6: #pattern[6]
                #print("HELLO6\n")
                column6.append(eachLetter)
 
            elif count == 7: #pattern[6]
                #print("HELLO6\n")
                column7.append(eachLetter)
                
            elif count == 8: #pattern[6]
                #print("HELLO6\n")
                column8.append(eachLetter)
            #print(count)

            count = (count +1)%9;
       # print(column0)
        #print(column1)
        #print(column2)
        #print(column3)
        #print(column4)
        #print(column5)
       # print(column6)
       # print(column7)
       # print(column8)
        
        for i in range(9):
            if i == pattern[0]:
                outText = outText+column0
            elif i == pattern[1]:
                outText = outText+column1
            elif i == pattern[2]:
                outText = outText+column2
            elif i == pattern[3]:
                outText = outText+column3
            elif i == pattern[4]:
                outText = outText+column4
            elif i == pattern[5]:
                outText = outText+column5
            elif i == pattern[6]:
                outText = outText+column6
            elif i == pattern[7]:
                outText = outText+column7
            elif i == pattern[8]:
                outText = outText+column8
            
        #outText = column1+column2+column4+column0+column3+column5+column6
        outText = ''.join(outText)
    #print(outText)
    print("Transposition: ",outText)
    return outText

def decrypt_func():
    global deactivated,filename
    print('decrypted file')
    if (deactivated == 1):
        #csvfile.close()
        deactivated = 0
        file_field = str(filename.get())
        
        csvfile = open(file_field, "r", newline = "") 
        string_file = "decrypt_" + file_field +'.csv'
        csvfile_decrypt = open(string_file, "w", newline = "")
        fieldnames = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','class']
        writer = csv.DictWriter(csvfile_decrypt, fieldnames=fieldnames)
        writer.writeheader()
        dataset = read_csv(csvfile, names=fieldnames)
        array = dataset.values
        
        for iter in range(1,len(array)):
            row = array[iter,:]
            decrypt_arr = []
            for iter2 in range(len(row)):
                if (iter2 == 61):
                    temp_decrypt = transpose_decrypt(row[iter2],'127',4)
                    print('I AM IN HERE')
                else:
                    temp_decrypt = killmenow(row[iter2],'127')
                
                temp_decrypt = ''.join(temp_decrypt) #converting array to string
                temp_decrypt = temp_decrypt.replace(" ","") #joining the string
                    
                ########decrypt func
                decrypt_arr.append(temp_decrypt)
        
            
            writer.writerow({'1': decrypt_arr[0],'2':decrypt_arr[1],'3':decrypt_arr[2],'4':decrypt_arr[3],'5':decrypt_arr[4],'6':decrypt_arr[5],'7':decrypt_arr[6],'8':decrypt_arr[7],'9':decrypt_arr[8],'10':decrypt_arr[9],
                              '11':decrypt_arr[10],'12':decrypt_arr[11],'13':decrypt_arr[12],'14':decrypt_arr[13],'15':decrypt_arr[14],'16':decrypt_arr[15],'17':decrypt_arr[16],'18':decrypt_arr[17],'19':decrypt_arr[18],'20':decrypt_arr[19],
                              '21':decrypt_arr[20],'22':decrypt_arr[21],'23':decrypt_arr[22],'24':decrypt_arr[23],'25':decrypt_arr[24],'26':decrypt_arr[25],'27':decrypt_arr[26],'28':decrypt_arr[27],'29':decrypt_arr[28],'30':decrypt_arr[29],
                              '31':decrypt_arr[30],'32':decrypt_arr[31],'33':decrypt_arr[32],'34':decrypt_arr[33],'35':decrypt_arr[34],'36':decrypt_arr[35],'37':decrypt_arr[36],'38':decrypt_arr[37],'39':decrypt_arr[38],'40':decrypt_arr[39],
                              '41':decrypt_arr[40],'42':decrypt_arr[41],'43':decrypt_arr[42],'44':decrypt_arr[43],'45':decrypt_arr[44],'46':decrypt_arr[45],'47':decrypt_arr[46],'48':decrypt_arr[47],'49':decrypt_arr[48],'50':decrypt_arr[49],
                              '51':decrypt_arr[50],'52':decrypt_arr[51],'53':decrypt_arr[51],'54':decrypt_arr[53],'55':decrypt_arr[54],'56':decrypt_arr[55],'57':decrypt_arr[56],'58':decrypt_arr[57],'59':decrypt_arr[58],'60':decrypt_arr[59],'61':decrypt_arr[60],'class': decrypt_arr[61]})
                
            decrypt_arr = []
        
        csvfile.close()
        csvfile_decrypt.close()
        # getFile_button.close()
        
        operation["text"] = "Successfully Decrypted!"
        filename.destroy()
        master.update()
    else:
        operation["text"] = "Please deactivate the system beforehand"
        master.update()

def subs_decrypt(realText,key,choice):
    if (choice == 7):
        
            
        newText = ''
        count = 0
        count_outer = 0
        caps = 1
        
        numb_list = ['0','1','2','3','4','5','6','7','8','9','-']
    
        my_dict1_A = ['B','G','T','N','H','Y','M','J','U','V','F','R','C','D','E','X','S','W','K','I','L','P','O','Q','Z','A']
        my_dict1_a = ['b','g','t','n','h','y','m','j','u','v','f','r','c','d','e','x','s','w','k','i','l','p','o','q','z','a']
        
        my_dict2_A = ['N','V','D','U','C','M','L','E','K','A','P','F','O','R','J','Z','W','B','S','G','T','I','H','Q','X','Y']
        my_dict2_a = ['n','v','d','u','c','m','l','e','k','a','p','f','o','r','j','z','w','b','s','g','t','i','h','q','x','y']
        
        for eachLetter in realText:
            
            if eachLetter in numb_list:
                index = numb_list.index(eachLetter)
                
            if(count<int(key[0]) and count_outer<int(key[0]) and int(key[0])!=0):
                
                if(caps == 1):
                    index = (my_dict1_A.index(eachLetter)) % 11
                    newLetter = numb_list[index]
                    
                elif(caps == 0):
                    newLetter = my_dict1_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[0])):
                    count = 0 
                                    
            elif(count<int(key[1]) and count_outer<(int(key[0])+int(key[1])) and int(key[1])!=0):
                
                if(caps == 1):
                    index = (my_dict2_A.index(eachLetter)) % 11
                    newLetter = numb_list[index]
                elif(caps == 0):
                    newLetter = my_dict2_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[1])):
                    count = 0 
                    
            elif(count<int(key[2]) and count_outer<(int(key[0])+int(key[1])+int(key[2]))):
                
                if(caps == 1):
                    index = (my_dict1_A.index(eachLetter)) % 11
                    newLetter = numb_list[index]
                elif(caps == 0):
                    newLetter = my_dict1_a[index]
                    
                newText = newText + newLetter
                count = count +1 
                count_outer = count_outer+1 
                if(count == int(key[2])):
                    count = 0 
                    
            if(count_outer == (int(key[0])+int(key[1])+int(key[2]))):  #when got 2 zeros and one 1 and also to reset
                count_outer = 0

        return newText

def transpose_decrypt(realText, key, size):
    final_split = ''
    
    realText = realText.replace(" ","")
    key = int(key)
    
    if size == 4: 
        
        choice = key%10 #to generate the choice that will be used for transposition 
        pattern = []
        pattern1 = [0,1,2,3]
        pattern2 = [1,0,2,3]
        pattern3= [2,0,1,3]
        pattern4= [0,2,1,3]
        pattern5= [1,2,0,3]
        pattern6= [2,1,0,3]
        pattern7= [2,1,3,0]
        pattern8= [1,2,3,0]
        pattern9= [3,2,1,0]
        pattern10= [2,3,1,0]
        
        if (choice == 0):
            pattern = pattern10
        elif (choice == 1):
            pattern = pattern1
        elif (choice == 2):
            pattern = pattern2
        elif (choice == 3):
            pattern = pattern3
        elif (choice == 4):
            pattern = pattern4
        elif (choice == 5):
            pattern = pattern5
        elif (choice == 6):
            pattern = pattern6
        elif (choice == 7):
            pattern = pattern7
        elif (choice == 8):
            pattern = pattern8
        elif (choice == 9):
            pattern = pattern9 
        
        L = len(realText)
        
        mL = L % 4
        rows = (L - mL)/2
        
        count =1;
        
        column0 =[]
        column1 =[]
        column2 =[]
        column3 =[]
        outText=[]
        
        if (mL == 1) and (L == 9):
        
            for eachLetter in realText:
             
             if count <= 2:
                 column0.append(eachLetter)
                 # print(column0)
                 
             elif count <= 4 and count > 2:
                 column1.append(eachLetter) 
                
             elif count <= 7 and count > 4:
                 column2.append(eachLetter)
                      
             elif count > 7:
                 column3.append(eachLetter)
                 
             count = count + 1
                
            for i in range(4):
                if i == pattern[0]: #1
                    outText = outText+column3
                elif i == pattern[1]: #2
                    outText = outText+column1
                elif i == pattern[2]: #3
                    outText = outText+column0
                elif i == pattern[3]: #0
                    outText = outText+column2
    
            outText = ''.join(outText)
            
            count = 1
            
            column0 = []
            column1 = []
            column2 = []
            column3 = []
        
            finalText = ''
            
            term = []
            
            rows = 0
            j = 0
            
            
            while rows <= 2:
                
                for i in range(4):
                    
                    term = outText[j]
                   
                    finalText =  finalText + term
                    
                    if i == 0 and rows == 2:
                        break
                    
                    if i == 0:
                        j = j + 3 
                    
                    elif i == 3 and rows == 0:
                        j = 1
                        
                    elif i == 3 and rows == 1:
                        j = 2
                        
                    else: 
                        j = j + 2 
            
                rows = rows + 1
                i = 0
                
                
        elif (mL == 2) and (L == 6):
            
            for eachLetter in realText:
             
             if count <= 1:
                 column0.append(eachLetter)
                 
             elif count <= 3 and count > 1:
                 column1.append(eachLetter) 
                
             elif count <= 5 and count > 3:
                 column2.append(eachLetter)
                      
             elif count > 5:
                 column3.append(eachLetter)
                 
             count = count + 1           
            
            for i in range(4):
                if i == pattern[0]:
                    outText = outText+column3
                elif i == pattern[1]:
                    outText = outText+column1
                elif i == pattern[2]:
                    outText = outText+column0
                elif i == pattern[3]:
                    outText = outText+column2
            
            outText = ''.join(outText)
            
            count = 1
            
            column0 = []
            column1 = []
            column2 = []
            column3 = []
            
            finalText = ''
            
            term = []
            
            rows = 0
            j = 0
            
            
            while rows <= 1:
                
                for i in range(4):
                    
                    term = outText[j]
                   
                    finalText= finalText + term
                    
                    if i == 1 and rows == 1:
                        break

                    if i == 3 and rows == 0:
                        j = 1
                        
                    elif i == 2 and rows == 0:
                        j = j + 1
                        
                    elif i == 3 and rows == 0:
                        j = 2
                        
                    else: 
                        j = j + 2 
            
                # print("rows",rows)
                rows = rows + 1
                i = 0
            
        elif (mL == 2) and (L == 10): 

            for eachLetter in realText:
             
             if count <= 2:
                 column0.append(eachLetter)
                 
             elif count <= 5 and count > 2:
                 column1.append(eachLetter) 
                
             elif count <= 8 and count > 5:
                 column2.append(eachLetter)
                      
             elif count > 8:
                 column3.append(eachLetter)
                 
             count = count + 1
                
            for i in range(4):
                if i == pattern[0]:
                    outText = outText+column3
                elif i == pattern[1]:
                    outText = outText+column1
                elif i == pattern[2]:
                    outText = outText+column0
                elif i == pattern[3]:
                    outText = outText+column2
    
            outText = ''.join(outText)
            
            count = 1
            
            column0 = []
            column1 = []
            column2 = []
            column3 = []
        
            finalText = ''
            
            term = []
            
            rows = 0
            j = 0
            
            
            while rows <= 2:
                
                for i in range(4):
                    
                    term = outText[j]
                   
                    finalText = finalText + term
                    
                    if i == 1 and rows == 2:
                        break
                    
                    if i == 2:
                        j = j + 2
                    
                    elif i == 3 and rows == 0:
                        j = 1
                        
                    elif i == 3 and rows == 1:
                        j = 2
                        
                    else: 
                        j = j + 3
            
                rows = rows + 1
                i = 0
            
        elif (mL == 2) and (L == 6):
            
            for eachLetter in realText:
             
             if count <= 1:
                 column0.append(eachLetter)
                 # print(column0)
                 
             elif count <= 3 and count > 1:
                 column1.append(eachLetter) 
                 # print(column1)
                
             elif count <= 5 and count > 3:
                 column2.append(eachLetter)
                 # print(column2)
                      
             elif count > 5:
                 column3.append(eachLetter)
                 # print(column3)
                 
             count = count + 1           
            
            for i in range(4):
                if i == pattern[0]:
                    outText = outText+column3
                elif i == pattern[1]:
                    outText = outText+column1
                elif i == pattern[2]:
                    outText = outText+column0
                elif i == pattern[3]:
                    outText = outText+column2
            
            outText = ''.join(outText)
            
            count = 1
            
            column0 = []
            column1 = []
            column2 = []
            column3 = []
            
            finalText = ''
            
            term = []
            
            rows = 0
            j = 0
            
            
            while rows <= 1:
                
                for i in range(4):
                    
                    term = outText[j]
                   
                    finalText = finalText + term
                    
                    if i == 1 and rows == 1:
                        break
    
        
                    if i == 3 and rows == 0:
                        j = 1
                        
                    elif i == 2 and rows == 0:
                        j = j + 1
                        
                    elif i == 3 and rows == 0:
                        j = 2
                        
                    else: 
                        j = j + 2 
            
                # print("rows",rows)
                rows = rows + 1
                i = 0
            
        elif (mL == 0) and (L == 8):
            
            for eachLetter in realText:
             
             if count <= 2:
                 column0.append(eachLetter)
                 
             elif count <= 4 and count > 2:
                 column1.append(eachLetter) 
                
             elif count <= 6 and count > 4:
                 column2.append(eachLetter)
                      
             elif count > 6:
                 column3.append(eachLetter)
                 
             count = count + 1           
            
            for i in range(4):
                if i == pattern[0]:
                    outText = outText+column3
                elif i == pattern[1]:
                    outText = outText+column1
                elif i == pattern[2]:
                    outText = outText+column0
                elif i == pattern[3]:
                    outText = outText+column2
      
            outText = ''.join(outText)
            
            count = 1
            
            column0 = []
            column1 = []
            column2 = []
            column3 = []
            
            finalText = ''
            
            term = []
            
            rows = 0
            j = 0
            
            
            while rows <= 1:
                
                for i in range(4):
                    
                    term = outText[j]
                   
                    finalText = finalText + term

                    if i == 3 and rows == 0:
                        j = 1
      
                    else: 
                        j = j + 2 
            
                # print("rows",rows)
                rows = rows + 1
                i = 0
                     
        if (L == 8):
            final_split = ' '.join(finalText[i:i+4] for i in range(0,L+1,4))
            
        elif (L == 9):
            split1 = ' '.join(finalText[i:i+4] for i in range(0,3,4))
            split2 = ' '.join(finalText[i:i+5] for i in range(4,9,5))
            final_split = ''.join(split1+" "+split2)
            
        elif (L == 10):
            split1 = ' '.join(finalText[i:i+5] for i in range(0,4,5))
            split2 = ' '.join(finalText[i:i+5] for i in range(5,9,5))
            final_split = ''.join(split1+" "+split2)
        elif (L == 6):
            final_split = finalText
            
    print(final_split)
            
    return final_split


def caesar_decrypt(realText, step):
    outText = []
    cryptText = []
    uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numb_list = ['0','1','2','3','4','5','6','7','8','9','-']
    for eachLetter in realText:
        if eachLetter in uppercase:
            index = uppercase.index(eachLetter)
            crypting = (index - step) % 26 
            newLetter = uppercase[crypting]
            outText.append(newLetter)
        elif eachLetter in lowercase:
            index = lowercase.index(eachLetter)
            crypting = (index - step) % 26
            cryptText.append(crypting)
            newLetter = lowercase[crypting]
            outText.append(newLetter) 
        elif eachLetter in numb_list:
            index = numb_list.index(eachLetter)
            crypting = (index - step) % 11
            cryptText.append(crypting)
            newLetter = numb_list[crypting]
            outText.append(newLetter)
            
    # print(outText)
    return outText


def killmenow(code3,key):
    decrypt1 = subs_decrypt(code3,key,7)
    decrypt2 = caesar_decrypt(decrypt1, 8)
    decrypt3 = caesar_decrypt(decrypt2, 4)

    return decrypt3

def main_encryption(message,keys):
    
    encrypted = message
    

    for eachKey in keys:
        if (int(eachKey) == 0):
            encrypted = caesar_encrypt(encrypted, 1)
            
        elif (int(eachKey) == 1):
             encrypted = caesar_encrypt(encrypted, 4)
        
        elif (int(eachKey) == 2):
             encrypted = caesar_encrypt(encrypted, 8)
        
        elif (int(eachKey) == 3):
             encrypted = transposition(encrypted,keys,4)
            
        elif (int(eachKey) == 4):
             encrypted = transposition(encrypted,keys,7)
            
        elif (int(eachKey) == 5):
             encrypted = transposition(encrypted,keys,9)
            
        elif (int(eachKey) == 6):
             encrypted = transposition(encrypted,keys,5)
            
        elif (int(eachKey) == 7):
             encrypted = substitution(encrypted,keys,7)
            
        elif (int(eachKey) == 8):
             encrypted = substitution(encrypted,keys,8)
            
        elif (int(eachKey) == 9):
             encrypted = substitution(encrypted,keys,9)
    print("Encrypted Text:",encrypted)
             
    return encrypted
    
login_button = tk.Button(master, text="Login", command=Login, font = myfont, height=1, width=10)
login_button.grid(row = 3, column = 1)

QRcode_button = tk.Button(master, text="Scan QRcode", command=QRcode, font = myfont, height=1, width=10)
QRcode_button.grid(row = 3, column = 5)

exit_button = tk.Button(master, text="Done", command=close, font = myfont, height=1, width=10)
exit_button.grid(row = 4, column = 1)

deactivate_button = tk.Button(master, text="Deactivate", command=pause_func, font = myfont, height=1, width=10)
deactivate_button.grid(row = 4, column = 5)

enter_button = tk.Button(master, text="-->", command=enter_func, font = myfont, height=1, width=5)
enter_button.grid(row = 1, column = 5)

# getFile_button = tk.Button(slave, text="Get File", command=decrypt_func, font = myfont, height=1, width=5)
# getFile_button.grid(row = 1, column = 1)

tk.Label(master, text="Operations:", font = myfont).grid(row=6)
Message = "Please login"
operation= tk.Message(master, text = Message, bg="lightgreen",width= 1000)
operation.grid(row = 6, column = 1)

# Message1 = "Hello"
# operation1= tk.Message(slave, text = Message1, bg="lightgreen",width= 1000)
# operation1.grid(row = 3, column = 1)

tk.mainloop()
