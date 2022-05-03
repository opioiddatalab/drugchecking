import excel "/Users/nabarun/Dropbox/Mac/Downloads/Sample Tracking Sheet_MASTER.xlsx", sheet("Public Health Data") firstrow clear
keep Confirm* SampleID
reshape long ConfirmedSubstance, i(SampleID) j(j)
drop SampleID j
drop if ConfirmedSubstance==""
duplicates drop
replace ConfirmedSubstance=subinstr(ConfirmedSubstance," (major)","",.)
replace ConfirmedSubstance=subinstr(ConfirmedSubstance," (minor)","",.)
replace ConfirmedSubstance=subinstr(ConfirmedSubstance," (trace)","",.)
replace ConfirmedSubstance=subinstr(ConfirmedSubstance," (Ketamine precursor)","",.)
replace ConfirmedSubstance=subinstr(ConfirmedSubstance," (DMT metabolite)","",.)
replace ConfirmedSubstance=strtrim(ConfirmedSubstance)
duplicates drop
rename ConfirmedSubstance substance
export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/druglists/druglist.csv", delimiter(tab) replace
