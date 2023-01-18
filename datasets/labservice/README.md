# Confirmatory/Complementary Test Results

This folder contains lab results from UNC's confirmatory/complementary [drug checking service](https://streetsafe.supply).<br>
<br>
> **Warning**<br>
> By downloading or accessing these datasets you are affirming that you are not a member of a law enforcement agency.<br>

<br>

# File Format
The file has multiple rows per sample, with one substance on each row. The datasets do not contain geographic identifiers. Datasets are updated daily. They are available in CSV, SAS, Stata, and Excel formats (above). Data availability using these files started on January 1, 2023.<br>

Syntax for direct call of the CSV via URL:

```
https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/labservice/unc_gcms.csv
```
<br>

The data elements are:<br>

|Variable|Description|
|:----|:----|
|`sampleid`|Sample identification number from vial (begins with 800xxx). This is *not* the StreetCheck app ID.|
|`date_complete`|Date analysis was completed in lab in format `01jan2023`|
|`substance`|Substance(s) identified using our [controlled vocabulary](https://github.com/opioiddatalab/drugchecking/blob/main/chemdictionary/substances_detected.csv)|
|`abundance`|Whether the substance was detected in primary or trace amounts. Trace elements are noted, and primary are left blank. Trace is defined as <5% of the most abundant peak in the chromatogram.|
|`method`|Laboratory method used for confirming substance. Takes values of GCMS, derivatized GCMS, and FTIR. When designated as "FTIR" this means GCMS followed by FTIR for further investigation. Rarely, We occasionally have to use FTIR to confirm which isomer a substance is once there is a match on GC.|
|`peak`|Identifies the corresponding retention time peak (in minutes) from the chromatogram.|
<br>

# GCMS Chromatograms

![chromatogram](https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/spectra/300830.PNG)

The chromatogram is one of the outputs we analyze, a summary of the constituents. All chromatograms can be [found in this folder](https://github.com/opioiddatalab/drugchecking/tree/main/spectra) in PNG format. File naming convention is just the sample ID followed by `.PNG`. Syntax for direct call for spectra image files via URL:

```
https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/spectra/300830.PNG
```

+ Peak 6.65 = caffeine
+ Peak 7.2 = xylazine
+ Peak 8.74 = 4-ANPP
+ Peak 9.35 = heroin
+ Peak 9.71 = fentanyl

For samples with multiple chromatograms (e.g., removing acetaminophen), peaks correspond to the composite chromatogram.

# Other Resources
+ [All results](https://www.streetsafe.supply/results) (searchable)
+ List of all samples [containing xylazine](https://www.streetsafe.supply/results/xylazine)
+ All [North Carolina](https://www.streetsafe.supply/results/location/nc-samples) samples
+ [NLP code](https://github.com/opioiddatalab/drugchecking/blob/main/textexport/autotext.do) for converting sample results into human readable indivdual records for [website](https://streetsafe.supply)
+ [List of all substances detected](https://github.com/opioiddatalab/drugchecking/blob/main/chemdictionary/substances_detected.csv) with frequencies
+ Data collection card and sample collection instructions [PDF](https://cdr.lib.unc.edu/concern/multimeds/5d86p887m?locale=en)
+ Sample collection tutorial [video](https://vimeo.com/778263038/aae5f16d73)
+ [Chemical Dictionary](https://github.com/opioiddatalab/drugchecking/tree/main/chemdictionary) with pronunciations and classifications
+ [Canonical list](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/code/completed.csv) of all completed sample ID
+ [Laboratory methods](https://github.com/opioiddatalab/drugchecking/blob/main/docs/lab_methods.md) description
