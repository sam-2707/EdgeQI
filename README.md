EDGE-QI: An Energy and QoS-Aware Intelligent Edge Framework
This repository contains the Python implementation of EDGE-QI, an intelligent framework for edge computing designed for modern IoT systems. This project is based on the research paper "EDGE-QI: An Energy and QoS-Aware Intelligent Edge Framework for Adaptive IoT Task Scheduling".

EDGE-QI enables adaptive task scheduling, lightweight ML inference, and intelligent data summarization by prioritizing tasks based on context, battery status, and network conditions. This ensures optimal system responsiveness while minimizing redundant communication and saving energy.

Key Features
The framework is designed to deliver significant improvements over traditional edge computing approaches:

⚡️ Adaptive Task Scheduling: A priority-driven scheduler dynamically executes, defers, or skips tasks based on real-time system conditions.

🔋 Energy-Aware Monitoring: The system monitors device energy levels and adjusts its behavior to extend battery life, skipping non-critical tasks when energy is low.

🌐 QoS-Aware Network Monitoring: By monitoring network latency, the scheduler ensures that high-priority tasks are executed when the network quality is sufficient, improving reliability.

🧠 Intelligent Data Summarization: To save bandwidth and energy, the framework only transmits data when a significant change or anomaly is detected, filtering out redundant information.


🗣️ MQTT-Based Communication: Utilizes the lightweight and scalable MQTT protocol for efficient device-to-server communication, ideal for constrained IoT environments.

🤖 Edge-Based ML Inference: Supports running lightweight machine learning models directly on the edge device to reduce latency and enable real-time anomaly detection.

System Architecture
The project is organized into a modular and scalable directory structure:

EdgeQI/
│
├── App/                # Application Layer (Subscriber, Dashboard)
├── Core/               # Core framework components
│   ├── communication/
│   ├── monitor/
│   ├── scheduler/
│   └── summarizer/
├── ML/                 # Machine Learning models and tasks
│   ├── models/
│   └── tasks/
├── hardware/           # Hardware-specific code (e.g., Raspberry Pi)
├── tests/              # Unit tests for the framework
│
├── main.py             # Main application entry point
└── requirements.txt    # Project dependencies
Getting Started
Follow these steps to set up and run the EDGE-QI simulation on your local machine.

Prerequisites
Python 3.10+

An MQTT Broker: The framework requires a running MQTT broker. Mosquitto is a popular choice.

Download and install Mosquitto.

After installation, ensure the Mosquitto service is running and accessible on localhost:1883.

Configure your firewall to allow traffic on TCP port 1883.

Installation and Setup
Clone the repository:

Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Create a virtual environment (recommended):

Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required Python packages:

Bash

pip install -r requirements.txt
Running the Simulation
To see the framework in action, you need to run two scripts in separate terminals.

Terminal 1: Start the MQTT Subscriber

This script listens for and displays the results published by the edge device.

Bash

python App/subscriber.py
You should see the message: [Subscriber] Connected to broker.

Terminal 2: Start the EDGE-QI Main Application

This script initializes all the components and starts the intelligent scheduler.

Bash

python main.py
Expected Output
In the main.py terminal, you will see the scheduler initializing, executing tasks, and publishing results.

Simultaneously, in the subscriber.py terminal, you will see the JSON-formatted messages being received from the MQTT broker.

Project Status
The project is currently in the simulation phase. The core framework, including the intelligent scheduler, monitors, and summarizer, is fully implemented and functional in a simulated environment.

Future Work
The next steps to advance this project from simulation to a real-world application include:

Implement Quality-Aware Inference: Integrate logic into the scheduler to dynamically switch between different ML model versions (e.g., full-precision vs. quantized) based on resource availability.

Develop the Application Dashboard: Build a web-based dashboard using a framework like Streamlit or Dash to visualize the incoming data in real-time.

Integrate Real Hardware: Replace the simulated sensor data with real data from hardware sensors connected to a Raspberry Pi or NVIDIA Jetson Nano.

Expand Unit Tests: Add comprehensive unit and integration tests to ensure the reliability and robustness of the framework.

Citation
This project is an implementation of the concepts presented in the following paper:

S. K. Sistla and S. Tilak, "EDGE-QI: An Energy and QoS-Aware Intelligent Edge Framework for Adaptive IoT Task Scheduling." 
