

frames reset
clear all

// Pull in NC specific datasets
use "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/nc/nc_analysis_dataset.dta"

frame create lab
frame change lab

use "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/datasets/nc/nc_lab_detail.dta"

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





erase templist
