
*import delimited "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/selfservice/expected_stimulants/stimfent_MAY.csv", clear

use "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/analysis_dataset.dta", clear


// Selection Criteria
keep if lab_meth==1 | lab_cocaine==1

// Swab indicator
gen swab=0
	replace swab=1 if regexm(collection,"swab")
	
// Weird sensations
gen weird=0
	replace weird=1 if sen_weird==1
	
// Crystals
gen crystal10 = 0
	replace crystal10=1 if crystals==1
	
// Variable formats
rename countyfips temp
encode temp, g(countyfips)

// Modeling
glm lab_fentanyl, l(identity) 

glm lab_fentanyl confirmatory consumed weird swab, l(identity) vce(r)

xtset countyfips
xtgee lab_fentanyl, f(normal) link(identity) 
xtgee lab_fentanyl confirmatory consumed weird swab, f(normal) link(identity) vce(r)

xtgee lab_fentanyl confirmatory consumed weird swab, f(normal) link(identity) vce(r)


// Cocaine
xtgee lab_fentanyl confirmatory consumed weird swab if lab_cocaine==1 & lab_meth!=1, f(normal) link(identity) vce(r)


// Methamphetamine
xtgee lab_fentanyl confirmatory consumed weird swab  if lab_meth==1 & lab_cocaine!=1, f(normal) link(identity) vce(r)

// Texture
** Cocaine
xtgee lab_fentanyl confirmatory consumed weird swab if lab_cocaine==1 & lab_meth!=1 & crystals!=1, f(normal) link(identity) vce(r)


** Methamphetamine
**** Powder
xtgee lab_fentanyl confirmatory consumed weird swab  if lab_meth==1 & lab_cocaine!=1 & crystals!=1, f(normal) link(identity) vce(r)


xtgee lab_fentanyl confirmatory consumed weird swab  if lab_meth==1 & lab_cocaine!=1 & crystals!=1, corr(exch) f(p) link(log) vce(r) eform scale(x2)


**** Crystal
xtgee lab_fentanyl confirmatory consumed weird swab  if lab_meth==1 & lab_cocaine!=1 & crystals==1, f(normal) link(identity) vce(r)




// IRR for meth
** recode to get interpretable direction 
gen crystal01 = 0
	replace crystal01 = 1 if crystal10==0
	
** convert date
*gen date2=date(date_collect, "DMY")
*xtset countyfips date2

glm lab_fentanyl crystal01 confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1, f(p) link(log) vce(r) eform

xtset countyfips
xtgee lab_fentanyl confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1, corr(exch) f(poisson) link(identity) vce(r) scale(x2)

xtgee lab_fentanyl confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1, corr(exch) f(nb) link(identity) vce(r)

xtset countyfips
xtgee lab_fentanyl crystal01 confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1, corr(exch) f(nb) link(log) vce(r) eform scale(x2)

xtset countyfips
xtgee lab_fentanyl crystal01 confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1, corr(exch) f(gaussian) link(identity) vce(r) eform


xtset countyfips
xtreg lab_fentanyl confirmatory consumed weird swab, re vce(r) 




/////// Fentanyl positivity


*** Both
xtgee lab_fentanyl confirmatory consumed weird swab, corr(exch) f(nb) link(identity) vce(r)

*** Meth
xtgee lab_fentanyl confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1, corr(exch) f(nb) link(identity) vce(r)

*** Coke
xtgee lab_fentanyl confirmatory consumed weird swab if lab_cocaine==1 & lab_meth!=1, corr(exch) f(gaussian) link(identity) vce(r) nolog
matrix b=e(b)
xtgee lab_fentanyl confirmatory consumed weird swab if lab_cocaine==1 & lab_meth!=1, corr(exch) f(nb) link(identity) vce(r) from(b, skip)


/////// By texture

*** Crystal meth
xtgee lab_fentanyl confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1 & crystals==1, corr(exch) f(gaussian) link(identity) vce(r)


*** Powder Meth
xtgee lab_fentanyl confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1 & crystals!=1, corr(exch) f(gaussian) link(identity) vce(r)
matrix b=e(b)
xtgee lab_fentanyl confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1 & crystals!=1, corr(exch) f(nb) link(identity) vce(r) from(b, skip)

////// IRR Methamphetamine
xtset countyfips
xtgee lab_fentanyl crystal01 confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1, corr(exch) f(nb) link(log) vce(r) eform scale(x2)


//// Powder cocaine
xtgee lab_fentanyl confirmatory consumed weird swab if lab_meth!=1 & lab_cocaine==1 & crystals!=1, corr(exch) f(gaussian) link(identity) vce(r) nolog
matrix b=e(b)
xtgee lab_fentanyl confirmatory consumed weird swab if lab_meth!=1 & lab_cocaine==1 & crystals!=1, corr(exch) f(nb) link(identity) vce(r) from(b, skip)




//////////////////// Expectations

//// Powder cocaine
xtgee lab_fentanyl expect_fentanyl confirmatory consumed weird swab if lab_meth==1 & lab_cocaine!=1 & crystals!=1, corr(exch) f(gaussian) link(identity) vce(r) nolog noconstant

matrix b=e(b)
xtgee lab_fentanyl confirmatory consumed weird swab if lab_meth!=1 & lab_cocaine==1 & crystals!=1, corr(exch) f(nb) link(identity) vce(r) from(b, skip)
