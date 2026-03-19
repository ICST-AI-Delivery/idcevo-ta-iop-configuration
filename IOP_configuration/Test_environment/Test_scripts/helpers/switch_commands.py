#!/usr/bin/env python3

# Now we can import the module using absolute imports
from conrad_relaycard.card import RelayCard
from conrad_relaycard.constants import ComCodes, CommandCodes
from conrad_relaycard.state import RelayState

def power_off_HU():
    """Example usage of the RelayCard class."""
    # Create a RelayCard instance (replace 'COM36' with your actual port)
    card = RelayCard('COM36')
    card.setup()

    current_state = card.get_ports(1)
    print(f"Current relay state: {current_state}")
    
    port_state = card.get_port(1, 7)
    print(f"Get relay state: {port_state}")
    card.set_port(1, 7, False)

def power_on_HU():
    """Example usage of the RelayCard class."""
    # Create a RelayCard instance (replace 'COM36' with your actual port)
    card = RelayCard('COM36')
    card.setup()

    current_state = card.get_ports(1)
    print(f"Current relay state: {current_state}")
    
    port_state = card.get_port(1, 7)
    print(f"Get relay state: {port_state}")
    card.set_port(1, 7, True)