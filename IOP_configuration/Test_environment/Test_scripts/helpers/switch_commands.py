#!/usr/bin/env python3

# Add the source directory to Python path
import sys
import os

# Get the path to the src directory containing the conrad_relaycard package
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conrad-relaycard-master', 'src')
sys.path.insert(0, src_path)

# Now we can import the module using absolute imports
from conrad_relaycard.card import RelayCard
from conrad_relaycard.constants import ComCodes, CommandCodes
from conrad_relaycard.state import RelayState
import re

def extract_switch_com_port_from_batch():
    """Extract SWITCH COM port from run_IOP.bat file"""
    try:
        # Path to run_IOP.bat (3 folders up from current script)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        batch_file_path = os.path.join(current_dir, '..', '..', '..', 'run_IOP.bat')
        batch_file_path = os.path.normpath(batch_file_path)
        
        if not os.path.exists(batch_file_path):
            print(f"Warning: run_IOP.bat not found at {batch_file_path}, using default COM36")
            return 'COM36'
        
        with open(batch_file_path, 'r') as file:
            content = file.read()
            
        # Look for the SWITCH_COM_PORT pattern
        match = re.search(r'set\s+"SWITCH_COM_PORT=([^"]+)"', content)
        if match:
            com_port = match.group(1)
            print(f"Extracted SWITCH COM port from run_IOP.bat: {com_port}")
            return com_port
        else:
            print("Warning: SWITCH_COM_PORT not found in run_IOP.bat, using default COM36")
            return 'COM36'
            
    except Exception as e:
        print(f"Warning: Error reading run_IOP.bat: {e}, using default COM36")
        return 'COM36'

def power_off_HU():
    """Example usage of the RelayCard class."""
    # Create a RelayCard instance with dynamic COM port from run_IOP.bat
    com_port = extract_switch_com_port_from_batch()
    card = RelayCard(com_port)
    card.setup()

    current_state = card.get_ports(1)
    print(f"Current relay state: {current_state}")
    
    port_state = card.get_port(1, 7)
    print(f"Get relay state: {port_state}")
    card.set_port(1, 7, False)

def power_on_HU():
    """Example usage of the RelayCard class."""
    # Create a RelayCard instance with dynamic COM port from run_IOP.bat
    com_port = extract_switch_com_port_from_batch()
    card = RelayCard(com_port)
    card.setup()

    current_state = card.get_ports(1)
    print(f"Current relay state: {current_state}")
    
    port_state = card.get_port(1, 7)
    print(f"Get relay state: {port_state}")
    card.set_port(1, 7, True)
