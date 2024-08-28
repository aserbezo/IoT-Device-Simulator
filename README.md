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

```bash
git clone https://github.com/yourusername/car-telemetry-simulation.git
```

### 2. Set Up Environment Variables


#### 1. Install the `python-dotenv` package

To install the `python-dotenv` package, which allows you to read environment variables from a `.env` file in Python, you can use pip, the Python package installer:

```sh
pip install python-dotenv
```
To verify the installation, run:
```sh
pip show python-dotenv
```
- Create a .env file in the root directory of the project

#### 2. Add Your Azure IoT Hub Device Connection Strings

Copy the following names and only change your connection strings:

```sh
  jasonstatham_connection_string= {Your_Jason_IoT_Hub_Connection_String}
  jamesbond_connection_string= {Your_James_IoT_Hub_Connection_String}
  johnyenglish_connection_string={Your_Johny_IoT_Hub_Connection_String}
```

### 3. Install Python Dependencies

Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

Make sure the requirements.txt file contains the following dependencies:

- python-dotenv
- azure-iot-device


### 4. Running the Simulation

To start the simulation, run the following command:

```bash
python main.py
```

The script will simulate telemetry data for three cars, sending data to the Azure IoT Hub at the specified intervals.


### 5. Project Structure
```
car-telemetry-simulation/
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

### 6. Vehicle Status Update

Message sent to Azure IoT Hub:

```json
{
  "vehicle_id": "ABC12347",
  "timestamp": "2024-08-14 11:52:50",
  "location": {
    "latitude": 42.69258944526666,
    "longitude": 23.328606080076582
  },
  "speed": 70,
  "engine_status": {
    "rpm": 2600,
    "temperature": 80
  },
  "battery_status": {
    "voltage": 13.3,
    "charge_state": "charging"
  },
  "tire_pressure": {
    "front_left": 32,
    "front_right": 32,
    "rear_left": 32,
    "rear_right": 32
  },
  "driver_behavior": {
    "acceleration": 3.2,
    "braking": -3.3,
    "seatbelt_status": false
  },
  "alerts": {
    "engine_check": true,
    "low_fuel": false,
    "tire_pressure_low": false,
    "battery_low": true
  }
}




- routes/: Contains JSON files that define the GPS coordinates for the car routes.
- main.py: The main script that simulates car telemetry data and sends it to Azure IoT Hub.
- requirements.txt: A file listing the required Python dependencies.
- README.md: This document.

