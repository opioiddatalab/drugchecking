# UNC Drug Checking Chemical Dictionary
<br>
The CSV file above is a canonical list of substances detected/execpted by the UNC drug checking lab starting in 2021.
<br><br>

## File and Variable Conventions
+ Chemical names are listed in the first column `substance`
+ Columns correspond to drug classes. A 1/0 column flag is used to indicate class membership (1=yes).
+ Pronunication guide is there as suggestions, and a work in progress. Feel free to submit suggestions.
+ A substance can have more than one category classification.
<br><br>

## Considerations
+ Substances are added to this list once they are detected in our lab. Hence, this should not be considered an exhaustive list of substances in any category.
+ For each new chemical detected, we classify it based on our expertise, scientific literature, and professional concensus.
+ Classifiations are intended to be most relevant for public health and drug checking professionals.
+ Chemical names are standardized according to our internal expertise and conventions. They may or may not match literal text in cheminformatics databases without additional pre-processing. Example: `p-fluorofentanyl` versus `para-fluorofentaynl`
+ The `commonrole` column is being worked on and not standardized. Use with discretion and submit suggestions.


## Progammers Note
Direct path access to raw CSV 
```
https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/chemdictionary/chemdictionary.csv
```
