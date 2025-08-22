import os
import time
from LiquidHandling import Pump
from ReactPyR.ReactPyR import ReactPyR
from ika.magnetic_stirrer import MagneticStirrer


class SensingSensitivityReaction:
    """The procedure the pump and IR spectrometer follows to run experiments for the digital discovery paper."""

    def __init__(
        self,
        experiment_name,
        icIR_template_name,
        spectra_location,
        spectra_path,
        solvent_valve,
        waste_valve,
        water_valve,
        air_valve,
        ir_valve,
        prime_volume,
        prime_speed,
        solvent_sample_volume,
        solvent_pump_speed,
        solvent_spectrum_time,
        sample_volume,
        sample_spectrum_time,
        sample_pump_speed,
        experiment_run_time,
        clean_speed,
    ):

        # IR experiment information
        self.icIR_template_name = icIR_template_name  # The template used to start an icIR machine. If not written in specified format, icIR wont start experiment.
        self.spectra_location = spectra_location  # The location where the specta will be saved. This is used by icIR opc server. If not written in specified format, icIR wont start experiment (should be a subdirectory of iC IR Experiments folder, where subfolders are seperated by \\).
        self.spectra_path = spectra_path  # The path (string) to the folder to save IR spectra. This is used by the python class.

        # Experiment information
        self.experiment_run_time = experiment_run_time  # The time (s) the experiment should last for. It dictates how many samples can be sent in this time interval.
        self.check_experiment_name(
            experiment_name
        )  # Checks if the experiment exists already.
        self.experiment_name = experiment_name  # The name of the experiment, which will also be used to save spectra file names.

        # Pump valve information
        self.solvent_valve = (
            solvent_valve  # The pump's valve number connected to the solvent flask.
        )
        self.wet_solvent_valve = wet_solvent_valve  # The pump's valve number connected to the wet solvent flask.
        self.waste_valve = (
            waste_valve  # The pump's valve number connected to the waste flask.
        )
        self.water_valve = (
            water_valve  # The pump's valve number connected to the water flask.
        )
        self.ir_valve = ir_valve  # The pump's valve number connected to the IR machine.
        self.air_valve = air_valve  # The pump's valve number connected to air.

        # Priming information
        self.prime_speed = (
            prime_speed  # The speed of the pumps (mL/min) to prime lines with.
        )
        self.prime_volume = prime_volume  # The volume of solvent to prime lines with.

        # Solvent sample information
        self.solvent_sample_volume = solvent_sample_volume  # The volume (mL) of solvent required to reach IR machine to collect spectra
        self.solvent_spectrum_time = solvent_spectrum_time  # The time (s) the IR experiment (to collect solvent spectrum) should run for.
        self.solvent_pump_speed = solvent_pump_speed  # The speed (mL/min) pumpd draw and collect solvent sample.

        # Sample information
        self.sample_volume = (
            sample_volume  # The volumes (mL) of the samples to be drawn by the pump.
        )
        self.sample_spectrum_time = sample_spectrum_time  # The time (s) the IR experiment (to collect sample spectrum) should run for.
        self.sample_pump_speed = (
            sample_pump_speed  # The speed (mL/min) pumps draw and collect samples.
        )

        # Cleaning information
        self.clean_speed = (
            clean_speed  # The speed (mL/min) pumps draw and dispense to clean lines.
        )

        self.wet_solvent_clean_volume = wet_solvent_clean_volume  # The volume (mL) of wet solvent to clean lines with.
        self.water_clean_volume = (
            water_clean_volume  # The volume (mL) of water to clean lines with.
        )
        self.solvent_clean_volume = (
            solvent_clean_volume  # The volume (mL) of solvent to clean lines with.
        )
        self.air_clean_volume = (
            air_clean_volume  # The volume (mL) of air to dry lines with.
        )

        # Only one pump and an IR machine is required for this project.
        self.pump = Pump("COM3", 12)
        self.ReactPyR = ReactPyR("opc.tcp://localhost:62552/iCOpcUaServer")

        # Other required attributes
        self.sample_setup_appropiate = False  # Boolean to check if system has been set up well for sample preperation.
        self.requires_50_50_mix = False
        self.first = False

        # Start Stirrer
        self.plate = MagneticStirrer(port=stirrer_port)
        self.plate.set_target_stir_rate(stir_rate)
        self.plate.start_stirring()

        print(
            "Stirring set"
        )  # Booolean to check if the experiment is running with 50_50 mix samples.

    def check_experiment_name(self, experiment_name):
        """Checks if the exerpiment name already has any files associated with it."""

        files_in_dir = os.listdir(self.spectra_path)
        experiment_spectra = spectra_path + ".iCIR"
        if experiment_spectra in files_in_dir:
            raise NameError(
                f"The spectra for '{experiment_name}' has been collected already. Change experiment name."
            )

    def prime_lines(self):
        """Priming solvent->waste lines with solvent."""

        print("Priming solvent->waste lines")
        print()
        # Priming solvent->waste
        self.pump.transfer(
            from_position=self.solvent_valve,
            to_position=self.waste_valve,
            volume=self.prime_volume,
            aspirate_speed=self.prime_speed,
            dispense_speed=self.prime_speed,
        )

    def collect_solvent_sample(self):
        """Collects the spectrum of the solvent."""

        # Transfering sample volume
        print("Transfering solvent to IR machine for solvent spectra collection")
        self.pump.transfer(
            from_position=self.solvent_valve,
            to_position=self.ir_valve,
            volume=self.solvent_sample_volume,
            aspirate_speed=self.solvent_pump_speed,
            dispense_speed=self.solvent_pump_speed,
        )

        # Strating icIR experiment
        print("Starting icIR experiment")
        self.ReactPyR.start_experiment(self.spectra_location, self.icIR_template_name)

        # Collecting solvent spectra
        print("Collecting solvent sample spectra")
        time.sleep(self.solvent_spectrum_time)

        self.ReactPyR.pause_experiment()

        # transfer from IR back to solvent
        print("Transfering solvent sample back to ir")
        self.pump.transfer(
            from_position=self.ir_valve,
            to_position=self.solvent_valve,
            volume=self.solvent_sample_volume * 1.1,
            aspirate_speed=self.solvent_pump_speed,
            dispense_speed=self.solvent_pump_speed,
        )

        print()

    def additional_mix_sample_check(self):
        """An additional check if the experiment is to be trailed with a 50/50 sample mix."""

        exit_loop = False
        while not exit_loop:
            mix_input = input(
                "Do you have to change the sample vial to a 50/50 mix after 2 hours? (Yes/No/Exit): "
            )

            if mix_input.lower() in ["y", "yes"]:
                self.requires_50_50_mix = True
                exit_loop = True

            elif mix_input.lower() in ["e", "exit", "no", "n"]:
                self.requires_50_50_mix = False
                exit_loop = True

            else:
                print("Please add an appropiate input")
        print()

    def check_sample_setup(self):
        """Before more samples are run, the system needs to be setup and checked by the chemist."""

        # Check if a control sample needs to be run at the end of the experiment
        exit_loop = False
        while not exit_loop:
            mix_input = input(
                "Do you have to change the sample vial to a 50/50 mix after the experiment is complete? (Yes/No/Exit): "
            )

            if mix_input.lower() in ["y", "yes"]:
                self.requires_50_50_mix = True
                exit_loop = True

            elif mix_input.lower() in ["no", "n"]:
                self.requires_50_50_mix = False
                exit_loop = True

            elif mix_input.lower() in ["e", "exit"]:
                exit_loop = True
                self.sample_setup_appropiate = False

            else:
                print("Please add an appropiate input")

        print()

    def collect_sample(self, mix=False):
        """Collecting the spectra of a sample.
        mix: True if the sample is a 50/50 mixture."""

        # Aspirate from Ir machine
        print("Aspirating the sample from IR machine.")
        self.pump.switch(self.ir_valve)
        self.pump.move(self.sample_volume, self.sample_pump_speed)
        print()

        # resume spectra aquisition
        print("Collecting the spectrum of the sample.")
        self.ReactPyR.resume_experiment()
        if mix:
            time.sleep(180)
        else:
            time.sleep(self.sample_spectrum_time)

        self.ReactPyR.pause_experiment()

        # Dispensing back the drawn volume
        print("Returning the sample back to IR.")
        self.pump.move(0, self.sample_pump_speed)

        print()

    def collect_first_sample(self):
        """Collecting spectra of sample."""

        print("Collecting the spectra of the first sample")

        # resume spectra aquisition
        self.ReactPyR.resume_experiment()
        time.sleep(self.sample_spectrum_time)
        self.ReactPyR.pause_experiment()

        # Dispensing back the drawn volume

        print("Transfering air to IR machine for to reset")
        self.pump.transfer(
            from_position=self.air_valve,
            to_position=self.ir_valve,
            volume=self.solvent_sample_volume * 1.1,
            aspirate_speed=self.sample_pump_speed,
            dispense_speed=self.sample_pump_speed,
        )
        self.first = False
        print()

    def continue_sample_collection(self):
        """Collecting samples for the remainder of the experiment run time."""

        # Run a loop untill the experiment time has been reached.
        print("Collecting the remainder sample spectra.")
        start_time = time.time()
        continue_loop = True
        mix_check_bool = True
        while time.time() - start_time < self.experiment_run_time and continue_loop:

            print(
                f"Total experiment run time {round((time.time()-start_time)/60, 4)} / {self.experiment_run_time/60} min"
            )

            # If it a 50/50 mix is required and 2 hours have elapsed, the sample needs to be changed then an additional 3 scans are required.
            if self.requires_50_50_mix:
                if (time.time() - start_time) > (
                    experiment_run_time / 2
                ) and mix_check_bool:
                    if self.mix_check():
                        self.collect_sample(mix=True)
                        mix_check_bool = False
                        continue_loop = False
                    else:
                        continue_loop = False
                        mix_check_bool = False
                else:
                    self.collect_sample()
            else:
                self.collect_sample()

    def stop_experiment(self):
        """Stopping IR experiment."""

        print("Stopping IR experiment")
        self.ReactPyR.stop_experiment()
        print()

    def clean(self):
        """Cleaning the system."""

        print("Cleaning system")

        # Cleaning ir lines with wet solvent
        print("Cleaning ir lines with wet solvent.")
        self.pump.transfer(
            from_position=self.wet_solvent_valve,
            to_position=self.ir_valve,
            volume=self.wet_solvent_clean_volume,
            aspirate_speed=self.clean_speed,
            dispense_speed=self.clean_speed,
        )

        # Cleaning ir lines with water.
        print("Cleaning ir lines with water.")
        self.pump.transfer(
            from_position=self.water_valve,
            to_position=self.ir_valve,
            volume=self.water_clean_volume,
            aspirate_speed=self.clean_speed,
            dispense_speed=self.clean_speed,
        )

        # Cleaning ir lines with solvent.
        print("Cleaning ir lines with solvent.")
        self.pump.transfer(
            from_position=self.solvent_valve,
            to_position=self.ir_valve,
            volume=self.solvent_clean_volume,
            aspirate_speed=self.clean_speed,
            dispense_speed=self.clean_speed,
        )

        # Cleaning ir lines with air.
        print("Drying ir lines with air.")
        self.pump.transfer(
            from_position=self.air_valve,
            to_position=self.ir_valve,
            volume=self.air_clean_volume,
            aspirate_speed=self.clean_speed,
            dispense_speed=self.clean_speed,
        )

    def shut_down(self):
        """Shuts down pumps and ir machine."""

        # Shutting down
        self.ReactPyR.shutdown()
        self.pump.shutdown()

    def run_experiment(self):
        """Runnning through a complet e experiment."""

        self.check_sample_setup()
        self.prime_lines()
        self.collect_solvent_sample()

        # Checking if the experiment has been set up appropiatly.
        # if self.sample_setup_appropiate:
        self.collect_first_sample()
        self.continue_sample_collection()
        self.stop_experiment()
        self.clean()

        self.shut_down()


if __name__ == "__main__":
    # Example use

    # Valve information
    solvent_valve = 5
    wet_solvent_valve = 6
    waste_valve = 12
    water_valve = 8
    air_valve = 1
    ir_valve = 4

    # Prime information
    prime_speed = 15 / 60  # Division by 60 is required for conversion reasons
    prime_volume = 2

    # Solvent sample information
    solvent_sample_volume = 1
    solvent_pump_speed = 0.07
    solvent_spectrum_time = 12

    # Sample information
    sample_volume = 0.9
    sample_spectrum_time = 12
    sample_pump_speed = 16 / 60  # Division by 60 is required for conversion reasons

    # Stirring information
    stir_rate = 150
    stirrer_port = "COM5"

    # Experiment information
    experiment_run_time = 14400  # 4 hours in sec 14400
    experiment_name = "TestTubingLength_7"

    # Cleaning information
    clean_speed = 6 / 60  # Division by 60 is required for conversion reasons
    wet_solvent_clean_volume = 3
    water_clean_volume = 4
    solvent_clean_volume = 3
    air_clean_volume = 20

    # Spectra information
    icIR_template_name = "DigitalDiscoveryProject_Updated"
    spectra_location = "Digital Discovery Project\\" + experiment_name
    spectra_path = "C:/Users/localadm-lablaptop/Documents/iC IR Experiments/Digital Discovery Project"

    experiment1 = SensingSensitivityReaction(
        experiment_name,
        icIR_template_name,
        spectra_location,
        spectra_path,
        solvent_valve,
        waste_valve,
        water_valve,
        air_valve,
        ir_valve,
        prime_volume,
        prime_speed,
        solvent_sample_volume,
        solvent_pump_speed,
        solvent_spectrum_time,
        sample_volume,
        sample_spectrum_time,
        sample_pump_speed,
        experiment_run_time,
        clean_speed,
    )
    experiment1.run_experiment()
