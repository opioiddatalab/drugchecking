

frames reset
clear all

// Pull in NC specific datasets
use "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/nc/nc_analysis_dataset.dta"

frame create lab
frame change lab

use "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/lab_detail.dta"

frame change default

/////////////////////////
//                    //
//    Xylazine NC    //
//                  //
/////////////////////


keep if state=="NC" & lab_xylazine_any==1


// List of relevant samples
frame copy default list
frame change list
keep sampleid
save templist, replace

frame change lab

merge m:1 sampleid using templist, nogen keep(3)


erase "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/templist.dta"


// What other substances were detected?
gen counter=1
drop if substance=="xylazine"
collapse (sum) counter, by(substance)
gsort -counter
rename counter samples
gen rank = _n

export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/code/Streamlit/x_subs.csv", quote replace

// What sensations were reported?
