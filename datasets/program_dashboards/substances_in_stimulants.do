

frames reset
clear all

// Directory - pull in both full datasets

cd "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/"

frame create card
frame change card

use analysis_dataset

frame create lab
frame change lab

use lab_detail

frame change card

// Limit to NC samples
keep if state=="NC"

// Create crack variable
gen crack=0 if lab_cocaine==1
	replace crack=1 if lab_cocaine==1 & regexm(expectedsubstance, "crack")
	
// Create meth variables
gen methtype = 0 if lab_meth==1
	replace methtype=1 if lab_meth==1 & crystals==1

// Create datasets for each of the 4 stimulants
	
frame put sampleid if crack==1, into(crack)
frame change crack
save crack, replace

frame change card
frame put sampleid if crack==0, into(coke)
frame change coke
save coke, replace

frame change card
frame put sampleid if methtype==1, into(crystal)
frame change crystal
save crystal, replace

frame change card
frame put sampleid if methtype==0, into(meth)
frame change meth
save meth, replace

// Extract lab results for each of the datasets

** Crack

frame change lab
merge m:1 sampleid using crack, keep(3)
gen samples=1
collapse (sum) samples (max) pubchemcid date_complete , by(substance)
rename date_complete latest
gsort -samples
export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/program_dashboards/elements/crack_lab.csv", replace
use lab_detail, clear

** Coke
merge m:1 sampleid using coke, keep(3)
gen samples=1
collapse (sum) samples (max) pubchemcid date_complete , by(substance)
rename date_complete latest
gsort -samples
export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/program_dashboards/elements/coke_lab.csv", replace
use lab_detail, clear

** Crystal meth
merge m:1 sampleid using crystal, keep(3)
gen samples=1
collapse (sum) samples (max) pubchemcid date_complete , by(substance)
rename date_complete latest
gsort -samples
export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/program_dashboards/elements/crystal_lab.csv", replace
use lab_detail, clear

** Powder meth
merge m:1 sampleid using meth, keep(3)
gen samples=1
collapse (sum) samples (max) pubchemcid date_complete , by(substance)
rename date_complete latest
gsort -samples
export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/program_dashboards/elements/powdermeth_lab.csv", replace

erase crack.dta
erase coke.dta
erase crystal.dta
erase meth.dta

use lab_detail, clear
