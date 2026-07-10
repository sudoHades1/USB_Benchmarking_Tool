# USB_Benchmarking_Tool_for_Linux
This tool was created with the help of ChatGPT. I'm just starting to learn how to code and create an automation tool.

This tool acts as continuous speed test benchmarking tool for multiple drives that generates sequential read/write and random read/write reports.

INSTRUCTIONS ON HOW TO USE:

1. Download Python and install pip
sudo apt-get install python3
sudo apt-get install python3-pip

2. Create a virtual environment
python3 -m venv .venv (or your preferred virtual environment name)
source .venv/bin/activate

4. Install the dependencies
pip install -r requirements.txt

5. Run the benchmarking tool
python3 main.py


NOTE: This tool can only provide accurate results using exFAT filesystem configuration. I will update this soon to be available in all filesystem configuration

The config.yaml can be modified to match your preferred test parameters such as number of runs and file size to test.
