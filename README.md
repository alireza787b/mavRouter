
# MavRouter V1.0

![image](https://github.com/alireza787b/mavRouter/assets/30341941/31c99696-2141-4a52-abc2-b4c1dca39158)

MavRouter is an open-source graphical user interface (GUI) application designed to facilitate the routing of MAVLink traffic. It enables users to configure the source as either a serial port or a UDP endpoint and set up two destination output ports, simplifying the process of interfacing with MAVProxy for UAV telemetry and command protocols.

## Features

- Switch between Serial and UDP source types.
- Configure serial port settings including baud rate.
- Set up two distinct MAVLink output ports.
- Optional integration with MAVProxy's map and console windows.
- User input validation for serial and UDP configurations.

## Installation

### Prerequisites

- Python 3.x
- [MAVProxy](https://ardupilot.org/mavproxy/), which can be installed via pip or from the official site.


### Getting Started with Source Code

If you prefer to use the source code directly, you can clone the repository and set up the environment as follows:

1. **Clone the Repository**
   Clone MavRouter to your local machine using Git:
   ```bash
   git clone https://github.com/alireza787b/mavRouter.git
   ```

2. **Install Dependencies**
   Navigate to the cloned directory and install the required dependencies:
   ```bash
   cd mavRouter
   pip install -r requirements.txt
   ```

   **Note for Ubuntu Users:** If you encounter an error related to `tkinter`, you may need to install it separately. This can be done using the following command:
   ```bash
   sudo apt-get install python3-tk
   ```

3. **Run the Application**
   Launch MavRouter by executing the Python script:
   ```bash
   python mavRouter.py
   ```



### Executables

Pre-built binaries for macOS and Windows and Ubuntu 22.04 are available on the [releases page](https://github.com/alireza787b/mavRouter/releases). These executables include all necessary dependencies, offering a straightforward setup.

## Usage

MavRouter can be used in various scenarios, such as:

- Redirecting MAVLink data from UAV hardware to a software instance running on WSL, MAVSDK, or MAVROS.
- Routing telemetry data from Pixhawk to devices within a Wi-Fi network.
- Supporting UAV software development and testing by providing MAVLink data to network endpoints.

## Contribution

Contributions to MavRouter are welcome. Feel free to fork the repository, make changes, and submit pull requests.

## Author

**Alireza Ghaderi**

- [LinkedIn](https://www.linkedin.com/in/alireza787b)
- [GitHub](https://github.com/alireza787b)

## License

MavRouter is released under the MIT license. Feel free to use, modify, and distribute it as per the license agreement.

---


