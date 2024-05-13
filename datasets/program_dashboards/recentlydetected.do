// This code generates a list of new drugs detected for the first time in the past 6 months days

import delimited using "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_lab_detail.csv", clear

drop lab* card-confirmatory cas unii abundance method

// Convert to date/time format
gen date = date(date_complete, "DMY")
order date, a(date_complete)
format date %td
drop date_complete

// Create group by substance
** group by substance
egen subgroup = group(substance)
sort subgroup date

** ranks occurrence of each sample by date it appeared
bysort subgroup: gen orderofappearance=_n

** Keep first occurrence of each substance
keep if orderofappearance==1

** Sort by date (might need to "ssc install gsort" to import the function the first time)
gsort -date

** Drop non-specific substances
drop if regexm(substance, "non-specific")
drop if regexm(substance, "pending")
drop subgroup

** Get today's date
gen temp = c(current_date)
gen today = date(temp, "DMY")
format today %td
drop temp

** Limit to last 6 months (183 days)
keep if date>today-183

drop order* today

rename date first_detected

export delimited using"/Users/nabarun/Documents/drugchecking/datasets/program_dashboards/elements/recentlydetected.csv", replace
