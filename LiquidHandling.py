from supplier_pump import PUMP
import math

class Pump(PUMP):
    """This is a basic wrapper around the original pump class provided by the pump suppliers. It introduces more complex functionality and ease of use."""

    def __init__(self, port, config = 12):
        super().__init__(port, config, address=1, SPM=1, waste_port=12, mode=0)
        """Port: port name communicating wtih pump.
        Config: the number of valves the pump has."""
    
    def ml_speed_to_pulse(self, ml_per_sec:int):
        """Converts speed in ml/s to pulses/s"""
        # By definition (see pump manual) a pulse has a displacement of 0.01mm
        # The total volume of a 30mm syringe is 1 mL
        # Therefore, volume displaced by a pulse is 
        pulse_volume = 1/30 * 0.01
        
        # To get ml/sec to pulse per sec:
        pulse_per_sec = ml_per_sec/pulse_volume
        return int(pulse_per_sec)
    
    def ml_to_position(self, ml:int):
        """Calculates the position the plunger should be placed to draw given volume"""
        # The total volume of the syringe is 1 ml
        # There are two resolutions (0.01mm and 0.00125mm)
        
        # A placeholder variable to store resolution.   
        scale = None
        
        # If no pump.scalling attribute has been set, the pump manual states the standard step is set to a 0.01 resolution 
        try:
            if int(self.scalling) == 0:
                scale = 0.01
            elif int(self.scalling) == 1:
                scale = 0.00125
        except:
            scale = 0.01

        # The total length of the syringe is 30 mm
        # The resolution is the size of the step in mm
        # Therefore the volume of a step is:
        step_volume = 1/30 * scale

        # Divide volume by volume of single step to get the number of steps
        no_steps = ml/step_volume
        return no_steps
    
    def move(self, volume: float, speed:float = 0.05):
        """Moves plunger to aspirate / dispense liquid
        volume_ml: the volume in ml to draw in/out
        speed: ml/sec (max is 0.53)"""

        position = self.ml_to_position(volume)
        converted_speed = self.ml_speed_to_pulse(speed)
        
        # For project purposes movement will always be 'ABS', the position given as mL to draw, and speed in ml/s
        super().move(position=position, movement='ABS', speed=converted_speed)

    def switch(self, position, force=False):
        """Changes valve position."""

        # All switchs will move based on shortest path ('ANY').
        super().switch(position, 'ANY', force) 
    
    def transfer(self, from_position = int, to_position = int, volume = float, dispense_speed: int=0.5, aspirate_speed: int=0.05):
        """Transfers liquid from one valve position to another based on shortest switch.
        from_position: valve location to aspirate.
        to_position: valve location to dispense
        volume: volume to transfer in mL
        dispense_speed: speed to dispense in mL/sec
        aspirate_speed: speed to aspirate in mL/sec
        """
        
        SyringeCapacity = int(self.SET_SYRINGE_VOLUME)                                  # Can change if syringes are swapped.
        FullSyringes = math.floor(volume/SyringeCapacity)                               # Calculates number of full aspirations required, floor(x) returns largest integer not greater than x.
        PartialSyringes = float(volume%SyringeCapacity)                                 # Calculates if partial aspiration is required. i.e. < 1mL for 1mL syringe.
        
        transfer_iterations = 0
        
        while FullSyringes > 0:                                                         # Transfers however many full syringes are required. 
            self.switch(from_position)                                                  # Pump moves to position where pick up from.
            self.move(SyringeCapacity, aspirate_speed)                                  # Picks up liquid at from_position.
            self.switch(to_position)                                                    # Pump moves to position where it'll dispense.
            self.move(0, dispense_speed)                                                # Pump dispenses picked up liquid.
            transfer_iterations += 1
            print(f'\nTransferred {transfer_iterations} mL out of {volume} mL\n')
            FullSyringes -= 1
        while PartialSyringes > 0:                                                      # Transfers the remainder.
            self.switch(from_position)
            self.move(PartialSyringes, aspirate_speed)
            self.switch(to_position)
            self.move(0, dispense_speed)
            PartialSyringes = 0

    def shutdown(self):
        """Shutting down pumps involves disconnecting them."""
        self.disconnect()

if __name__=='__main__':
    # Example use
    pump = Pump('COM1', 12)
    pump.switch(3)
    pump.move(1, 0.1)
    pump.transfer(4, 12, 3.1, 1)
    pass
