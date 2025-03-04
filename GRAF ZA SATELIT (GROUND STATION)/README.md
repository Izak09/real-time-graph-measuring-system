# Satellite Data Visualization

## Overview

This project provides a graphical interface to receive, process, visualize, and store satellite telemetry data in real time from a serial COM port. The data includes altitude, temperature, and pressure readings, which are plotted in real-time. 

## Features

- Reads data from a serial COM port
- Decodes hexadecimal telemetry data
- Visualizes altitude, temperature, and pressure over time
- Saves data in CSV and Excel formats
- Supports real-time data monitoring
- Simple and interactive GUI

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Required Python libraries:
  - PySimpleGUI
  - numpy
  - pandas
  - matplotlib
  - serial
  - openpyxl

### Steps to Install

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/satellite-visualization.git
   cd satellite-visualization
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Application**
   ```bash
   python main.py
   ```
2. The application will start reading satellite data and display real-time graphs.
3. Click **"Save Data"** to store readings in CSV and Excel formats.
4. Click **"Exit"** to close the application.

## Data Format

The incoming data should be in the following format:

```
A8;B0;80;30;C2
```

Each value is hexadecimal and represents:

- Temperature (Hex to Celsius)
- Altitude (Hex to meters, converted to km)
- Pressure (Hex to hPa)

## License

This project is licensed under the MIT License. See `LICENSE` for details.

### PySimpleGUI License

This project uses PySimpleGUI, which is licensed under an open-source license. To comply with PySimpleGUI's terms, ensure you review its license details here: [PySimpleGUI License](https://pypi.org/project/PySimpleGUI/).

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

## Contact

For any questions or suggestions, feel free to open an issue on GitHub.

---

Enjoy visualizing your satellite data! 🚀


