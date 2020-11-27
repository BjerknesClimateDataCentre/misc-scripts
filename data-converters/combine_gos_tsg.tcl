#!/usr/bin/tclsh

# Simple script to merge data from General Oceanics and TSG files
# Should be generalised at some point, but I don't have motivation now.

set CO2_FILE "GOS_2020-101-1222dat.txt"
set TSG_FILE "TSG.csv"
set OUT_FILE "GOS_2020-101-1222dat-mergedTSG.txt"

set RED "\033\[0,31m"
set GREEN "\033\[0;32m"

set TSG_DATE_COL 0
set TSG_COPY_COLUMNS [list 6 8]

# Read in GOS data
set chan [open $CO2_FILE "r"]
set data [read $chan]
close $chan

set co2Lines [split $data "\n"]
unset data

# Read in TSG data
set chan [open $TSG_FILE "r"]
set data [read $chan]
close $chan

set tsgLines [split $data "\n"]
unset data


# Open the output file
set outChan [open $OUT_FILE "w"]
puts $outChan "Type\terror\tPC Date\tPC Time\tGPS date\tgps time\tlatitude\tlongitude\tequ temp\tstd val\tCO2 mv\tCO2 um/m\tH2O mv\tH2O mm/m\tlicor temp\tlicor press\tatm press\tequ press\tH2O flow\tlicor flow\tequ pump\tvent flow\tatm cond\tequ cond\tdrip 1\tdrip 2\tcond temp\tdry box temp\tdeck box temp\tOxygen\tSaturation\tTemperature\tWBPressure\tIntake Temp\tSalinity\tFluoresc\tTSG_SST\tTSG_Salinity"

set currentTSGRow 0
set currentTSGLine [split [lindex $tsgLines 0] ","]
set currentTSGDate [clock scan [lindex $currentTSGLine $TSG_DATE_COL] -format "%Y-%m-%dT%H:%M:%SZ" -gmt true]
set tsgFinished 0

# Skip header
set currentCO2Row 1
set currentCO2Line [lindex $co2Lines 1]
set currentCO2Date [clock scan "[lindex [split $currentCO2Line "\t"] 2] [lindex [split $currentCO2Line "\t"] 3]" -format "%d/%m/%y %H:%M:%S" -gmt true]
set co2Finished 0

while {!$co2Finished && !$tsgFinished} {

    set foundClosestTSGLine 0
    set currentDiff [expr abs($currentTSGDate - $currentCO2Date)]

    while {!$foundClosestTSGLine} {
        set currentDiff [expr abs($currentTSGDate - $currentCO2Date)]
        set nextDiff [expr $currentDiff + 1]

        set nextTSGLine [split [lindex $tsgLines [expr $currentTSGRow + 1]] ","]
        if {[llength $nextTSGLine] > 0} {

            set nextTSGDate [clock scan [lindex $nextTSGLine $TSG_DATE_COL] -format "%Y-%m-%dT%H:%M:%SZ" -gmt true]
            set nextTSGRow [expr $currentTSGRow + 1]
            set nextDiff [expr abs($nextTSGDate - $currentCO2Date)]

            if {$nextDiff < $currentDiff} {
                set currentTSGLine $nextTSGLine
                set currentTSGDate $nextTSGDate
                set currentTSGRow $nextTSGRow

                #if {[expr $currentTSGRow % 1000] == 0} {
                    puts -nonewline "\r${GREEN}$currentCO2Row of [llength $co2Lines] [clock format $currentCO2Date -format "%Y-%m-%d %H:%M:%S"]           ${RED}$currentTSGRow of [llength $tsgLines] [clock format $currentTSGDate -format "%Y-%m-%d %H:%M:%S"]   "
                    flush stdout
                #}
            } else {
                set foundClosestTSGLine 1
            }
        } else {
            set tsgFinished 1
            set foundClosestTSGLine 1
        }
    }

    if {$currentDiff <= 30} {
        puts -nonewline $outChan "$currentCO2Line"
        foreach tsgCol $TSG_COPY_COLUMNS {
            puts -nonewline $outChan "\t[lindex $currentTSGLine $tsgCol]"
        }

        puts -nonewline $outChan "\n"
    }

    incr currentCO2Row
    #if {[expr $currentCO2Row % 100] == 0} {
        puts -nonewline "\r${RED}$currentCO2Row of [llength $co2Lines] [clock format $currentCO2Date -format "%Y-%m-%d %H:%M:%S"]           ${GREEN}$currentTSGRow of [llength $tsgLines] [clock format $currentTSGDate -format "%Y-%m-%d %H:%M:%S"]   "
        flush stdout
    #}

    if {$currentCO2Row < [llength $co2Lines]} {
        set currentCO2Line [lindex $co2Lines $currentCO2Row]
        if {[string trim $currentCO2Line] == ""} {
            set co2Finished 1
        } else {
            set currentCO2Date [clock scan "[lindex [split $currentCO2Line "\t"] 2] [lindex [split $currentCO2Line "\t"] 3]" -format "%d/%m/%y %H:%M:%S" -gmt true]
        }
    } else {
        set co2Finished 1
    }
}

close $outChan
puts ""
