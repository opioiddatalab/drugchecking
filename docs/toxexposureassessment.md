# *in situ* Toxicology Risk Assessment

For compliance with UNC Environmental Health Services, we assessed toxicology risk *in situ* at the point of sample collection. We assessed N=157 substances detected across N=844 street drug samples using GCMS.

## Qualifications
Each substance was reviewed in tandem by a chemist and a clinical toxicology/pharmacology specialist.

## Information Sources

Assessment was conducted on Feburary 9, 2023. When toxicology was unknown, the following sources were consulted, in order:
1. PubChem (using PubChem ID): toxicology, bioassay
1. FDA Global Product Registration System (using UNII): relationships, LD50
1. NLM DailyMed drug labels (using API): adverse events
1. Cayman Chemical (using CAS): LD metrics
1. PubMed, Google Scholar if completely unknown

## Assumptions and Considerations
+ Typical North American human was defined as otherwise healthy adult male or female of 60kg to 70kg.
+ Setting was defined as public health program with minimally trained sample collectors.
+ Human factor considerations were failure to wear gloves and failure to use provided absorbent spill cloth.
+ Aside from ACN, no other potentially harmful substance is introduced by the drug checking kits.
+ All substances identified previosuly existed in street drugs. 
+ Drug-drug interactions were considered relevant for known combinations of common street drugs, and considered as either paired exposure (e.g., one opioid, one benzodiazepine), as well as in common co-ccurrence patterns from our [empirical lab data](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/nc/nc_lab_detail.csv).
+ Single acute exposure hepatotoxicity was considered but deemed unlikely given Worst Case Scenario quantities (see below).
+ Teratogenicity risks were considered. No substances were identified that are known to pose teratogenic risk at the concentrations expected and routes of exposure assessed.
+ Common pharmaceutical preparations were considered, as well commonly known street drug forms.

## Worst Case Scenarios
Worst Case Scenario was defined as a vial of 1.5 mL ACN containing drug sample spilling on a hard surface. Highest concentration exposure is via ~5mg scoop sample collection method; residual amounts collected using swab (e.g., from empty baggies from litter) are expected to contain amounts too low for appreciable toxicity.

+ For **dermal exposure**, the Worst Case Scenario is built around human error from failing to wear gloves. It begins with evaporation of ACN on a non-porous surface, leaving behind full quantity of drug sample. This would be followed by skin contact of the entire quantity lasting <3 minutes before rinsing with water (e.g., powder brushed onto palm of ungloved hand from table). Broken skin scenarios were also considered.
+ For **inhalation exposure**, the Worst Case Scenario is due to inadvertent introduction to nasal mucosa. It would begin with evaporation of ACN on a non-porous surface, leaving behind full quantity of drug sample. This would be followed by finger (gloved or ungloved) contamination brought to nostril and deeply inhaled (e.g., to smell the substance). Passive inhalation and aerosol risk negligible due to solvated form and plausible spill distribution pattern.
+ For **oral exposure**, the Worst Case Scenario encompasses intentional and inadvertent consumption. Inadvertent scenario is food contamination *in situ*, through dermal or fomite-like transfer, or accidental spillage, considering simultaneous dermal and oral exposure. Intentional consumption of dried sample is highly unlikely because the drugs would have been more likely to have been consumed in original street form/packaging; ACN in sample collection kits do not increase pre-existing risk. "Methyl cyanide" (ACN) warning on label is intended to deter this specific behavior. In the Worst Case Scenario for inadvertent introduction to oral mucosa, followed by ingestion and swallowing, we considered <5mg to be the upper limit of plausibility. It would begin with evaporation of ACN on a non-porous surface, leaving behind full quantity of drug sample. The entirety of the dried sample would then have to be inadvertently and knowingly brushed onto a plate of food, and immediately consumed. A second, slightly more likely, scenario was considered whereby a fraction of the dried sample is "tasted" on an ungloved fingertip resulting in both oral and dermal exposure. In this scenario <1mg would be expected to be ingested orally, with greatest concern due to absorption through the oral mucosa, and secondary concern of exposure to pulmonary tissue (e.g., post-nasal drip) or esophageal epithelium exposure (e.g., corrosive substances). For pharmaceutical prearations commonly manufactured in liquid form (e.g., methadone), 2 mL was considered the limit of plausible intentional exposure because the vial has a 4mL limit, of which 1.5mL ACN is already present.

## Empirical Drug Composition Data
Empirical data on frequency, relative amount (trace vs. primary), and combinations were drawn from 800+ street drug samples analyzed by our lab using GCMS from November 2021 through January 2023. Drug samples from the community were received as part of a mail-in drug checking program. Samples were sent to the laboratory in 4.0-mL screw-top glass vials containing the sample dissolved in 1.5mL acetonitrile. Samples were analyzed with a ThermoScientific Exactive GC with an electron ionization source. The mass accuracy capability is <1 parts per million RMS error with internal calibration. [Full methods here.](https://github.com/opioiddatalab/drugchecking/blob/main/docs/lab_methods.md)<br><br>
Data on [North Carolina samples](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/nc/nc_lab_detail.csv) are posted publicly.<br><br>
[List of detected substances](https://github.com/opioiddatalab/drugchecking/blob/main/chemdictionary/substances_detected.csv) nationally, with frequencies.

## Routes of Exposure
Three routes of exposure were considered:
+ **Oral** - ingestion of no more than 5 mg
+ **Dermal** - exposure time <2 minutes at concentration of <1mg
+ **Inhalation** - Incidental transmucosal exposure (e.g., glove-to-nose) and powder consumption of <5mg pure substance. 

## Classification
Substances were classified using 4 mutually exclusive categories.
+ **Low** - known or generally accepted clinical toxicology profile 
+ **Concern** - suspected or known concern of acute toxicity by route of exposure
+ **Routine** - commonly used medication or substance with known risk profile
+ **Unknown** - emerging substances found in street drugs, to be prospectively monitored

## Findings

Tabulation of assessed samples can be [found here](https://github.com/opioiddatalab/drugchecking/blob/main/docs/tox_assessment.csv).

Substance-route pairings of concern identified:
+ LSD-dermal
+ carfentanil-inhalation
+ etonitazene-dermal (via broken skin)
+ methadone-oral (liquid 20mg in 2mL)

Assessment unkown:
+ For certain substances (e.g., 2-methyl-1,2,3,4-tetrahydro-b-carboline) we were unable to find reliable known human or animal toxicology. They were routinely present in trace amounts in street drug samples, precluding real-world exposure assessment. Based on chemical structure assessment and comparative toxicology to similar molecules, we did not expect these substances to raise to the level of "concern" in the quantities expected and the specified routes of exposure. We will continue to monitor these substances for additional information.
+ In many instances a precursor/byproduct substance was detected (e.g., benzoylecgonine) that is poorly characterized as a substance by itself. These substances usually occur in trace quantities (<5% peak GCMS on chromatogram) and nearly always in conjunction with an active substance. In these instances the active moiety's toxicologic properties were consider to supercede.
