


frame create temp
frame change temp
import delimited "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/chemdictionary/chemdictionary.csv"
keep if `1'==1
keep substance `1'
gen i=_n
reshape wide substance, i(`1') j(i) 
keep substance* 
foreach var of varlist subs* {
	*replace `var'=`"""'+`var'+`"""'+","
	replace `var'=`var'+"|"
}
egen search=concat(subs*)
replace search = substr(search, 1, length(search) - 1) if substr(search, -1, 1) ==  "|"
replace search = `"""'+search+`"""'
keep search
local find=search[1]
frame change lab
gen lab_`1'_any=regexm(substance,`find')
la var lab_`1'_any "Detected as primary or trace"
note lab_`1'_any: "`find'"
frame drop temp





/*

foreach i of local drug {
frame create temp
frame change temp
import delimited "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/chemdictionary/chemdictionary.csv"
keep if `i'==1
keep substance `i'
gen i=_n
reshape wide substance, i(`i') j(i) 
keep substance* 
foreach var of varlist subs* {
	*replace `var'=`"""'+`var'+`"""'+","
	replace `var'=`var'+"|"
}
egen search=concat(subs*)
replace search = substr(search, 1, length(search) - 1) if substr(search, -1, 1) ==  "|"
replace search = `"""'+search+`"""'
keep search
local find=search[1]
frame change lab
gen lab_`i'_any=regexm(substance,`find')
la var lab_`i'_any "Detected as primary or trace"
note lab_`i'_any: "`find'"
frame drop temp

}

*/
