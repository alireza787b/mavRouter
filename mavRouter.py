"""
MavProxy GUI Router V1.0

This Python application provides a graphical user interface (GUI) for routing MAVLink traffic 
from a source to multiple destinations using MAVProxy. The GUI allows users to configure 
the source as either a serial port or a UDP endpoint and set up two destination output ports.

Features:
- Dynamically switch between Serial and UDP source types.
- Configure serial port settings including baud rate.
- Set up two distinct MAVLink output ports.
- Optionally launch MAVProxy's map and console windows.
- Validate user input for both serial and UDP configuration.

Requirements:
- Python 3.x
- tkinter library for the GUI (usually comes with Python).
- MAVProxy must be installed and accessible from the command line.
- Serial or network access to a MAVLink-compatible device.

How to Use:
1. Select the source type (Serial or UDP).
2. If Serial is selected, choose the COM port and set the baud rate.
3. If UDP is selected, enter the UDP endpoint in the format ip:port.
4. Enter the IP and port for the two destination output ports.
5. Check the options for additional windows if needed.
6. Click 'Start' to initiate the MAVProxy routing.
7. Click 'Stop' to terminate the MAVProxy process.

Author:
Alireza Ghaderi
LinkedIn: alireza787b
GitHub Repository: https://github.com/alireza787b/mavRouter

Created: November 2023
Version: 1.0

Please note that this application is intended for users who are familiar with MAVProxy and MAVLink.
Ensure that MAVProxy is correctly installed and configured on your system before using this GUI router.

License:
This project is open-sourced under the MIT license. Feel free to use, modify, and distribute 
as per the license agreement.

Build Binary:
pyinstaller --clean --onefile --add-data "favicon.ico;." --icon=favicon.ico mavRouter.py

"""


import sys
import glob
import serial
import os
import signal
import subprocess
import webbrowser
from tkinter import Tk, Frame, StringVar, Entry, Button, Checkbutton, IntVar, Label, OptionMenu, RAISED, Radiobutton
import re

# Global variable definitions
global comList, udpEntry, baudEnt,label_source, label_baud

def hyperLink(url):
    """Open a hyperlink in the default web browser."""
    webbrowser.open_new(url)   
    
def serial_ports():
    """
    Lists serial port names.

    Returns:
        A list of the serial ports available on the system.
    Raises:
        EnvironmentError: On unsupported or unknown platforms.
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform in ('linux', 'cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            with serial.Serial(port) as s:
                result.append(port)
        except (OSError, serial.SerialException):
            continue
    return result

def create_mavproxy_command(source, port, baud, outPort1, outPort2, mapState, dashState):
    """
    Create the MAVProxy command based on the given parameters.
    """
    comStr = 'mavproxy.py ' if sys.platform in ('linux', 'cygwin', 'darwin') else 'mavproxy.exe '
    
    if source == "Serial":
        if port == "Select Port":
            return "Error: No serial port selected."
        comStr += f' --master={port} --baudrate {baud} '
    else:
        if not is_valid_udp_address(port):
            return "Error: Invalid UDP address format. Use <ip>:<port>."
        comStr += f' --master=udp:{port} '

    comStr += f'--out {outPort1} --out {outPort2} --non-interactive '
    if mapState == 1:
        comStr += ' --map '
    if dashState == 1:
        comStr += ' --console '
    return comStr

def terminate_process(process):
    """
    Terminates a process based on the current platform.

    Args:
        process: The process to terminate.
    """
    if sys.platform.startswith('win'):
        process.send_signal(signal.CTRL_C_EVENT)
    else:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)


def setup_gui():
    app = Tk()
    app.geometry("600x700")  # Adjusted for additional space
    app.title("MavRouter V1.0")

    global comList, udpEntry, baudEnt, label_source, label_baud
    frame_1 = Frame(master=app, padx=10, pady=10)
    frame_1.pack(fill="both", expand=True)

    Label(frame_1, text="MavRouter V1.0", font=("Arial", 16, "bold")).pack(side="top", pady=(0, 10))

    # Source Section
    Label(frame_1, text="Source Configuration", font=("Arial", 12, "bold")).pack(anchor='w')
    frame_source = Frame(master=frame_1)
    frame_source.pack(fill="both", expand=True, pady=(5, 20))

    sourceType = StringVar(value="Serial")
    Label(frame_source, text="Source Type:").pack(anchor='w')
    Radiobutton(frame_source, text="Serial", variable=sourceType, value="Serial", command=lambda: update_source(sourceType)).pack(anchor='w')
    Radiobutton(frame_source, text="UDP", variable=sourceType, value="UDP", command=lambda: update_source(sourceType)).pack(anchor='w')

    label_source = Label(frame_source, text="Serial Port:")
    label_source.pack(anchor='w')
    sourceInput = StringVar(value="Select Port")
    comList = OptionMenu(frame_source, sourceInput, *serial_ports())
    comList.pack(fill="both", anchor='w')

    label_baud = Label(frame_source, text="Baud Rate:")
    baudEnt = Entry(frame_source)
    baudEnt.insert(0, "57600")
    udpEntry = Entry(frame_source)
    udpEntry.insert(0, "172.21.144.1:18570")

    label_baud.pack(anchor='w')
    baudEnt.pack(fill="both", anchor='w')

    # Destination Section
    Label(frame_1, text="Destination Configuration", font=("Arial", 12, "bold")).pack(anchor='w')
    frame_destination = Frame(master=frame_1)
    frame_destination.pack(fill="both", expand=True, pady=(5, 20))

    Label(frame_destination, text="Output Port 1:").pack(anchor='w')
    out1 = Entry(frame_destination)
    out1.insert(0, "127.0.0.1:14540")
    out1.pack(fill="both", anchor='w')

    Label(frame_destination, text="Output Port 2:").pack(anchor='w')
    out2 = Entry(frame_destination)
    out2.insert(0, "127.0.0.1:14550")
    out2.pack(fill="both", anchor='w')

    # Checkboxes and Buttons
    mapStateCheck = IntVar()
    mapCheck = Checkbutton(frame_1, text="Map Window", variable=mapStateCheck)
    mapCheck.pack(anchor='w')

    dashStateCheck = IntVar()
    dashBoardCheck = Checkbutton(frame_1, text="Dashboard GUI Window", variable=dashStateCheck)
    dashBoardCheck.pack(anchor='w')

    start_button = Button(frame_1, text="Start", command=lambda: start_mavproxy(
        sourceType.get(), 
        udpEntry.get() if sourceType.get() == "UDP" else sourceInput.get(),
        baudEnt.get(),
        out1.get(),
        out2.get(),
        mapStateCheck.get(),
        dashStateCheck.get()
    ))
    start_button.pack(fill="both", pady=5)

    stop_button = Button(frame_1, text="Stop", command=stop_mavproxy)
    stop_button.pack(fill="both", pady=5)

    # Footer
    footerLabel = Label(app, text="MavProxy Easy Router GUI V1.0", relief=RAISED)
    footerLabel.pack(side="bottom", fill="x")
    footerLink = Label(app, fg="blue", cursor="hand2", text="GitHub: Alireza787b")
    footerLink.bind("<Button-1>", lambda e: hyperLink("https://github.com/alireza787b"))
    footerLink.pack(side="bottom", fill="x")

    app.mainloop()


def update_source(sourceTypeVar):
    global comList, udpEntry, baudEnt, label_source, label_baud

    if sourceTypeVar.get() == "Serial":
        # Show Serial-related widgets
        label_source.config(text="Serial Port:")
        label_source.pack(anchor='w')
        comList.pack(fill="both", anchor='w')
        label_baud.pack(anchor='w')
        baudEnt.pack(fill="both", anchor='w')
        # Hide UDP-related widget
        udpEntry.pack_forget()
    else:
        # Show UDP-related widget
        label_source.config(text="Source UDP Address:")
        label_source.pack(anchor='w')
        udpEntry.pack(fill="both", anchor='w')
        # Hide Serial-related widgets
        comList.pack_forget()
        label_baud.pack_forget()
        baudEnt.pack_forget()


def is_valid_udp_address(address):
    """
    Validates the UDP address format.

    Args:
        address (str): UDP address in the format 'ip:port'.

    Returns:
        bool: True if valid, False otherwise.
    """
    pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}:\d+$')
    return bool(pattern.match(address))


def create_mavproxy_command(source, port, baud, outPort1, outPort2, mapState, dashState):
    """
    Create the MAVProxy command based on the given parameters.
    """
    comStr = 'mavproxy.py ' if sys.platform in ('linux', 'cygwin', 'darwin') else 'mavproxy.exe '
    
    if source == "Serial":
        if port == "Select Port":
            return "Error: No serial port selected."
        comStr += f' --master={port} --baudrate {baud} '
    else:
        if not port or ':' not in port:
            return "Error: Invalid UDP address format {port}. Use <ip>:<port>."
        comStr += f' --master=udp:{port} '

    comStr += f'--out {outPort1} --out {outPort2} --non-interactive '
    if mapState == 1:
        comStr += ' --map '
    if dashState == 1:
        comStr += ' --console '
    return comStr

def start_mavproxy(source, port, baud, outPort1, outPort2, mapState, dashState):
    """
    Start the Mavproxy process with the specified settings.
    """
    global stateMav
    command = create_mavproxy_command(source, port, baud, outPort1, outPort2, mapState, dashState)
    
    if command.startswith("Error"):
        print(command)  # or use any other method to show the error to the user
        return

    try:
        if stateMav.poll() is None:
            print("Mavproxy is already running. Stopping current instance.")
            terminate_process(stateMav)
    except NameError:
        print("Starting Mavproxy for the first time.")

    if sys.platform.startswith('win'):
        stateMav = subprocess.Popen(command, shell=True)
    else:
        stateMav = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    print(f"Started Mavproxy with command: {command}")



def stop_mavproxy():
    """
    Stop the currently running Mavproxy process.
    """
    global stateMav
    try:
        if stateMav.poll() is None:
            print("Stopping Mavproxy.")
            terminate_process(stateMav)
        else:
            print("Mavproxy is not running.")
    except NameError:
        print("Mavproxy has not been started yet.")

if __name__ == "__main__":
    setup_gui()

