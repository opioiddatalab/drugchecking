# Dataset Details for Analysts

Our analysis generates two datasets. One contains data recorded on the card and 1/0 indicators of lab results. The second file contains the detailed chemical findings. The datasets are linkable by `sampleid` variable. For reference, the [data collection card](https://cdr.lib.unc.edu/concern/multimeds/5d86p887m?locale=en) and [codebook](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/unc_druchecking_codebook.txt) are available.

## Confirmatory/complementary Testing Results

For confirmatory/complementary testing customers, the dataset file names will be the same as below, but will be placed in a separate directory. If you just want chemical results and know the sample ID, [this file](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/labservice/README.md) will give you immediate access. These are updated daily.

<br>

## File Formats
Results files `analysis_dataset.*` and `lab_detail.*` are provided in:
+ Stata (v14 or later)
+ Excel (.xlsx)
+ SAS (transport v8)
+ CSV (comma-separated with quote enclosure for strings)

<br>

## File Inventory
Below are two small demo datasets with documentation.  
<br>
`analysis_dataset` Example analysis dataset in WIDE format with processed and derived variables (N=20)
<br>[Stata](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.dta)
<br>[Excel](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.xlsx)
<br>[SAS](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.v8xpt)
<br>[CSV](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.csv)

<br>

`lab_detail` Example lab detail dataset in LONG format with standardized chemical names (N=20)
<br>[Stata](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.dta)
<br>[Excel](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.xlsx)
<br>[SAS](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.v8xpt)
<br>[CSV](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.csv)

<br>


The `sampleid` variable links the datasets `analysis_dataset.*` and `lab_detail.*`.<br>

For a quick view of the data, see this [Google Sheets](https://docs.google.com/spreadsheets/d/13tXdH9tdAcSNcyEA7Y6F8hdgu2tygL3ePUrxHSRY0OA/edit?usp=sharing) example as a single file with 2 tabs. <br>

# Analysis Dataset
The file `analysis_dataset.*` contains one row for each sample. It includes the characteristics that were reported on the card, and handy pre-processed variables to aid data analysis and visualization. The variable convention allows the analyst to quickly generate a time-series of how many samples contained fentanyl, for example in Stata:

```
table date if lab_fentanyl_any==1
```

It also contains 1/0 derived flags to help easily answer many common analytic questions, such as whether the sample contains xylazine, or if any fentanyl processing impurities (like 4-ANPP) were detected. These derived variables are indicated with the naming convention `lab_` in the variable name. The presence of particular compounds is marked `_any` in the variable name to indicate that the substance was detected in primary or trace amounts. The lack of a `_any` in the variable name means that it was the detected as a primary substance. Therefore, this sample contains xylazine in trace abundance `lab_xylazine_any=1` but not as a primary constituent `lab_xylazine=0`.<br><br>


|sampleid|date collected|lab_fentanyl|lab_fentanyl_impurity|lab_xylazine|lab_xylazine_any|
|-------:|--------------|--------|-----|-----|--------------|
123|12dec2022|1|1|0|1|

<br><br>

You can import the example `analysis_dataset.csv` instantly into Google sheets by pasting this one line of code into the first cell (A1):
```
=importData("https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/analysis_dataset.csv")

```

## Geolocation
+ The origin location (usually city) of the sample is recorded in the `location` variable, along with auto-geocoded `county` (via [OpenCage API](https://opencagedata.com/api)). If only county name was provided, this is indicated in the `location` field.
+ County is also provided in FIPS format as `countyfips` (5-digit including state) and `countyfips_3` (3-digit county only). In addition, a text combination of state abbreviation and county name is also provided, often helpful in visualizations, as `state_county` which takes the form `NC | NEW HANOVER` or `WA | KING`. All FIPS codes are strings with leading zeros.
+ State is provided as 2-digit state FIPS `statefips` and in `state_county`. The `state` variable is the capitalized two-letter USPS state abbreviation, and `full_state` is the state name with an initial capital. 
+ If location is not provided on the card, the location is defaulted to the city and county corresponding to the mailing address of where the kits were sent (e.g., program location).

<br>

# Lab Detail Dataset
The `lab_detail.*` file contains one row for each substance detected for each sample. The derived variables use the same naming convention and allow for understanding how each substance is classified. Additional variables can be constructed using searches on the `substance` variable. This file does not contain the information from the card provided during sample collection, which instead appears in `analysis_dataset.*` for the sake of data efficiency. This also allows you to see trace back and see how variable was constructed at an individual chemical level.<br><br>

| sampleid | substance | method | abundance |lab_fentanyl|lab_fentanyl_impurity|lab_xylazine|lab_xylazine_any|
|-----:|---------------|--------|-----------|------------|-----------------------|------------|----------------|
|   123| fentanyl      |GCMS    |           |1           |0                      |0           |0|
|   123| xylazine      |GCMS    |      trace|0           |0                      |0           |1|                   
|   123| 4-ANPP        |GCMS    |           |0           |1                      |0           |0|

<br>

In addition to the lab results, each substance is also classified using 1/0 flags according to our [Chemical Dictionary](https://github.com/opioiddatalab/drugchecking/blob/main/chemdictionary/chemdictionary.csv). This allows you to quickly identify which substances are synthetic cathinones, or fentanyl synthesis impurities. Please let us know if you'd like additional classifications. The chemical classifications in `lab_detail.*` are carried into `analysis_dataset.*` allowing for complete traceability on classification.

You can import the example `lab_detail.csv` instantly into Google sheets by pasting this one line of code into the first cell (A1):
```
=importData("https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/lab_detail.csv")

```

## Chemical Naming Conventions
In order to standardize chemical names (e.g., 6-monoacetylmorphine versus 6-MAM), lab results are provided in a standard common naming schema in `substance` but also cross-listed to three major standard chemical identification formats.
+ [PubChem CID](https://pubchem.ncbi.nlm.nih.gov) - From the National Library of Medicine, PubChem is the go-to open source chemical naming tool, and the one with the most complete number of substances. Links to literature, names, tox data, etc. can be found with this identifier. Because their database is so complete, small variations in plain language names can return spurious results; the CID is the preferred search term.
+ [CAS Registry Number](https://www.cas.org) - One of the global standards for substance identification maintained by the American Chemical Society, with a [handy API](https://commonchemistry.cas.org). Useful for linking out to cheminformatics systems. But some paywalls too.
+ [UNII](https://precision.fda.gov/uniisearch) - US FDA Global Substance Registration System can provide human-relevant summary data on toxicological risks.

# GCMS Chromatograms

![chromatogram](https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/spectra/olderspectra/300830.PNG)

The chromatogram is one of the outputs we analyze, a summary of the constituents (note: the chromatogram above is similar to, but not exactly the same, as the structured data example). All chromatograms can be [found in this folder](https://github.com/opioiddatalab/drugchecking/tree/main/spectra) in PNG format. File naming convention is just the sample ID followed by `.PNG`. Syntax for direct call for spectra image files via URL:

```
https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/spectra/300830.PNG
```
<br>

Peaks are labeled in the [human readable record](https://www.streetsafe.supply/results/p/300830), which can be [searched here](https://www.streetsafe.supply/results).<br>

Major substances in graph:<br>

+ Peak 6.65 = caffeine
+ Peak 7.2 = xylazine
+ Peak 8.74 = 4-ANPP
+ Peak 9.35 = heroin
+ Peak 9.71 = fentanyl

---
*fin.*

