import os
import sys
import time
from modified_pump import Pump
from ir_machine import IR_machine

class DigitalDiscoveryReaction():
    """The procedure the pump and IR spectrometer follows to run experiments for the digital discovery paper."""

    def __init__(self, experiment_name, solvent_valve, waste_valve, water_valve, ir_valve, prime_volume):
        self.experiment_name = experiment_name                                          # The name of the experiment, which will also be used to save spectra file names.

        # General experiment information

        # Pump valve information
        self.solvent_valve = solvent_valve                                              # The pump's valve number connected to the solvent flask.
        self.waste_valve = waste_valve                                                  # The pump's valve number connected to the waste flask.
        self.water_valve = water_valve                                                  # The pump's valve number connected to the water flask.
        self.ir_valve = ir_valve                                                        # The pump's valve number connected to the IR machine.

        # Consistant attributes across experiments.
        self.icIR_template_name = 'Digital Discovery Template'                          # The template used to start an icIR machine.
        self.spectra_location = 'Digital Discovery Project\\' + self.experiment_name    # The location where the specta will be saved.
        self.pump_speed = 0.07                                                          # The speeds (ml/min) pumps operate at.
        self.prime_volume = prime_volume                                                # The volume of solvent to prime lines with.

        # Only one pump and an IR machine is required for this project.
        self.pump = Pump('COM1', 12)
        self.ir_machine = IR_machine('opc.tcp://localhost:62552/iCOpcUaServer')

        # Other required attributes
        self.sample_setup_appropiate = False                                            # Boolean to check if system has been set up well for sample preperation.

    def prime_lines(self):
        """Priming solvent->waste and solvent->IR machine lines with solvent."""

        # Priming solvent->waste
        self.pump.transfer(self.solvent_valve, self.waste_valve, self.prime_volume, self.pump_speed, self.pump_speed)
        
        # Priming solvent->IR_machine lines
        self.pump.transfer(self.solvent_valve, self.waste_valve, self.prime_volume, self.pump_speed, self.pump_speed)

    def start_IR_aquisition(self):
        """Starts IR spectra aquisition then waiting 60 seconds collect solvent spectra."""
        self.ir_machine.start_experiment(self.experiment_name, self.icIR_template_name)     # NOTE: its possible to only change the scan time via python. I suggest making a template that has already been set to 2h and 2m scans 
        time.sleep(60)

    def collect_first_sample(self):
        """Analysing the first sample then pausing spectra aquisition."""
        
        # Collecting sample
        self.pump.transfer(self.ir_valve, self.solvent_valve, 1.5)

        # Pausing spectra aquisiton
        self.ir_machine.pause_experiment()
    
    def check_sample_setup(self):
        """Before more smaples are run, the system needs to be setup and checked by the chemist."""
        
        # The first check: if there is enough solvent.
        check_1 = False
        exit_loop = False
        while not exit_loop:
            check_1_input = input("Have you lifted the solvent line above the liquid level? (Yes/No/Exit): ")
            
            if check_1_input.lower() in ['y', 'yes']:
                check_1 = True
                exit_loop = True

            elif check_1_input.lower() in ['e', 'exit']:
                exit_loop = True
            else:
                print('Please add an appropiate input')
                print()

        # The second check: if flasks are setup appropiatly.
        check_2 = False
        exit_loop = False
        if check_1 == True:
            while not exit_loop:
                check_2_input = input("Have you connected the sample flask to the ReactIR? (Yes/No/Exit) : ")
            
            if check_2_input.lower() in ['y', 'yes']:
                self.sample_setup_appropiate = True
                print(self.sample_setup_appropiate)
                exit_loop = True

            elif check_2_input.lower() in ['e', 'exit']:
                exit_loop = True
            else:
                print('Please add an appropiate input')
                print()
    
    def collect_smaples(self):
        """Makes samples and their IR spectra."""
        
        # Seeing if checks have passed.
        if self.sample_setup_appropiate:

            print('Entering repeat loop.')
            time.sleep(5)


            # Making samples
            for _ in range(3): # ETA ~ 4.5h.
                print(f'On repeat {_}')

                # Pump Amide solution through IR.
                self.pump.switch(self.ir_valve)
                self.pump.move(0.9, self.pump_speed)
                if _ == 0:                                      # Resuming IR experiment (which has been previously paused).
                    self.ir_machine.resume_experiment()
                self.pump.switch(self.solvent_valve)
                self.pump.move()

                # Waiting for 3 seconds.
                time.sleep(3)

                # Pump amide back to reactor.
                self.pump.transfer(self.solvent_valve, self.ir_valve, 1, self.pump_speed)
    
    def stop_experiment(self):
        """Stops spectra aquisition, shuts down pumps and ir machine."""
        
        # Stoping spectra aquisition
        self.ir_machine.stop_experiment()

        # Shutting down
        self.ir_machine.shutdown()
        self.pump.shutdown()
    
    def run_experiment(self):
        """Runnning through a complete experiment."""

        self.prime_lines()
        self.start_IR_aquisition()
        self.collect_first_sample()
        self.check_sample_setup()
        self.collect_smaples()
        self.stop_experiment()

if __name__=='__main__':
    print('What si ')