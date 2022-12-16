# UNC Drug Checking Lab Data

All samples were collected anonymously. No individually identifying information was collected.

If you are ready to start durg checking by mail, [request a startup kit](https://www.streetsafe.supply/contact).

## Individual results with chromatogram
+ [All results](https://www.streetsafe.supply/results) (searchable)
+ List of all samples [containing xylazine](https://www.streetsafe.supply/results/xylazine)
+ All [North Carolina](https://www.streetsafe.supply/results/location/nc-samples) samples

## Data Tables for Analysis

### File Inventory
+ Data collection card and sample collection instructions [PDF](https://cdr.lib.unc.edu/concern/multimeds/5d86p887m?locale=en)
+ Sample collection tutorial [video](https://vimeo.com/778263038/aae5f16d73)
+ Chem Dictionary with pronunciations and classifications [CSV](https://github.com/opioiddatalab/drugchecking/blob/main/chemdictionary/chemdictionary.csv)
+ Laboratory protocols (coming soon)
+ Decriptive methods text for proposals and manuscripts (coming soon)
+ Processing code displaying every raw data processing step and variable creation [Stata](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/result_processing.do)
+ Full documentation in codebook [TXT](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/unc_druchecking_codebook.txt)
+ Example analysis dataset with processed and derived variables (N=20) [Stata](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.dta) [Excel](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.xlsx) [SAS](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.v8xpt) [CSV](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/analysis_dataset.csv)
+ Example lab detail dataset with standardized chemical names (N=20) [Stata](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.dta) [Excel](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.xlsx) [SAS](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.v8xpt) [CSV](https://github.com/opioiddatalab/drugchecking/blob/main/datasets/lab_detail.csv)

There are two results files, `analysis_dataset.*` and `lab_detail.*`. They are provided in Stata, Excel, SAS, and CSV (tab-separated) formats. The `sampleid` variable links the datasets.<br>

The file `analysis_dataset.*` contains one row for each sample. It includes the characteristics that were reported on the card, and handy pre-processed variables to aid data analysis and visualization. The variable convention allows the analyst to quickly tabulate how many samples in the last 30 days contained fentanyl, for example.<br>

```
Stata
table date substance if fentanyl==1
```

It also contains 1/0 derived flags to help easily answer many common analytic questions, such as whether the sample contains xylazine, or if any fentanyl processing impurities (like 4-ANPP) were detected. These derived variables are indicated with the naming convention `lab_` in the variable name. The presence of particular compounds is marked `_any` in the variable name to indicate that the substance was detected in primary or trace amounts. The lack of a `_any` in the variable name means that it was the detected as a primary substance. Therefore, this sample contains xylazine in trace abundance `lab_xylazine_any=1` but not as a primary constituent `lab_xylazine=0`. It was reported to have been involved in an overdose.<br><br>


|sampleid|date collected|expected substance|location|state|color|OD involvement|lab_fentanyl|lab_fentanyl_impurity|lab_xylazine|lab_xylazine_any|
|-------:|--------------|--------|-----|-----|--------------|--------|---------------|--------|------------|------|
123|12dec2022|heroin|Raleigh|NC|blue|1|1|1|0|0|1|

<br>The `lab_detail.*` file contains one row for each substance detected for each sample. The derived variables use the same naming convention and allow for understanding how each substance is clasified. Additional variables can be constructed using searches on the `substance` variable. This file does not contain the information from the card provided during sample collection, which instead appears in `analysis_dataset.*` for the sake of data efficiency.<br><br>

| sampleid | substance | method | abundance |lab_fentanyl|lab_fentanyl_impurity|lab_xylazine|lab_xylazine_any|
|-----:|---------------|--------|-----------|------------|-----------------------|------------|----------------|
|   123| fentanyl      |GCMS    |           |1           |0                      |0           |0|
|   123| xylazine      |GCMS    |      trace|0           |0                      |0           |1|                   
|   123| 4-ANPP        |GCMS    |           |0           |1                      |0           |0|

