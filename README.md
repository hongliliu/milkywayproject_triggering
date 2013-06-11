milkywayproject_triggering
==========================
Code to calculate correlation functions for two (astrophysical) catalogue datasets


What is this repository?
========================

The main file in the repository is calc_corr.py. This file contains functions that calculate the correlation function between two astrophyiscal data catalogues using the Landy-Szalay approximator generalised for heterogeneous datasets (Landy \& Szalay, 1993; Bradshaw et al, 2011); or the auto-correlation function of one dataset.

The code was developed for use with the catalogue of bubbles in the interstellar medium generated from the Milky Way Project (MWP; http://milkywayproject.org), an initiative by the Zooniverse citizen science organisation (http://www.zooniverse.org), and the catalogue of young stellar objects from the Red MSX Source Survey (RMS; Urquhart et al. 2008, ASPC, 387, 381; http://www.ast.leeds.ac.uk/RMS/). It therefore assumes that one catalogue has positional information as well as an object size (effective radius), and the other only positional information. The catalogues do however contain many additional fields.

In addition, the repository contains a sample script demonstrating how to use the calc_corr code, with sample calls, data file generation and plots. Sample catalogues used in Kendrew et al (2012) are included in the cats/ subdirectory. NOTE that these may no longer be the most recent MWP data catalogues, these can be found at http://milkywayproject.org/data/.


Requirements and Dependencies
==============================

The code is written in Python, and was fully tested in Python 2.6.6. It is compatible with Python 2.7.

The following Python packages are used:

numpy
scipy
matplotlib
itertools
astropy (v. 0.2.3)
time
os
pdb (debugger, optional)

The code comes with no guarantees that it will run on your system, though please email me with questions. I will maintain the code on a best-effort basis.


Who wrote it?
===============

This code was written by Sarah Kendrew, Postdoc in Astronomy, while at the Max Planck Institute for Astronomy in Heidelberg, Germany. For more info, please contact me on sarahaskendrew AT gmail.com


Referencing
============

If you use this code, please cite:
Kendrew et al, 'The Milky Way Project: A Statistical Study of Massive Star Formation Associated with Infrared Bubbles', ApJ 755(1), 71 (2012)

I'd like to hear about your work so drop me a line. If you upset he code extensively, please consider adding me as a co-author to any resulting publications.

Further reading
================
Much useful background reading can be found in the Kendrew+ 2012 paper.


Acknowledgements
================

This work was made possible by the participation of more than 35,000 volunteers on the Milky Way Project. Their contributions are acknowledged individually at http://www.milkywayproject.org/authors. The Milky Way Project is supported by The Leverhulme Trust. 


--- S. Kendrew, sarahaskendrew AT gmail.com, June 2013.


