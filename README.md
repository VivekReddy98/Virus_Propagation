# Virus_Propagation
Immunizing a Virus Propagated Time-Varying Contact Network with a limited vaccines using different immunization policies.

## Project Setup Guide:

### Clone and Create a Virtual Environment.
0) Clone this repositiry preferabbly in /home/unityID/ dir
1) Install virtual environment package:
2) sudo apt-get install python-virtualenv
3) Create a virtual environment inside your project directory using 
4) virtualenv -p /usr/bin/python3 project_directory/venv (The second argument is the name of the folder which will be created, you might not want to change it)
5) cd Virus_Propagation
6) source venv/bin/activate (to start the virtual environment)
6) pip install -r requirements.txt (To install required packages)

### Execute your setup.sh to set the required environemt variables.
Note: Edit the setup.sh to match the paths on your machine. (nano set_up.sh)
1) source setup.sh

### Copy datasets folder into the project directory

### Source Code Walkthrough
1) The Source Code is present in Utils folder and packaged as a library.
2) GenerateGraphMatrices.py has Methods to create various Graph related Matrices
3) Simulatory.py has methods to run simualtions
4) ImmunizationPolicies.py has methods written for various Immunization Policies.

### Steps to execute the code.
1) Use Execute.py to run the code (Modify the program to your needs)
2) Virus_propagaion.ipynb has methods written to generate necesary visualizations which are presented in the report.
