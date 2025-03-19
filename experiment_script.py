import os
import sys
import time
from modified_pump import Pump
from ir_machine import IR_machine

class SensingSensitivityReaction():
    """The procedure the pump and IR spectrometer follows to run experiments for the digital discovery paper."""

    def __init__(self, experiment_name, icIR_template_name, spectra_location, solvent_valve, waste_valve, water_valve, air_valve, ir_valve, prime_volume, prime_speed, solvent_sample_volume, solvent_pump_speed, solvent_spectrum_time, sample_volume, sample_spectrum_time, sample_pump_speed, experiment_run_time, clean_speed):
        self.experiment_name = experiment_name                                          # The name of the experiment, which will also be used to save spectra file names.

        # Pump valve information
        self.solvent_valve = solvent_valve                                              # The pump's valve number connected to the solvent flask.
        self.wet_solvent_valve = wet_solvent_valve                                      # The pump's valve number connected to the wet solvent flask.
        self.waste_valve = waste_valve                                                  # The pump's valve number connected to the waste flask.
        self.water_valve = water_valve                                                  # The pump's valve number connected to the water flask.
        self.ir_valve = ir_valve                                                        # The pump's valve number connected to the IR machine.
        self.air_valve = air_valve                                                      # The pump's valve number connected to air.

        # Consistant attributes across experiments.
        self.icIR_template_name = icIR_template_name                                    # The template used to start an icIR machine.
        self.spectra_location = spectra_location                                        # The location where the specta will be saved.

        # Priming information
        self.prime_speed = prime_speed                                                  # The speed of the pumps (mL/min) to prime lines with.   
        self.prime_volume = prime_volume                                                # The volume of solvent to prime lines with.

        # Solvent sample information
        self.solvent_sample_volume = solvent_sample_volume                              # The volume (mL) of solvent required to reach IR machine to collect spectra
        self.solvent_spectrum_time = solvent_spectrum_time                              # The time (s) the IR experiment (to collect solvent spectrum) should run for.
        self.solvent_pump_speed = solvent_pump_speed                                    # The speed (mL/min) pumpd draw and collect solvent sample.

        # Sample information
        self.sample_volume = sample_volume                                              # The volumes (mL) of the samples to be drawn by the pump.
        self.sample_spectrum_time = sample_spectrum_time                                # The time (s) the IR experiment (to collect sample spectrum) should run for.
        self.sample_pump_speed = sample_pump_speed                                      # The speed (mL/min) pumps draw and collect samples.

        # Experiment information
        self.experiment_run_time = experiment_run_time                                  # The time (s) the experiment should last for. It dictates how many samples can be sent in this time interval.

        # Cleaning information
        self.clean_speed = clean_speed                                                  # The speed (mL/min) pumps draw and dispense to clean lines.
        
        self.wet_solvent_clean_volume = wet_solvent_clean_volume                        # The volume (mL) of wet solvent to clean lines with. 
        self.water_clean_volume = water_clean_volume                                    # The volume (mL) of water to clean lines with.
        self.solvent_clean_volume = solvent_clean_volume                                # The volume (mL) of solvent to clean lines with.
        self.air_clean_volume = air_clean_volume                                        # The volume (mL) of air to dry lines with.
        
        
        # Only one pump and an IR machine is required for this project.
        self.pump = Pump('COM1', 12)
        self.ir_machine = IR_machine('opc.tcp://localhost:62552/iCOpcUaServer')

        # Other required attributes
        self.sample_setup_appropiate = False                                            # Boolean to check if system has been set up well for sample preperation.
    
    def prime_lines(self):
        """Priming solvent->waste lines with solvent."""

        print('Priming solvent->waste lines')
        print()
        # Priming solvent->waste
        self.pump.transfer(
            from_position=self.solvent_valve, 
            to_position=self.waste_valve,
            volume=self.prime_volume, 
            aspirate_speed=self.prime_speed,
            dispense_speed=self.prime_speed)

    def collect_solvent_sample(self):
        """Collects the spectrum of the solvent."""
        
        # Transfering sample volume
        print('Transfering solvent to IR machine for solvent spectra collection')
        self.pump.transfer(
            from_position=self.solvent_valve,
            to_position=self.ir_valve,
            volume=self.solvent_sample_volume,
            aspirate_speed=self.solvent_pump_speed,
            dispense_speed=self.solvent_pump_speed)
        
        # Strating icIR experiment 
        print('Starting icIR experiment')
        self.ir_machine.start_experiment(self.spectra_location, self.icIR_template_name)

        # Collecting solvent spectra
        print('Collecting solvent sample spectra')
        time.sleep(self.solvent_spectrum_time)

        self.ir_machine.pause_experiment()

        # transfer from IR back to solvent
        print('Transfering solvent sample back to ir')
        self.pump.transfer(
            from_position=self.ir_valve,
            to_position=self.solvent_valve,
            volume=self.solvent_sample_volume*1.5,
            aspirate_speed=self.solvent_pump_speed,
            dispense_speed=self.solvent_pump_speed
        )
        
        print()
    
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
                print()

            elif check_1_input.lower() in ['e', 'exit']:
                exit_loop = True

            elif check_1_input.lower() in ['no', 'n']:
                print('Please make sure to lift the solvent line above the liquid level.')

            else:
                print('Please add an appropiate input')

        # The second check: if flasks are setup appropiatly.
        exit_loop = False
        if check_1 == True:
            while not exit_loop:
                check_2_input = input("Have you connected the sample flask to the ReactIR? (Yes/No/Exit): ")
            
                if check_2_input.lower() in ['y', 'yes']:
                    self.sample_setup_appropiate = True
                    print(self.sample_setup_appropiate)
                    exit_loop = True
                    print()

                elif check_2_input.lower() in ['e', 'exit']:
                    exit_loop = True

                elif check_2_input.lower() in ['no', 'n']:
                    print('Please make sure to connect the sample flask to the ReactIR.')

                else:
                    print('Please add an appropiate input')
        print()
        
    def collect_sample(self):
        """Collecting the spectra of a sample"""

        # Aspirate from Ir machine
        print('Aspirating the smaple from IR machine.')
        self.pump.switch(self.ir_valve)
        self.pump.move(self.sample_volume, self.sample_pump_speed)

        # resume spectra aquisition
        print('Collecting the spectrum of the sample.')
        self.ir_machine.resume_experiment()
        time.sleep(self.sample_spectrum_time)
        self.ir_machine.pause_experiment()
        
        # Dispensing back the drawn volume
        print('Returning the sample back to IR.')
        self.pump.move(0, self.sample_pump_speed)

        print()
        
    def collect_first_sample(self):
        """Collecting spectra of smaple."""
        
        print('Collecting the spectra of the first sample')
        self.collect_sample()
        
    def continue_sample_collection(self):

        # Run a loop untill the experiment time has been reached.
        print('Collecting the remainder sample spectra.')
        start_time = time.time()
        while time.time()-start_time<self.experiment_run_time:
            print(f'Total experiment run time {time.time()-start_time} / {self.experiment_run_time}')
            self.collect_sample()

    def stop_experiment(self):
        """Stopping IR experiment."""
        
        print('Stopping IR experiment')
        self.ir_machine.stop_experiment()
        print()

    def clean(self):
        """Cleaning the system."""
        
        print('Cleaning system')
        
        # Cleaning ir lines with wet solvent
        print('Cleaning ir lines with wet solvent.')
        self.pump.transfer(
            from_position=self.wet_solvent_valve,
            to_position=self.ir_valve,
            volume=self.wet_solvent_clean_volume,
            aspirate_speed=self.clean_speed,
            dispense_speed=self.clean_speed)
        
        # Cleaning ir lines with water.
        print('Cleaning ir lines with water.')
        self.pump.transfer(
            from_position=self.water_valve,
            to_position=self.ir_valve,
            volume=self.water_clean_volume,
            aspirate_speed=self.clean_speed,
            dispense_speed=self.clean_speed)
    
        # Cleaning ir lines with solvent.
        print('Cleaning ir lines with solvent.')
        self.pump.transfer(
            from_position=self.solvent_valve,
            to_position=self.ir_valve,
            volume=self.solvent_clean_volume,
            aspirate_speed=self.clean_speed,
            dispense_speed=self.clean_speed)
        
        # Cleaning ir lines with air.
        print('Drying ir lines with air.')
        self.pump.transfer(
            from_position=self.air_valve,
            to_position=self.ir_valve,
            volume=self.air_clean_volume,
            aspirate_speed=self.clean_speed,
            dispense_speed=self.clean_speed)    
    
    def shut_down(self):
        """Shuts down pumps and ir machine."""

        # Shutting down
        self.ir_machine.shutdown()
        self.pump.shutdown()
    
    def run_experiment(self):
        """Runnning through a complete experiment."""

        self.prime_lines()
        self.collect_solvent_sample()
        self.check_sample_setup()
        
        # Checking if the experiment has been set up appropiatly.
        if self.sample_setup_appropiate:
            self.collect_first_sample()
            self.continue_sample_collection()
            self.stop_experiment()          
            self.clean()
        
        self.shut_down()                 

if __name__=='__main__':
    # Example use
    
    # Valve information
    solvent_valve = 5
    wet_solvent_valve = 6
    waste_valve = 12
    water_valve = 8
    air_valve = 1
    ir_valve = 4

    # Prime information
    prime_speed = 15 / 60                   # Division by 60 is required for conversion reasons
    prime_volume = 2

    # Solvent sample information
    solvent_sample_volume = 1
    solvent_pump_speed = 0.07
    solvent_spectrum_time = 65

    # Sample information
    sample_volume = 0.9
    sample_spectrum_time = 55
    sample_pump_speed = 2 / 60              # Division by 60 is required for conversion reasons
    
    # Experiment information
    experiment_run_time = 14400             # 4 hours in sec
    experiment_name = 'Test1'
    
    # Cleaning information
    clean_speed = 6 / 60                    # Division by 60 is required for conversion reasons
    wet_solvent_clean_volume = 3
    water_clean_volume = 4
    solvent_clean_volume = 3
    air_clean_volume = 20

    # Spectra information
    icIR_template_name = 'DigitalDiscoveryProject'                            
    spectra_location = 'Digital Discovery Project\\' + experiment_name
    
    experiment1 = SensingSensitivityReaction(experiment_name, icIR_template_name, spectra_location, solvent_valve, waste_valve, water_valve, air_valve, ir_valve, prime_volume, prime_speed, solvent_sample_volume, solvent_pump_speed, solvent_spectrum_time, sample_volume, sample_spectrum_time, sample_pump_speed, experiment_run_time, clean_speed)
    # experiment1.run_experiment()