# ORCA_Scan_Toolkit

&nbsp;&nbsp;&nbsp;&nbsp;Tools for studying excited state energy surfaces based
on the ORCA program, as ORCA is very good at excited state calculations.<br>

## scansplit.py

&nbsp;&nbsp;&nbsp;&nbsp;Inspired by the [SCANsplit program](http://sobereva.com/199)
developed by Sobereva, this script can be used to extract the structures from
all frames in the Gaussian rigid/relaxed scan output file and generate severial
single-point INP files for each frame according to the INP template. The script
could be useful if you need to analyze the evolution of electronic structure or
plot adiabatic potential energy surfaces of excited states, etc. Usage:
`python scansplit.py inptemp.inp scanout.out`, input order is irrelevant.<br>

## apesplot.py

&nbsp;&nbsp;&nbsp;&nbsp;This script is used to plot the adiabatic potential
energy surfaces(APESs) of multiple excited states distinguished by spin
multiplicity, based on the Wigner-Eckart theorem(2 or 3 spin are reachable). It
should be used in conjunction with `scansplite.py`. With simple setup, it can
produce **publishable-quality** images. Usage: place all the ORCA single-point
excited state calculation output files into the `apesplot.py` directory，modify
the scanning settings at the top of the `apesplot.py` (one can also add the
diabatic states and excitation wavelength), then run `python apesplot.py`.<br>
