# Car Telemetry Simulation

This project simulates the telemetry data for three different cars ("Jason", "James", and "Johny") traveling along predefined routes. The data includes GPS coordinates, temperature, speed, tire pressure, and various alerts, which are sent to Azure IoT Hub.

Additionally, you'll need an Azure IoT Hub instance to connect to. Make sure you have the connection strings for your IoT devices.

## Table of Contents
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Simulation](#running-the-simulation)
- [Project Structure](#project-structure)

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/downloads)

Additionally, you'll need an Azure IoT Hub instance to connect to. Make sure you have the connection strings for your IoT devices.

## Installation

### 1. Clone the Repository

To get started, clone this repository to your local machine using Git:

```sh
git clone https://github.com/aserbezo/IoT-Device-Simulator.git
```

###  2. Create a Virtual Environment
Create a virtual environment to isolate the project dependencies:

```sh python -m venv venv
```
Activate the virtual environment:
```sh
.\venv\Scripts\activate
```


### 3. Set Up Environment Variables 
Create a .env file in the root directory of the project and add your Azure IoT Hub device connection strings. The .env file should look like this:

- jasonstatham_connection_string=Your_Jason_IoT_Hub_Connection_String
- jamesbond_connection_string=Your_James_IoT_Hub_Connection_String
- johnyenglish_connection_string=Your_Johny_IoT_Hub_Connection_String


### 4. Install Python Dependencies

Install the required Python packages using pip:
```sh
pip install -r requirements.txt
```

Make sure the requirements.txt file contains the following dependencies:

- python-dotenv
- azure-iot-device


### 5. Running the Simulation

To start the simulation, run the following command:

```bash
python main.py
```

The script will simulate telemetry data for three cars, sending data to the Azure IoT Hub at the specified intervals.


### 6. Project Structure
```
IoT-Device-Simulator/
│
├── routes/
│   ├── sofia-burgas-route.json
│   ├── sofia-varna-route.json
│   └── sofia-vidin-route.json
│
├── main.py
├── requirements.txt
└── README.md
```

- routes/: Contains JSON files that define the GPS coordinates for the car routes.
- main.py: The main script that simulates car telemetry data and sends it to Azure IoT Hub.
- requirements.txt: A file listing the required Python dependencies.
- README.md: This document.

