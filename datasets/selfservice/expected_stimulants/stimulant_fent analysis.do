

clear all
frames reset

use "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/analysis_dataset.dta"
distinct sampleid

keep if lab_meth_any==1 | lab_cocaine_any==1
distinct sampleid

keep if lab_meth==1 | lab_cocaine==1
distinct sampleid

// Create categories of samples
gen category = .
	replace category = 1 if lab_meth==1 & lab_cocaine==0
	replace category = 2 if lab_meth==0 & lab_cocaine==1
	replace category = 3 if lab_meth==1 & lab_cocaine==1
	label define cat 1 "Methamphetamine" 2 "Cocaine" 3 "Both"
	label values category cat
tab category, m

