from cgi import print_directory
from tkinter import *
import asyncio
from turtle import home
from async_tkinter_loop import async_handler, async_mainloop
import sys
import glob
import serial
import os
import signal
import subprocess
import webbrowser
    
def hyperLink(url):
    webbrowser.open_new(url)   
    
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result



app = Tk()
app.iconbitmap("favicon.ico")
app.geometry("500x550")
app.title("Mavproxy GUI Router V.0.2")



def ref_callback():
    options = serial_ports()

    # datatype of menu text
    selectedCom = StringVar()
    print (options)
    # initial menu text
    try:
        selectedCom.set( options[-1] )
    except: 
        options = ["No Available Port"]
        selectedCom.set( options[-1] )
    
def start_callback():
    global stateMav
    try:
        print("Checking State...")
        
        if sys.platform.startswith('win'):
            stateMav.send_signal(signal.CTRL_C_EVENT)
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            os.killpg(os.getpgid(stateMav.pid), signal.SIGTERM)  # Send the signal to all the process groups
        elif sys.platform.startswith('darwin'):
            os.killpg(os.getpgid(stateMav.pid), signal.SIGTERM)  # Send the signal to all the process groups

        else:
            raise EnvironmentError('Unsupported platform')    
        
    except:
        print("Fresh Sart!")
        
    # port = comList.get()
    port = selectedCom.get()
    
    outPort1 = out1.get()
    outPort2 = out2.get()
    baud = baudEnt.get()
    
    if sys.platform.startswith('win'):
        comStr = 'mavproxy.exe '
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        comStr = 'mavproxy.py '
    elif sys.platform.startswith('darwin'):
        comStr = 'mavproxy.py '
    else:
        raise EnvironmentError('Unsupported platform')
    
    comStr += ' --master='+str(port)+' --baudrate '+str(baud)+' --out '+str(outPort1)+' --out '+str(outPort2)+' --non-interactive '
    if mapStateCheck.get() == 1:
        comStr += ' --map '
        
    if dashStateCheck.get() == 1:
        comStr += ' --console '
    #app.withdraw()
    
    
    if sys.platform.startswith('win'):
        stateMav = subprocess.Popen(comStr, shell=True)

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        stateMav = subprocess.Popen(comStr,stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid)
    elif sys.platform.startswith('darwin'):
        stateMav = subprocess.Popen(comStr,stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid)
    else:
        raise EnvironmentError('Unsupported platform')
    
    print(comStr)
    #await os.system(comStr)
    
    
def stop_callback():
    global stateMav
    try:
        print("Already Open. Quiting...")
        
        if sys.platform.startswith('win'):
            stateMav.send_signal(signal.CTRL_C_EVENT)
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            os.killpg(os.getpgid(stateMav.pid), signal.SIGTERM)  # Send the signal to all the process groups
        elif sys.platform.startswith('darwin'):
            os.killpg(os.getpgid(stateMav.pid), signal.SIGTERM)  # Send the signal to all the process groups

        else:
            raise EnvironmentError('Unsupported platform')    
        
        
    except:
        print("Not Open")
        
   


frame_1 = Frame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)



options = serial_ports()
  
# datatype of menu text
selectedCom = StringVar()
  
# initial menu text
try:
    selectedCom.set( options[-1] )
except: 
    options = ["No Available Port"]
    selectedCom.set( options[-1] )
    
comComboList = serial_ports()
comList = OptionMenu(frame_1,selectedCom , *options )
comList.pack(pady=12, padx=10,side="top",fill="both")

baudEnt = Entry(master=frame_1)
baudEnt.insert(0,"57600")
baudEnt.pack(pady=12, padx=10,side="top")




button_1 = Button(master=frame_1, command=lambda: ref_callback(), text="Refresh")
button_1.pack(pady=12, padx=10,side="top")




out1 = Entry(master=frame_1)
out1.insert(0,"127.0.0.1:14540")
out1.pack(pady=12, padx=10,fill="both")


out2 = Entry(master=frame_1)
out2.insert(0,"127.0.0.1:14550")
out2.pack(pady=12, padx=10,fill="both")

mapStateCheck = IntVar()

mapCheck = Checkbutton(master=frame_1,text="Map Window",variable=mapStateCheck, onvalue=1,offvalue=0)
mapCheck.pack(pady=12, padx=10)

dashStateCheck = IntVar()

dashBoardCheck = Checkbutton(master=frame_1,text="Dashboard GUI Window",variable=dashStateCheck, onvalue=1,offvalue=0)
dashBoardCheck.pack(pady=12, padx=10)


button_2 = Button(master=frame_1, command=start_callback, text="Start")
button_2.pack(pady=12, padx=10,side="top",fill="both")

button_2 = Button(master=frame_1, command=stop_callback, text="Stop")
button_2.pack(pady=12, padx=10,side="top",fill="both")

strfooter = StringVar()
strfooter.set("MavProxy Easy Router GUI V.0.2 by Alireza Ghaderi")
footerLabel = Label( app ,textvariable=strfooter, relief=RAISED )




linkFooter = StringVar()
linkFooter.set("GitHub: Alireza787b")

footerLink = Label( app, fg="blue", cursor="hand2" ,textvariable=linkFooter )

footerLink.bind("<Button-1>", lambda e: hyperLink("https://github.com/alireza787b"))
footerLink.pack(side="bottom",fill="x")
footerLabel.pack(side="bottom",fill="x")

async_mainloop(app)