* state names and abbreviations
clear all
cd "/Users/nabarun/Dropbox/Mac/Documents/GitHub/List-of-US-States"
import delimited states.csv, varname(1)
rename state statename
rename abbreviation state
set obs `=_N+1'
replace statename = "Puerto Rico" in 52
replace state = "PR" in 52

cd "/Users/nabarun/Dropbox/Projects/Autotext for drug checking/"


save states, replace


// Get posted products from Squarespace API
** Retrives last 50 sample ID numbers that have been posted to create canonical list
** Code hidden to protect endpoint

do "/Users/nabarun/Dropbox/Mac/Documents/GitHub/dc_internal/sqapi_last50.do"

// Download the data file and modify
* change file extension from .xlsm to .xlsx
! mv "/Users/nabarun/Dropbox/Mac/Downloads/LabResults.xlsm" "/Users/nabarun/Dropbox/Projects/Autotext for drug checking/LabResults.xlsm"
! mv "LabResults.xlsm" "LabResults.xlsx"
! rm "/Users/nabarun/Dropbox/Mac/Downloads/LabResults.xlsm"

* Import common names/explanations of substances 
*import excel "LabResults.xlsx", sheet("druglist") firstrow case(lower) clear
*keep chemicalname commonrole pronunciation
*rename chemicalname substance
*duplicates drop
*frame put *, into(translation)

// Harm Reduction Chemical Dictionary
*frame change translation
*export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/chemdictionary/chemdictionary.csv", quote replace
*frame change default


* Import lab data
import excel "LabResults.xlsx", sheet("LAB data") firstrow case(lower) clear
drop f g
drop if sampleid == ""
drop if lab_status== "pending"

replace sampleid=subinstr(sampleid,"_","-",.)

frame put *, into(lab) 

* Import card data
import excel "/Users/nabarun/Dropbox/Projects/Autotext for drug checking/LabResults.xlsx", sheet("CARD data") firstrow case(lower) clear
drop  linkedsample howlongagowasthesampleobta

* Variable cleanup
** residue
gen residueflag = regexm(lower(sampletype),"residue|cotton|swab")
order residueflag, a(sampletype)
	la var residueflag "Dichotmous flag for reside sample from cotton or swab 1=resiude"

** date
gen date_sample = date(date, "MDY")
	la var date_sample "Date sample collected"
order date_sample, a(date)
format date_sample %td

** overdose
gen odflag = regexm(lower(overdose), "involved")
	la var odflag "Dichotmous flag for OD involvement 1=OD"
		order odflag, a(overdose)

** pill flag
gen pillflag = regexm(lower(sampletype), "pill") | regexm(lower(texture), "pill")
	order pillflag, a(texture)
		la var pillflag "Composite dichotomous flag for pills, real or counterfeit, 1=pill"

		
* add state names for search
merge m:1 state using states, nogen keep(1 3)
drop state
rename statename state		
		
* Generate text: Location and date
replace date = subinstr(date," ", "",1)
gen t_location = "From " + location + ", " + state + " on " + date
	replace t_location = "From " + state + " on " + date if location=="" | regexm(lower(location),"spec")
	replace t_location = "From " + state if date==""
	replace t_location = "Collected on " + date if state==""
	replace t_location = "" if state=="" & date=="" | lower(date)=="unknown" | regexm(lower(state),"international")


 * Color and texture
gen temp_color=color
	replace temp_color="" if regexm(lower(color), "not spec")
gen temp_texture=texture
	replace temp_texture="" if regexm(lower(texture), "not spec")
gen t_color="Looks = " + temp_color + " " + temp_texture + "<br><br>"
	replace t_color = "Looks = " + temp_color + "<br><br>" if temp_texture==""
	replace t_color = "Looks = " + temp_texture + "<br><br>" if temp_color==""
	replace t_color = "Appearance not described" if temp_color=="" & temp_texture==""
		drop temp*
	replace t_color = subinstr(t_color,";",",",.)

* Sensations
gen t_sensations="Sensations = " + sensations + "<br><br>"
	replace t_sensations="Sensations not reported" if regexm(lower(sensations), "not specified|not used by participant") | sensations==""
	replace t_sensations = subinstr(t_sensations,";",",",.)
			
* Overdose involvement
gen t_od = "<strong>Careful! This sample caused an overdose.</strong>" + "<br><br>" if regexm(overdose,"OD")
	replace t_od = "Not involved in overdose." + "<br><br>" if regexm(overdose,"not")
	replace t_od = "Not sure if caused overdose." + "<br><br>" if regexm(overdose,"unknown")
	
* Expected Drug
gen t_expected = "Assumed to be " + expectedsubstance
	replace expectedsubstance=subinstr(expectedsubstance, "Unknown", "unknown", 1)
		gen temp_expected=subinstr(expectedsubstance,"; unknown"," and something else?",1) if regexm(expectedsubstance,"unknown")
			replace t_expected = "Assumed to be " + temp_expected if regexm(expectedsubstance,"unknown")
	replace t_expected = "Unclear what it was before the lab" if expectedsubstance=="unknown" | expectedsubstance=="other"
		drop temp*
		replace t_expected = subinstr(t_expected,";",",",.)
		
gen t_labnotes="<br> Lab Notes: " + lab_notes_share + "<br>"
		
// Flag recent samples
gen catt8="recent" if date_sample>today()-62 & date_sample!=.

		
quietly compress
frame put *, into(card)

frame put sampleid  t_* date_sample catt8, into(text)  
sort date_sample
	
// Lab Results

* Commonality of substances

frame change lab

distinct sampleid

** Number of substances
bysort sampleid: egen totalsubstances=count(substance)
	la var totalsubstances "Total number of substances detected in sample"


frame put sampleid substance, into(common)
frame change common
gen counter=1
collapse (sum) counter, by(substance)
means counter
gen uncommon=0
	replace uncommon=1 if counter<r(mean_h)
		la var uncommon "Substances ocurring less frequently than harmonic mean of frequency in entire databse"
		
// Uncommon Substances
		
frame change lab
frlink m:1 substance, frame(common)
frget uncommon, from(common)

frame put sampleid substance if uncommon==1, into(uncommontext)
frame change uncommontext
bysort sampleid: gen counter=_n
reshape wide substance, i(sampleid) j(counter)
egen t_temp = concat(substance*), punct(" + ")
replace t_temp=subinstr(t_temp,"  +  +","",.)
replace t_temp=subinstr(t_temp," +  +","",.)
replace t_temp=regexr(t_temp," \+$","")
drop substance*
gen t_uncommon = "Uncommon substance(s): " + t_temp

frame change text
frlink 1:1 sampleid, frame(uncommontext)
frget t_uncommon, from(uncommontext)
drop uncommontext
	
* Frames for major and minor
frame change lab
frame put sampleid substance if abundance=="", into(major)
frame put sampleid substance if abundance=="trace", into(trace)
frame put sampleid substance if abundance=="indication of", into(hint)

* Major substances

frame change major
bysort sampleid: gen counter=_n
bysort sampleid: egen maxnum=max(counter)

** use this later to insert vernacular names
frame put sampleid substance, into(linebyline)
*** end of that section

reshape wide substance, i(sampleid) j(counter)

* drop pending
drop if substance1==""

foreach var of varlist substance* {
	
	replace `var' = "<li>" + `var' + "</li>"
	
}

foreach var of varlist substance* {
	
	replace `var' = "" if `var'=="<li></li>"
	
}


egen t_temp = concat(substance*), punct("")
drop substance*

tostring maxnum, g(maxstr)
gen t_preamble = "Only " + maxstr + " major substance detected:"
replace t_preamble = maxstr + " major substances detected:" if maxnum>1
replace t_preamble = "This is a messy brew of " + maxstr + " major substances:" if maxnum>5

gen t_major = "<strong>" + t_preamble + "<ul>" + t_temp + "</ul>" + "</strong>"
replace t_major = "<strong>" + "Sorry, no substances of interest detected." + "</strong>" if regexm(t_temp,"no compounds")

drop t_temp t_preamble maxstr maxnum

frame change text
frlink 1:1 sampleid, frame(major)
frget t_major, from(major)
drop major


* Trace results
frame change trace
bysort sampleid: gen counter=_n
bysort sampleid: egen maxnum=max(counter)
reshape wide substance, i(sampleid) j(counter)
egen t_temp = concat(substance*), punct(" + ")
replace t_temp=subinstr(t_temp,"  +  +","",.)
replace t_temp=subinstr(t_temp," +  +","",.)
replace t_temp=regexr(t_temp," \+$","")
drop substance*
tostring maxnum, g(maxstr)
gen t_trace = "And we also found traces of " + t_temp + "."
replace t_trace = "But we found lots of contaminants too, with traces of " + t_temp + "." if maxnum>3

frame change text
frlink 1:1 sampleid, frame(trace)
frget t_trace, from(trace)
drop trace


* Indication of results
frame change hint
bysort sampleid: gen counter=_n
reshape wide substance, i(sampleid) j(counter)
egen t_temp = concat(substance*), punct(" + ")
replace t_temp=subinstr(t_temp,"  +  +","",.)
replace t_temp=subinstr(t_temp," +  +","",.)
replace t_temp=regexr(t_temp," \+$","")
drop substance*
gen t_hint = "There was also a hint of " + t_temp + ", but we were unable to see it clearly.<br><br>"
drop t_temp

frame change text
frlink 1:1 sampleid, frame(hint)
frget t_hint, from(hint)
drop hint

* Scientific info
frame change lab
drop date* method common uncommon
*drop if peak==""
drop if peak==.
drop if abundance=="trace"
drop abundance lab_status
tostring peak, replace
replace peak=subinstr(peak,"9999999999999","",.)
replace peak=subinstr(peak,"0000000000001","",.)
gen text = "Peak " + peak + " = " + substance
sort sampleid peak
bysort sampleid: gen counter=_n
drop substance peak* spectra_uploaded lab_notes
reshape wide text, i(sampleid) j(counter)

foreach var of varlist text* {
	
	replace `var' = "<li>" + `var' + "</li>"
	
}

foreach var of varlist text* {
	
	replace `var' = "" if `var'=="<li></li>"
	
}


egen t_temp = concat(text*), punct("")
drop text*
gen t_detail = "<strong>Major substances in graph:<br></strong><ul>" + t_temp + "</ul>"
drop t_temp

frame change text
frlink 1:1 sampleid, frame(lab)
frget t_detail, from(lab)
drop lab
replace t_detail="" if regexm(t_major,"Sorry")

// Lab notes



// Add warnings and notes

** Xylazine
gen t_xylazine = "<strong>Xylazine</strong> causes serious skin problems. These can happen anywhere on the body and don't heal quickly. And, <strong>xylazine</strong> can come on stronger than traditional dope and knock you out, so <strong>be mindful of your surroundings</strong>. It's best to avoid dope with xylazine. You might need medical attention to prevent long-term damage.<br><br>" if regexm(lower(t_major), "xylazine") | regexm(lower(t_trace), "xylazine")

** Fentanyl
gen t_fentanyl = "There were just traces of <strong>fentanyl</strong>. This could have been contamination, like if drugs were stored in old bags. But since fentanyl is so potent you should be prepared. Consider getting <strong>fentanyl test strips</strong> online or from a harm reduction program if you weren't expecting it. <strong>Carry naloxone (Narcan)</strong> to reverse overdoses. Even traces of fentanyl could be a problem if you don't use opioids regularly. <strong>Don't use alone</strong> so someone can help if you go out.<br><br>" if regexm(lower(t_trace), "fentanyl")


replace t_fentanyl = "<strong>Fentanyl</strong> is potent and the amount changes by batch. If you weren't expecting it, consider getting test strips online or from a harm reduction program. <strong>Carry naloxone (Narcan)</strong> to reverse overdoses. <strong>Don't use alone</strong> so someone can help if you go out.<br><br>" if regexm(lower(t_major), "fentanyl")

** Complex mixtures
gen t_mix = "There are a lot of different substances in this sample. We don't know the harms that some of these can cause. Be careful and be prepared for unexpected reactions.<br><br>" if strlen(t_major)>120

** fluorofentanyl
gen t_fluoro = "<strong>Fluorofentanyl</strong> is showing up recently. It's the result of different raw materials being used to make fentanyl. We don't know yet if it causes any specific problems.<br><br>" if regexm(lower(t_major), "fluorofentanyl") | regexm(lower(t_trace), "fluorofentanyl")

** Unknown substance
gen t_unknown = "This sample contains unknown substances(s). This means we couldn't find a match for it in our library. It could be a new chemical or something that's interfering with our machine. We are investigating it and will update the results.<br><br>" if regexm(lower(t_major), "unknown substance") | regexm(lower(t_trace), "unknown substance")

** Sugar peaks
gen t_sugars = "Non-specific sugars won't show up on the graph. See note below under 'What we can and can't tell'. <br><br>" if regexm(lower(t_major), "sugars") | regexm(lower(t_trace), "sugars")

** Peaks caveat
gen t_caveat = "Peaks that don't appear on the graph were detected using other advanced methods. If a peak appears on the graph but isn't listed above, then we reviewed it and determined it is inactive background noise. Contact us if you want details." + "<br><br>" if regexm(t_detail,"Major substances in graph")
replace t_caveat="" if regexm(lower(t_major),"no substances of interest detected")

** Pill caveat
gen t_pill = "For pills and fake pills, you may see extra peaks on the left hand part of the chromatogram. These represent fillers and trace chemicals from the pill binder. These substances are better isolated using infrared light (FTIR), and GCMS only provides limited information. See note below under 'What we can and can't tell'. Contact us if you want details.<br><br>" if regexm(lower(t_detail), "pill|xanax|alprazolam|m30|fake|counterfeit")

** Trace
gen t_tracetext="Trace substances in small quantities are usually harmless, but can sometimes cause health problems. Unexpected sensations may be due to these.<br><br>" if t_trace!=""

// Harm Reduction program information
gen t_hr = "Need free supplies and advice to keep you safe? Find your nearest harm reduction program at harmreduction.org<br><br>"
replace t_hr = "The Xchange in Greensboro can help provide you with free supplies and advice to stay safe. 'If you want to improve your life we are here to help you. One goal at a time. You make the goals... we listen to you.'<br>1114 Grove Street, Greensboro, NC 27403<br>Phone: 336-669-5543<br>Open: Mon 1-7pm, Tue 1-7pm, Thu 1-5pm, Fri 1-8pm<br>ncurbansurvivorunion.org<br><br>" if regexm(lower(t_location),"greensboro")

// Methods details
* Import lab data
frame create labtemp
frame change labtemp
import excel "/Users/nabarun/Dropbox/Projects/Autotext for drug checking/LabResults.xlsx", sheet("LAB data") firstrow case(lower) clear
frame put sampleid method, into(method)
frame change method
duplicates drop
drop if sampleid==""
gsort sampleid -method
bysort sampleid: gen counter=_n
reshape wide method, i(sampleid) j(counter)
egen t_method = concat(method*), punct(" + ")
replace t_method=subinstr(t_method,"  +  +","",.)
replace t_method=subinstr(t_method," +  +","",.)
replace t_method=regexr(t_method," \+$","")

frame change text
frlink 1:1 sampleid, frame(method)
frget t_method, from(method)
drop method

/// CREATE CANONINCAL LIST OF SAMPLES AND FLAG TO MOST RECENT
*frame create posted
*frame put sampleid, into(posted)

** Record update date
gen t_recorddate = "Record for Sample " + sampleid + " last updated " + "$S_DATE" + "."

// Remove missing fields
replace t_color="" if t_color=="Appearance not described"
replace t_sensations="" if t_sensations=="Sensations not reported"
replace t_od="" if t_od=="Not sure if caused overdose."

// Assemble for HTML
gen Description = "<p>" + t_location + "<br>" + t_expected + "<br><br>" + t_major + "<br>" + t_trace + t_tracetext + t_hint + t_fentanyl + t_xylazine + t_unknown + t_mix + t_fluoro + t_color + t_hr + t_detail + "<br>" + "Method(s): " + t_method + "<br>" + t_caveat + t_pill + t_labnotes + t_recorddate


// File cleanup and save
frame change text
keep if t_major!=""

order t_expected t_major t_trace, a(t_location)
order t_detail, last


save text, replace

export excel using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/textexport/textexport.xls", firstrow(variables) replace

* Delete original excel file
*! rm "LabResults.xlsm" "LabResults.xlsx"


// Save pending list
import excel "LabResults.xlsx", sheet("LAB data") firstrow case(lower) clear
keep sampleid lab_status
replace sampleid=subinstr(sampleid,"_","-",.)
keep if regexm(lab_status,"pending")
gen mail="received by lab"
order mail, first
drop if sampleid==""
tab sampleid
append using allcomplete 
tab lab_status
drop if lab_status=="" & r(N)>1
gen status_date="$S_DATE"
duplicates drop
sort sampleid
export delimited using "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/status/pending.csv", quote replace
** Share copies to Dropbox for Erin
! rm "/Users/nabarun/Dropbox/Drug Checking Autotext/upload_for_import.csv"
export delimited using "/Users/nabarun/Dropbox/Drug Checking Autotext/pending.csv", quote replace

// Open final text file back up
use text, clear
keep sampleid Description catt8
gen productid=""
gen variantid=""
gen producttype="PHYSICAL"
gen productpage="results"
gen productURL=sampleid
gen title=sampleid
order Description, a(title)
gen SKU=""
gen optionname1=""
gen optionvalue1=""
gen optionname2=""
gen optionvalue2=""
gen optionname3=""
gen optionvalue3=""
gen price=0
gen saleprice=0
gen onsale="No"
gen stock="Unlimited"
gen tags=""
gen weight=""
gen length=""
gen width=""
gen height=""
gen visible="Yes"

* Create categories
	gen catt1="xylazine" if regexm(lower(Description),"xylazine")
	gen catt2="fentanyl" if regexm(lower(Description),"fentanyl")
	gen catt3="/location/nc-samples" if regexm(lower(Description),"north carolina")
	gen catt4="overdoses" if regexm(lower(Description),"this sample caused an overdose")
	gen catt5="stimulants" if regexm(lower(Description),"cocaine|methamphetamine|crack")
	gen catt6="psychedelics" if regexm(lower(Description),"dmt|mdma|molly|mushrooms|psilocybin")
	gen catt7="werid-samples" if regexm(lower(Description),"uncommon substance(s):")
	* gen catt8="recent" if regexm(t_recent,"recent")
	gen catt9="fake-pills" if regexm(lower(Description),"pill")
	gen catt10="/location/texas" if regexm(lower(Description),"texas")
	gen catt11="/location/new-york" if regexm(lower(Description),"new york")
	
	* Put categories together
		egen categories=concat(catt*), punc(", ")
			order categories, a(stock)
				replace categories=subinstr(categories," ,","",.)
				replace categories="" if categories==","
				replace categories=subinstr(categories,"^, ","",1)
				gen flag = regexm(categories,"^, ")
					order flag,a(categories)
						replace categories=subinstr(categories,", ","",1) if flag==1
							drop flag
				replace categories=regexr(categories,",$","")
					drop catt*

* Add images from GitHub				
* (Separate multiple images with spaces or line breaks.)	
gen hostedimage="https://opioiddatalab.github.io/drugchecking/spectra/" + sampleid + ".PNG"


// For manual updates of specific samples, keep the following line and comment out the merge with canonical_list.
* keep if sampleid=="300398" | sampleid=="300349"

// Check against canonical list to only keep samples that have not been uploaded to site
merge 1:1 title using canonical_list, keep(1) 

* Drop error sample
drop if title=="06082021"

drop sampleid

export delimited using "/Users/nabarun/Dropbox/Projects/Autotext for drug checking/textexport.csv", novarnames quote replace

! rm "/Users/nabarun/Dropbox/Projects/Autotext for drug checking/LabResults.xlsx"
! rm "/Users/nabarun/Dropbox/Projects/Autotext for drug checking/upload_for_import.csv"
! rm "/Users/nabarun/Dropbox/Drug Checking Autotext/upload_for_import.csv"


python
import pandas as pd
df = pd.read_csv("/Users/nabarun/Dropbox/Projects/Autotext for drug checking/textexport.csv", header=None)
df.rename(columns={0: 'Product ID [Non Editable]', 1: 'Variant ID [Non Editable]', 2: 'Product Type [Non Editable]', 3: 'Product Page', 4: 'Product URL', 5: 'Title', 6: 'Description', 7: 'SKU', 8: 'Option Name 1', 9: 'Option Value 1', 10: 'Option Name 2', 11: 'Option Value 2', 12: 'Option Name 3', 13: 'Option Value 3', 14: 'Price', 15: 'Sale Price', 16: 'On Sale', 17: 'Stock', 18: 'Categories', 19: 'Tags', 20: 'Weight', 21: 'Length', 22: 'Width', 23: 'Height', 24: 'Visible', 25: 'Hosted Image URLs'}, inplace=True)
df.to_csv("/Users/nabarun/Dropbox/Projects/Autotext for drug checking/upload_for_import.csv", index=False)
df.to_csv("/Users/nabarun/Dropbox/Drug Checking Autotext/upload_for_import.csv", index=False)

end

clear all
frames reset


// GitHub commit
* ! cd "/Users/nabarun/Dropbox/Mac/Documents/GitHub/drugchecking/status/"
* ! cd git commit -a -m "automated daily results update"
