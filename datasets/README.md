# UNC Drug Checking Lab Data


*This documentation is in beta release. Code will undergo QC as we finalize.*
<br>
<br>
All samples were collected anonymously. No individually identifying information was collected.

If you are ready to start durg checking by mail, [request a startup kit](https://www.streetsafe.supply/contact).

# File Inventory
+ Full documentation in [codebook](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/unc_druchecking_codebook.txt)
+ [Processing code](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/code/result_processing.do) showing variable creation
+ [Google Sheets](https://docs.google.com/spreadsheets/d/13tXdH9tdAcSNcyEA7Y6F8hdgu2tygL3ePUrxHSRY0OA/edit?usp=sharing) viewer
+ `analysis_dataset` Example analysis dataset with processed and derived variables (N=20) [Stata](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.dta) [Excel](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.xlsx) [SAS](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.v8xpt) [CSV](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.csv)
+ `lab_detail` Example lab detail dataset with standardized chemical names (N=20) [Stata](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.dta) [Excel](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.xlsx) [SAS](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.v8xpt) [CSV](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.csv)

<br>

# File Formats
Results files `analysis_dataset.*` and `lab_detail.*` are provided in:
+ Stata (v14 or later)
+ Excel (.xlsx)
+ SAS (transport v8)
+ CSV (comma-separated with quote enclosure for strings)

<br>

The `sampleid` variable links the datasets `analysis_dataset.*` and `lab_detail.*`.<br>

<br>

For a quick view of the data, see this [Google Sheets](https://docs.google.com/spreadsheets/d/13tXdH9tdAcSNcyEA7Y6F8hdgu2tygL3ePUrxHSRY0OA/edit?usp=sharing) example as a single file with 2 tabs.

<br>

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

<br>

# Lab Detail Dataset
The `lab_detail.*` file contains one row for each substance detected for each sample. The derived variables use the same naming convention and allow for understanding how each substance is clasified. Additional variables can be constructed using searches on the `substance` variable. This file does not contain the information from the card provided during sample collection, which instead appears in `analysis_dataset.*` for the sake of data efficiency. This also allows you to see trace back and see how variable was contructed at an individual chemical level.<br><br>

| sampleid | substance | method | abundance |lab_fentanyl|lab_fentanyl_impurity|lab_xylazine|lab_xylazine_any|
|-----:|---------------|--------|-----------|------------|-----------------------|------------|----------------|
|   123| fentanyl      |GCMS    |           |1           |0                      |0           |0|
|   123| xylazine      |GCMS    |      trace|0           |0                      |0           |1|                   
|   123| 4-ANPP        |GCMS    |           |0           |1                      |0           |0|

<br>

You can import the example `lab_detail.csv` instantly into Google sheets by pasting this one line of code into the first cell (A1):
```
=importData("https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/lab_detail.csv")

```

# GCMS Chromatograms

![chromatogram](https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/spectra/300830.PNG)

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

# Human readable outputs
+ [All results](https://www.streetsafe.supply/results) (searchable)
+ List of all samples [containing xylazine](https://www.streetsafe.supply/results/xylazine)
+ All [North Carolina](https://www.streetsafe.supply/results/location/nc-samples) samples
+ [NLP code](https://github.com/opioiddatalab/drugchecking/blob/main/textexport/autotext.do) for converting sample results into human readable indivdual records for [website](https://streetsafe.supply)


# Other Resources
+ [List of all substances detected](https://github.com/opioiddatalab/drugchecking/blob/main/chemdictionary/substances_detected.csv) with frequencies
+ Data collection card and sample collection instructions [PDF](https://cdr.lib.unc.edu/concern/multimeds/5d86p887m?locale=en)
+ Sample collection tutorial [video](https://vimeo.com/778263038/aae5f16d73)
+ [Chemical Dictionary](https://github.com/opioiddatalab/drugchecking/tree/main/chemdictionary) with pronunciations and classifications
+ [Canonical list](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/code/completed.csv) of all completed sample ID
