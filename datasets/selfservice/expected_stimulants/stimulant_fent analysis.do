

clear all
frames reset

use "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/analysis_dataset.dta"
distinct sampleid

// Limit to any meth samples
keep if lab_meth_any==1 | lab_cocaine_any==1
distinct sampleid

// How many trace-stim-only samples
gen tracestim = 1
	replace tracestim = 0 if lab_meth==1 | lab_cocaine==1
tab tracestim
la var tracestim "If 1 then coke/meth ONLY in trace abundance"
tab tracestim

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
tab category

// Mask geolocation
drop lat* lon*

// Fix label
la var lab_meth "meth detected in lab in primary abundance"

// Distinct program
distinct program

// Mask program names
rename program temp
egen program = group(temp)
drop temp
la var program "De-identified program index"
distinct program
drop program_county


// Crack analysis
frame put expectedsubstance lab_fentanyl tracestim sampleid, into(crack)
frame change crack
keep if tracestim==0
distinct sampleid if regexm(expectedsubstance, "crack")
tab lab_fentanyl if regexm(expectedsubstance, "crack")
frame change default

// EXPORT
export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/selfservice/expected_stimulants/stimfent_MAY.csv", quote replace

save "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/selfservice/expected_stimulants/stimfent_MAY.dta", replace

// Generate codebook on public data

log using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/selfservice/expected_stimulants/stimulant_fent_codebook.txt", text replace
codebook, n h
log close

// Export lab results
frame put sampleid, into(temp)
frame change temp
gen samples=1
save "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/temp.dta", replace

use "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/lab_detail.dta", clear

merge m:1 sampleid using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/temp.dta", keep(3) nogen

collapse (sum) samples, by(substance)
drop samples
erase "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/temp.dta"

export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/selfservice/expected_stimulants/lab_detail_MAY.csv", quote replace

frame change default

// Flow diagram
frame put *, into(flow)
frame change flow
keep if tracestim==0
tab lab_fentanyl if category==1
tab lab_fentanyl crystal if category==1, m

/*
// Number of non-crack cocaine sampels testing + for fentanyl
tab lab_fentanyl if category==2 & regexm(expectedsubstance, "crack")==0

// For donuts

tab expect_fentanyl if lab_fentanyl==1 & category==1 & crystals!=1
tab expect_fentanyl if lab_fentanyl==1 & category==2 & regexm(expectedsubstance, "crack")!=1
