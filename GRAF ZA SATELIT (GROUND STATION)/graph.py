import PySimpleGUI as sg
import numpy as np
import pandas as pd
import socket
import threading
import time
import serial
from openpyxl.drawing.image import Image 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

time_values = []
altitude_values = []
temperature_values = []
pressure_values = []
latitude_values = []
longitude_values = []

# Set the COM port and baudrate for serial communication (in my case its COM5 and baud rate: 115200
try:
    ser = serial.Serial('COM4', 9600, timeout=1)
    ser.flush()
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

simulation_mode = False  # Set to False to read real-time data

def read_com_port():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        return data
    return None

# Function to decode the satellite data (hexadecimal to decimal conversion)
def decode_data(data):
    try:
        # Split the data by ';' (assuming format like A8;B0;80;30;C2)
        parts = data.split(';')
        parts = [part for part in parts if part]
        
        # If there are not exactly 5 VALID parts, return error message
        if len(parts) != 5:
        print(f"Data format error: {data}")
        return None, None, None, None, None
        
        # Decode the hexadecimal values into integers
        temp_data = int(parts[0], 16) 
        altitude_data = int(parts[1], 16) / 1000
        pressure_data = int(parts[2], 16)  
        gps_data = parts[3]
        return temp_data, pressure_data, altitude_data, gps_data, parts[4]
    except Exception as e:
        print(f"Error decoding data: {e}")
        return None, None, None, None, None

#Function to extract GPS data from NMEA string
#Also some additional exeception handlinng from NMEA string
jef extract_gps_coordinates(gps_data)
    try:
        if gps_data-startsWith("$GPGGA") or gps_data.startsWith("$GPRMC"):
            msg = pymea2.parse(gps_data)
            if hasattr(msg, 'lattitude') and hasattr(msg, 'longitude'):
                return msg.latitude, msg.longitude
        return None, None


def listen_for_data():
    global time_values, altitude_values, temperature_values, pressure_values, latitude_values, longitude_values
    while not simulation_mode:
        data = read_com_port()
        if data:
                temp_data, pressure_data, altitude_data = decode_data(data) # Decode values from hexadecimal
                
                # Add the decoded data to the lists
                if temp_data is not None and pressure_data is not None and altitude_data is not None:
                    current_time = int(time.time())  # Convert the whole number using system type
                    time_values.append(current_time)
                    altitude_values.append(altitude_data)
                    temperature_values.append(temp_data)
                    pressure_values.append(pressure_data)
            except Exception as e:
                print(f"Error processing data: {e}")
        time.sleep(0.1)

# Function to update the graph with real-time data
def update_graph(window):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 8))

    ax1.plot(time_values, temperature_values, color='blue')
    ax1.set_title('Temperature vs Time')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Temperature (\u00b0C)')

    ax2.plot(time_values, altitude_values, color='red')
    ax2.set_title('Altitude vs Time')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Altitude (km)')

    ax3.plot(time_values, pressure_values, color='green')
    ax3.set_title('Pressure vs Time')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Pressure (hPa)')

    for canvas in window['-CANVAS_TEMP-'].TKCanvas.winfo_children():
        canvas.destroy()

    canvas_elem = window['-CANVAS_TEMP-']
    canvas_fig = FigureCanvasTkAgg(fig, canvas_elem.TKCanvas)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack()

    plt.close()

# Function to save data to CSV
def save_data_to_csv():
    data = {'Time (s)': time_values, 'Altitude (km)': altitude_values, 'Temperature (C)': temperature_values, 'Pressure (hPa)': pressure_values}
    df = pd.DataFrame(data)
    df.to_csv("satellite_data.csv", index=False, mode='w', header=True)
def save_data_to_excel():
    # Format time values to a readable date-time format
    data = {
        'Time (s)': [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)) for t in time_values],  # Format time
        'Altitude (km)': altitude_values,
        'Temperature (C)': temperature_values,
        'Pressure (hPa)': pressure_values
    }
    df = pd.DataFrame(data)

    try:
        excel_writer = pd.ExcelWriter('satellite_data.xlsx', engine='openpyxl', mode='a')
        df.to_excel(excel_writer, index=False, sheet_name="Data")
        excel_writer.save()
    except FileNotFoundError:
        df.to_excel('satellite_data.xlsx', index=False, sheet_name="Data")

layout = [
    [sg.Text('Satellite Data Visualization', font=('Helvetica', 20))],
    [sg.Canvas(key='-CANVAS_TEMP-', size=(600, 400), background_color='white')],
    [sg.Button('Save Data'), sg.Button('Exit')]
]

window = sg.Window('Vizualizacija', layout, finalize=True)

# Start the thread to listen for satellite data from the COM port
threading.Thread(target=listen_for_data, daemon=True).start()

while True:
    event, values = window.read(timeout=1000)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Save Data':
        save_data_to_csv()
        save_data_to_excel()
    update_graph(window)
window.close()
