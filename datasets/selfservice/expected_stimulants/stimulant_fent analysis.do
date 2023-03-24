

clear all
frames reset

use "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/analysis_dataset.dta"
distinct sampleid

// Limit to any meth samples
keep if lab_meth_any==1 | lab_cocaine_any==1
distinct sampleid

// How many trace only samples
gen tracestim = 0
	replace tracestim = 1 if lab_meth_any==1 & lab_meth==0
	replace tracestim = 1 if lab_cocaine_any==1 & lab_cocaine==0 & tracestim==.
tab tracestim
la var tracestim "If 1 then coke/meth ONLY in trace abundance"

// For flow diagram: How many trace-stimulant-only are fent in primary abundance?
distinct sampleid if tracestim==1 & lab_fentanyl==1

// Create categories of samples
gen category = .
	replace category = 1 if lab_meth==1 & lab_cocaine==0
	replace category = 2 if lab_meth==0 & lab_cocaine==1
	replace category = 3 if lab_meth==1 & lab_cocaine==1
	label define cat 1 "Methamphetamine" 2 "Cocaine" 3 "Both"
	label values category cat
	la var category "1 if primary meth, 2 if primary cocaine, 3 if both"
	order category, a(tracestim)
tab category, m

// Mask geolocation
drop lat* lon*

// Fix label
la var lab_meth "meth detected in lab in primary abundance"

// Mask program names
rename program temp
bysort temp: gen program = _n
drop temp
la var program "De-identified program index"
drop program_county

export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/selfservice/expected_stimulants/stimfent.csv", quote replace

// Generate codebook on public data

log using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/selfservice/expected_stimulants/stimulant_fent_codebook.txt", text replace
codebook, n h
log close
