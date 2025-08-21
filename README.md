Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

# Sensing Sensitivity

This package is associated with the paper "ReactPyrR: A Python workflow for ReactIR allows for the quantification of the stability of sensitive compounds in air" by the Bell Group. 

This repo allows users to conduct experiments monitoring the kinetics of degradation of air-sensitive compounds in air and includes liquid handling control via a [LSPOne Syringe Pump](https://amf.ch/product/lspone-laboratory-syringe-pump/), stirring via an IKA RCT Digital Hotplate and [ReactIR15 Spectrometer](https://www.mt.com/dam/product_organizations/autochem/reactir/ReactIR-15.pdf) through Mettler Toledo's [iCIR software](https://www.mt.com/gb/en/home/products/L1_AutochemProducts/automated-reactor-in-situ-analysis-software/ic-ir-instrument.html). 

Dependencies: 

IKA Stirrer hotplate (https://pypi.org/project/ika/)

For use of this code the COM ports for the LSPOne and IKA hotplate must be identified using Device Manager and updated within. 

![Hardware Setup](/images/Hardware_DD.png)

![Software](/images/iCIR Screenshot.png)
