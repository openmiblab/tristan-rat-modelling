# tristan-rat-modelling
Kinetic analysis using the TRISTAN rat assay for transported-mediated drug inhibition

Preclinical - effect on liver function of 6 test drugs
======================================================

This example illustrates the use of `~dcmri.Liver` for fitting of signals 
measured in liver. The use case is provided by the liver work package of the 
`TRISTAN project <https://www.imi-tristan.eu/liver>`_  which develops imaging 
biomarkers for drug safety assessment. The data and analysis were first 
published in Melillo et al (2023). 

The specific objective of the study was to determine the effect of selected 
drugs on hepatocellular uptake and excretion of the liver-specific contrast 
agent gadoxetate. If a drug inhibits uptake into liver cells, then it might 
cause other drugs to circulate in the blood stream for longer than expected, 
potentially causing harm to other organs. Alternatively, if a drug inhibits 
excretion from the liver, then it might cause other drugs to pool in liver 
cells for much longer than expected, potentially causing liver injury. These 
so-called drug-drug interactions (DDI's) pose a significant risk to patients 
and trial participants. A direct in-vivo measurement of drug effects on liver 
uptake and excretion can potentially help improve predictions of DDI's and 
inform dose setting strategies to reduce the risk.

The study presented here measured gadoxetate uptake and excretion in healthy 
rats before and after injection of 6 test drugs. Studies were performed in 
preclinical MRI scanners at 3 different centers and 2 different field 
strengths. Results demonstrated that two of the tested drugs (rifampicin and 
cyclosporine) showed strong inhibition of both uptake and excretion. One drug 
(ketoconazole) inhibited uptake but not excretion. Three drugs (pioglitazone, 
bosentan and asunaprevir) inhibited excretion but not uptake. 

**Reference**

Melillo N, Scotcher D, Kenna JG, Green C, Hines CDG, Laitinen I, Hockings PD, 
Ogungbenro K, Gunwhy ER, Sourbron S, et al. Use of In Vivo Imaging and 
Physiologically-Based Kinetic Modelling to Predict Hepatic Transporter 
Mediated Drug–Drug Interactions in Rats. Pharmaceutics. 2023; 15(3):896. 
`[DOI] <https://doi.org/10.3390/pharmaceutics15030896>`_ 
