# *in situ* Toxicology Risk Assessment

For compliance with UNC Environmental Health Services, we assessed toxicology risk *in situ* at the point of sample collection. We assessed N=157 substances detected across N=844 street drug samples using GCMS.

## Qualifications
Each substance was reviewed in tandem by a chemist and a clinical toxicology/pharmacology specialist.

## Information Sources

Assessment was conducted on Feburary 9, 2023. When toxicology was unknown, the following sources were consulted, in order:
1. [PubChem](https://pubchem.ncbi.nlm.nih.gov/) (using PubChem ID): toxicology, bioassay
1. [FDA Global Product Registration System](https://precision.fda.gov/uniisearch) (using UNII): relationships, LD50
1. [NLM DailyMed](https://dailymed.nlm.nih.gov/dailymed/index.cfm) drug labels (using API): adverse events
1. [Cayman Chemical](https://www.caymanchem.com/) (using CAS): LD metrics
1. PubMed, Google Scholar if completely unknown

## Assumptions and Considerations
+ Typical North American human was defined as otherwise healthy adult male or female of 60kg to 70kg.
+ Setting was defined as public health program with minimally trained sample collectors.
+ Human factor considerations were failure to wear gloves and failure to use provided absorbent spill cloth.
+ Aside from ACN, no other potentially harmful substance is introduced by the drug checking kits.
+ All substances identified previously existed in street drugs. 
+ Drug-drug interactions were considered relevant for known combinations of common street drugs, and considered as either paired exposure (e.g., one opioid, one benzodiazepine), as well as in common co-ccurrence patterns from our [empirical lab data](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/nc/nc_lab_detail.csv).
+ Single acute exposure hepatotoxicity was considered but deemed unlikely given Worst Case Scenario quantities (see below).
+ Teratogenicity risks were considered. No substances were identified that are known to pose teratogenic risk at the concentrations expected and routes of exposure assessed.
+ Common pharmaceutical preparations were considered, as well commonly known street drug forms.
+ Toxicology due to ACN alone has been addressed separately.

## Worst Case Scenarios
Worst Case Scenario was defined as a vial of 1.5 mL ACN containing drug sample spilling on a hard surface. Highest concentration exposure is via ~5mg scoop sample collection method; residual amounts collected using swab (e.g., from empty baggies from litter) are expected to contain amounts too low for appreciable toxicity.

+ For **dermal exposure**, the Worst Case Scenario is built around human error from failing to wear gloves. It begins with evaporation of ACN on a non-porous surface, leaving behind full quantity of drug sample. This would be followed by human skin contact of the entire quantity lasting <3 minutes before rinsing with water (e.g., powder brushed onto palm of ungloved hand from table). Broken skin scenarios were also considered.
+ For **inhalation exposure**, the Worst Case Scenario is due to inadvertent introduction to human nasal mucosa. It would begin with evaporation of ACN on a non-porous surface, leaving behind full quantity of drug sample. This would be followed by finger (gloved or ungloved) contamination brought to nostril and deeply inhaled (e.g., to smell the substance). Passive inhalation and aerosol risk negligible due to solvated form and plausible spill distribution pattern.
+ For **oral exposure**, the Worst Case Scenario encompasses intentional and inadvertent human consumption. Inadvertent scenario is food contamination *in situ*, through dermal or fomite-like transfer, or accidental spillage, considering simultaneous dermal and oral exposure. Intentional consumption of dried sample is highly unlikely because the drugs would have been more likely to have been consumed in original street form/packaging; ACN in sample collection kits do not increase pre-existing risk. "Methyl cyanide" (ACN) warning on label is intended to deter this specific behavior. In the Worst Case Scenario for inadvertent introduction to oral mucosa, followed by ingestion and swallowing, we considered <5mg to be the upper limit of plausibility. It would begin with evaporation of ACN on a non-porous surface, leaving behind full quantity of drug sample. The entirety of the dried sample would then have to be inadvertently and knowingly brushed onto a plate of food, and immediately consumed. A second, slightly more likely, scenario was considered whereby a fraction of the dried sample is "tasted" on an ungloved fingertip resulting in both oral and dermal exposure. In this scenario <1mg would be expected to be ingested orally, with greatest concern due to absorption through the oral mucosa, and secondary concern of exposure to pulmonary tissue (e.g., post-nasal drip) or esophageal epithelium exposure (e.g., corrosive substances). For pharmaceutical prearations commonly manufactured in liquid form (e.g., methadone), 2 mL was considered the limit of plausible intentional exposure because the vial has a 4mL limit, of which 1.5mL ACN is already present.
+ We also considered human exposure among Common Carrier personnel, resulting from crushed box and vial. The Worst Case Scenario invovles broken glass as the primary causative hazard, with secondary exposure to chemical substances. Toxicology concerns by route are similar to above, with greater attention to broken skin dermal exposure. In these instances, combinations of ACN and drug substance were considered. The Worst Case Scenario was defined as a crushed package with broken vial, resulting in mild laceration (ungloved hand) from broken glass, with exposure duration of 10 minutes before washing with water. 

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

Tabulation of all assessed samples can be [found here](https://github.com/opioiddatalab/drugchecking/blob/main/docs/tox_assessment.csv).

Substance-route pairings of concern identified:
+ LSD-dermal
+ carfentanil-inhalation
+ etonitazene-dermal (via broken skin)
+ methadone-oral (liquid 20mg in 2mL)

### Mitigation
+ **LSD-dermal** exposure is rare but plausible, with known dermal absorption of LSD. Fatal toxicology is [exceedingly rare](https://shaunlacob.com/wp-content/uploads/2020/12/Investigators-Brochure-LSD-MAPS-2008.pdf), but pharmacological effects can happen at low concentrations. Only 2 out of 844 samples containing LSD have been encountered by our lab ([300467](https://www.streetsafe.supply/results/p/300467) and [300821](https://www.streetsafe.supply/results/p/300821), both in paper blotter format. Lacertation exposure after solvation in ACN could result in pharmacological effect. Hand washing instructions could be considered.
+ **carfentanil-inhalation** is rare but plausible. No samples with carfentanil have been observed from street samples in our lab. Dermal absorption *in vitro* is fastest in water (30 mins), and slowest in ethanol (1.5 hours); [Lent et al.](https://pubmed.ncbi.nlm.nih.gov/31669393/) conclude "small skin exposures may not result in rapid, significant toxicity." Inhalation risk of carfentanil is hypothesized, but dose ranges are unknown. [Animal](https://pubmed.ncbi.nlm.nih.gov/28330429/) and [human](https://pubmed.ncbi.nlm.nih.gov/12712038/) exposure studies provide limited information. In the United States, carfentanil-involved overdose was [largely isolated](https://pubmed.ncbi.nlm.nih.gov/32935381/) to calendar years 2016-17, with rapid decline and disappearance in 2018 and beyond. In drug seizure data during this time period, carfentanil was [rarely detected](https://pubmed.ncbi.nlm.nih.gov/29659874/) by itself, and usually as a minor component mixed with other unregulated opioids. Still, there is a possibility that carfentanil could re-emerge in street drugs. If this happens (e.g., more than 3 samples in a 3 month period), additional warnings and mitigation strategies will be considered in packaging.
+ **etonitazine-dermal** is [poorly characterized](https://doi.org/10.1016/B978-0-12-818788-3.00018-8) and primarily of concern if exposure happens via broken skin. Etonitazine has been detected in [Toronto](https://drugchecking.cdpe.org/alert/etonitazene/), and occasionally in the United States. With LD<sub>50</sub> of 250 μg/kg in mice, it is a novel opioid of concern. We have not received any street drug samples containing etonitazene, but one sample with a related molecule, [N-piperidinyl etonitazene](https://www.streetsafe.supply/results/p/300408), with much lower expected potency. Inhalation risk quantities are unknown. Like with carfentanil, we will continue to monitor the emergence of etonitazine and consider changes to packaging if it is repeatedly detected.
+ **methadone-oral** is an edge case scenario, if 2 mLs of liquid methadone (e.g., from MMTP) at 10 mg/mL were to be consumed. This seems highly improbable, especially with the deterrent labeling on our vial. Liquid methadone is only dispensed in specialty clinics, with observed dosing; take-home methadone is also a medical model. Intentional consumption of 2 mLs of liquid methadone from a 4 mL vial (containing 1.5 mL ACN) is a highly contrived situation and cannot be envisioned in scenarios other than intentional self-harm. We believe the "methyl cyanide" labeling is important, and could possibly be adjusted to include "do not consume" instead of "for public health use only." 


### Assessment Unknown
+ For certain substances (e.g., 2-methyl-1,2,3,4-tetrahydro-b-carboline) we were unable to find reliable known human or animal toxicology. They were routinely present in trace amounts in street drug samples, precluding real-world exposure assessment. Based on chemical structure assessment and comparative toxicology to similar molecules, we did not expect these substances to raise to the level of "concern" in the quantities expected and the specified routes of exposure. We will continue to monitor these substances for additional information.
+ In many instances a precursor/byproduct substance was detected (e.g., benzoylecgonine) that is poorly characterized as a substance by itself. These substances usually occur in trace quantities (<5% peak GCMS on chromatogram) and nearly always in conjunction with an active substance. In these instances the active moiety's toxicologic properties were consider to supercede.
