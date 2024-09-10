
# EternalBlue Simulation Project

## Overview

The **EternalBlue Simulation Project** is a Python-based educational tool that demonstrates a simplified version of the EternalBlue exploit, which was used in the infamous WannaCry ransomware attack. This project is designed to help users understand the nature of the SMBv1 vulnerability (MS17-010), how exploits work, and how modern defenses mitigate such threats. 

**Important:** This project is intended for educational purposes only. It should not be used for any malicious activities. Always use this knowledge to improve security practices and understand the importance of system updates and protections.

## Project Structure

The project is organized into the following components:

- **`README.md`**: Provides an overview of the project, setup instructions, and usage guidelines.
- **`requirements.txt`**: Lists the required Python libraries.
- **`main.py`**: The main entry point of the project.
- **`modules/`**: Contains various modules for different functionalities:
  - **`scanner.py`**: Handles network scanning to detect SMBv1 vulnerabilities.
  - **`exploit_simulator.py`**: Simulates the process of exploiting the SMBv1 vulnerability.
  - **`payload_simulator.py`**: Simulates the delivery of a payload to the target system.
  - **`defense_mechanisms.py`**: Demonstrates how system patches and firewalls prevent exploits.
- **`docs/`**: Contains educational notes and explanations about the exploit and defenses.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/IMAFDI/EternalBlue_Simulation.git
   cd EternalBlue_Simulation
   ```

2. **Create a Virtual Environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Required Libraries:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Main Script:**
   ```bash
   python main.py
   ```

2. **Follow the Prompts:**
   - Enter the IP address of the target system you want to simulate the exploit on.
   - The script will perform the following actions:
     - Scan for SMBv1 vulnerability on the target IP.
     - Check if the system is patched with MS17-010.
     - Check if a firewall is blocking SMBv1 traffic.
     - Simulate the exploit if the system is vulnerable.
     - Simulate payload delivery to the target system.

## Modules

### `scanner.py`
This module scans for systems running SMBv1 by checking if port 445 is open. It uses the nmap library to perform network scans.

### `exploit_simulator.py`
Simulates the process of exploiting the SMBv1 vulnerability. This module connects to the target system's SMBv1 service and sends a simulated exploit payload.

### `payload_simulator.py`
Simulates the delivery of a payload to the target system. This module demonstrates how an attacker might inject a payload remotely.

### `defense_mechanisms.py`
Shows how system defenses such as patches and firewalls block exploit attempts. It assumes the system is either patched with MS17-010 or protected by a firewall.

## Educational Focus
This project provides insights into:
- **Network Scanning**: Understanding how to scan for vulnerabilities in network services.
- **Exploit Simulation**: Learning the concept behind buffer overflow exploits and their impact.
- **Defense Mechanisms**: Demonstrating how system updates and firewalls protect against exploits.
- **Ethical Hacking**: Emphasizing the importance of using knowledge responsibly and focusing on security improvements.

## Contributing
Feel free to contribute to this project by opening issues or submitting pull requests. If you have suggestions for improvements or additional educational content, your contributions are welcome!

## License
This project in not been licensed under any License. You can are free to use and give your inputs.

## Acknowledgements
- **EternalBlue**: Exploit used in the WannaCry ransomware attack, highlighting the importance of cybersecurity.
- **SMBv1 Vulnerability**: The target of this simulation, which underscores the need for timely system updates and security measures.

## Contact
For any questions or concerns, please contact me via github.

**Remember**: This project is for educational purposes only. Do not use this knowledge for illegal activities or unauthorized access to systems. Always adhere to ethical guidelines in cybersecurity practices.
