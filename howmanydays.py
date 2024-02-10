#!/usr/bin/python3
# -*- coding: utf-8 -*-

# https://github.com/dr-prodigy/python-holidays/blob/master/holidays/countries/austria.py
# https://stackoverflow.com/questions/2224742/most-recent-previous-business-day-in-python

# https://www.timeanddate.com/date/workdays.html?d1=14&m1=8&y1=2022&d2=1&m2=11&y2=2030

    # From: Sonntag, 14. August 2022, 11:00:00
    # To: Freitag, 1. November 2030, 00:00:00
    # Result: 3000 days, 13 hours, 0 minutes and 0 seconds
    # The duration is 3000 days, 13 hours, 0 minutes and 0 seconds
    # Or 8 years, 2 months, 17 days, 13 hours
    # Or 98 months, 17 days, 13 hours

    # Alternative time units
    # 3000 days, 13 hours, 0 minutes and 0 seconds can be converted to one of these units:
    # 259 246 800 seconds
    # 4 320 780 minutes
    # 72 013 hours
    # 3000 days (rounded down)
    # 428 weeks (rounded down)

    # Result: 2050 days
    # 3001 calendar days – 951 days skipped:
    # Excluded 428 Saturdays
    # Excluded 429 Sundays
    # Excluded 94 holidays:

    # October 2022–December 2022: 60 days included
    # Year 2023: 247 days included
    # Year 2024: 252 days included
    # Year 2025: 249 days included
    # Year 2026: 250 days included
    # Year 2027: 251 days included
    # Year 2028: 248 days included
    # Year 2029: 249 days included
    # January 2030–September 2030: 188 days included

#
# pli, 14.08.2022, initial prog
# pli, 01.05.2023, calculation of vacation days, incl. aliquote nb of days for broken years
#---------------------------------------------------------

# install dependencies
# sudo apt-get install python3-dateutil
# sudo apt-get install python3-pandas
# sudo pip3 install holidays

import sys
import getopt
import locale
from time import strftime, localtime
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse

import pandas as pd
import numpy as np
import holidays
import math


# format day string
date_fmt  = '%Y-%m-%d %H:%M:%S'
date_fmt2 = '%A, %d. %B %Y, %H:%M:%S'

# default Urlaubstage
URLAUBS_TAGE = 25

# default Krankenstand
KRANK_TAGE = 5

# geplanter Pensionsantritt
RETIRE_DATE  = '2030-11-01 00:00:00'

# HL->Wien->HL
KM_PER_DAY    = 110
# price per week
FUEL_PER_WEEK = 50

# de_AT.ISO8859-1
locale.setlocale(locale.LC_ALL, "")

# only for debugging
DEBUG = False

#--------------------------------------------------------------------------------

def yordinal(year, month, day):
    return ((year-1)*365 + (year-1)//4 - (year-1)//100 + (year-1)//400
         + [ 0,31,59,90,120,151,181,212,243,273,304,334][month - 1]
         + day
         + int(((year%4==0 and year%100!=0) or year%400==0) and month > 2))


def ydaysBetweenDates(date1,date2):
    y1 = date1.year
    m1 = date1.month
    d1 = date1.day

    y2 = date2.year
    m2 = date2.month
    d2 = date2.day

    x = date.toordinal(date1)
    y = date.toordinal(date2)

    return int(y-x)


def calc_dates(date_now, rt_date, vac_days, sick_days, mode=1, costs=False):

    # start date
    dts      = datetime.strptime(date_now, date_fmt)
    # end date
    dte      = datetime.strptime(rt_date, date_fmt)
    dtdiff   = dte - dts

    # netto dauer
    reldiff  = relativedelta(dte,dts)
    years    = reldiff.years
    months   = reldiff.months
    days     = reldiff.days
    hours    = reldiff.hours
    minutes  = reldiff.minutes
    seconds  = reldiff.seconds

    # dauer in unterschiedlichen Groeßen
    # dtdiff.days
    g_months   = years * 12 + months
    #g_days     = ydaysBetweenDates(dts,dte)
    g_days     = dtdiff.days
    g_hours    = g_days * 24 + hours
    g_minutes  = g_hours * 60 + minutes
    g_seconds  = g_minutes * 60 + seconds


    # Arbeitstage
    #-----------------------------------------------------------
    date1 = pd.to_datetime(dts,format=date_fmt).date()
    date2 = pd.to_datetime(dte,format=date_fmt).date()

    # get austrian holidays
    at_holidays = []
    at_vac      = holidays.AT()

    # iterate over range, build holiday list
    for dt in rrule(DAILY, dtstart=dts, until=dte):
        if dt in at_vac:
            at_holidays.append(dt.strftime("%Y-%m-%d"))


    # workdays MO-FR
    bdays        = np.busday_count( date1 , date2)
    # exclude holidays
    bdays_no_vac = np.busday_count( date1 , date2, holidays = at_holidays)


    # calc vacation days
    # start till end of year
    dts_ye   = datetime.strptime(str(dts.year)+'-12-31 00:00:00', date_fmt)
    # start of last year till end
    dte_yb   = datetime.strptime(str(dte.year)+'-01-01 00:00:00', date_fmt)

    # calc diffs
    dt_first = dts_ye - dts
    dt_last  = dte    - dte_yb

    # aliquote vac days for first and last year
    vac_part1 = math.ceil(vac_days/365*dt_first.days)
    vac_part2 = math.ceil(vac_days/365*dt_last.days)

    # aliquote sick leave days for first and last year
    sick_part1 = math.ceil(sick_days/365*dt_first.days)
    sick_part2 = math.ceil(sick_days/365*dt_last.days)

    # nb of years for the rest of the timespan
    mid_diff  = relativedelta(dte_yb,dts_ye)
    mid_years = mid_diff.years

    # sum up vacation days
    nb_vac_days =  int(vac_part1 + vac_part2 + mid_years*vac_days)

    # sum up sick leave days
    nb_sick_days =  int(sick_part1 + sick_part2 + mid_years*sick_days)

    # estimation of number of vacation days
    #nb_vac_days =  int(vac_days * (years + months/12))

    # estimation
    nb_netto_days = int(bdays_no_vac)-int(nb_vac_days)-int(nb_sick_days)
    nb_km         = nb_netto_days * KM_PER_DAY
    fuel_costs    = nb_netto_days/5*FUEL_PER_WEEK


    #-----------------------------------------------------------
    # print result

    # quick and dirty_ without locales
    gf_months     = "{:,}".format(g_months).replace(',', '.')
    gf_weeks      = "{:,}".format(g_days // 7).replace(',', '.')
    gf_week_days  = "{:,}".format(g_days % 7).replace(',', '.')
    gf_days       = "{:,}".format(g_days).replace(',', '.')
    gf_hours      = "{:,}".format(g_hours).replace(',', '.')
    gf_minutes    = "{:,}".format(g_minutes).replace(',', '.')
    gf_seconds    = "{:,}".format(g_seconds).replace(',', '.')

    gf_nb_km      = "{:,}".format(nb_km).replace(',', '.')
    gf_fuel_costs = "{:_}".format(fuel_costs).replace('.', ',').replace('_','.')


    print("=================================================")
    if mode == 1:
        # mode 1 = table
        print("Starttag           : %s" % dts)
        print("Zieltag            : %s" % dte)
        print("Dauer              : %s" % reldiff)
        #print("Dauer in Tagen     : %7s" % dtdiff.days)

        if DEBUG:
            print("years              : %s" % years)
            print("months             : %s" % months)
            print("days               : %s" % days)
            print("hours              : %s" % hours)

        print()
        print("gesamt Monate      : %9s" % gf_months)
        print("gesamt Wochen      : %9s" % gf_weeks)
        print("gesamt Tage        : %9s" % gf_days)
        print("gesamt Stunden     : %9s" % gf_hours)
        print("gesamt Minuten     : %9s" % gf_minutes)

        if costs:
            print("\ngesamt km          : %9s" % (gf_nb_km))
            print("gesamt Benzinkosten: %11s" % (gf_fuel_costs))

        print()
        print("Urlaubstage p/a    : %9s" % vac_days)
        print("gesamt Urlaubst.   : %9s" % nb_vac_days)
        print("gesch. Krankenst.  : %9s" % nb_sick_days)
        print("Werktage(MO-FR)    : %9s" % bdays)
        print("Arbeitstage        : %9s" % bdays_no_vac)
        print("------------------------------")
        print("netto Arbeitstage  : %9s" % int(nb_netto_days))
        print("------------------------------")

    if mode == 2:
        # mode 2 = similar to www.timeanddate.com
        print("Starttag: %s" % dts.strftime(date_fmt2))
        print("Zieltag : %s" % dte.strftime(date_fmt2))
        print("Ergebnis: %s Tage, %s Stunden, %s Minuten und %s Sekunden\n" % (dtdiff.days, hours, minutes, seconds))

        print("Oder %s Jahre, %s Monate, %s Tage, %s Stunden" % (years, months, days, hours))
        print("Oder %s Monate, %s Tage, %s Stunden" % (g_months, days, hours))
        print("Oder %s Wochen, %s Tage\n" % (gf_weeks, gf_week_days))

        print("%s Tage, %s Stunden, %s Minuten und %s Sekunden sind:" % (dtdiff.days, hours, minutes, seconds))
        print(" %12s Sekunden" % (gf_seconds))
        print(" %12s Minuten" % (gf_minutes))
        print(" %12s Stunden" % (gf_hours))

        print()
        saso = dtdiff.days-bdays
        nwda = dtdiff.days-bdays_no_vac
        fday = nwda-saso

        print("%s Tage bis Ende, sind:" % (dtdiff.days))
        print("   %4s Werktage(MO-FR)" % bdays)
        print(" - %4s Wochenenden(SA-SO)" % saso)
        print(" - %4s Feiertage" % fday)
        print(" = %4s Arbeitstage" % bdays_no_vac)
        print(" - %4s Urlaubstage (%s p/a)" % (nb_vac_days, vac_days))
        print(" - %4s Krankenstandstage (gesch.) (%s p/a)" % (nb_sick_days, sick_days))
        print("------------------------------")
        print("   %4s netto Arbeitstage" % int(nb_netto_days))
        print("------------------------------")
        if costs:
            print("\n-- KOSTEN ---------------------------")
            print("%7s km bis Ende" % (gf_nb_km))
            print("%9s € voraussicht. Benzinkosten" % (gf_fuel_costs))
            print("-------------------------------------")


    #print("\n=================================================")
    print()



def usage():
    msg  = "\nusage: " + __file__ + " -e yyyy-mm-dd [-s yyyy-mm-dd] [-v n] [-m n] [ -c ]\n"
    msg += "\t\t-e|--enddate yyyy-mm-dd \t.... End date\n"
    msg += "\t\t-s|--startdate yyyy-mm-dd \t.... Start date\n"
    msg += "\t\t-v|--vacationdays n \t\t.... number of vacation days\n"
    msg += "\t\t-m|--displaymode n  \t\t.... displaymode [1|2]\n"
    msg += "\t\t-m|--costs  \t\t\t.... show costs\n\n"
    msg += "\t" + __file__ + " -e "+RETIRE_DATE[:-9]+"\n"
    msg += "\t" + __file__ + " -e "+RETIRE_DATE[:-9]+" -v 30\n"
    msg += "\t" + __file__ + " -e "+RETIRE_DATE[:-9]+" -s "+sdate[:-9]+" -v 30\n"
    msg += "\t" + __file__ + " -e "+RETIRE_DATE[:-9]+" -s "+sdate[:-9]+" -v 30 -m 2\n\n"

    print(msg)
    sys.exit(1)


#----------------------------------------------------------------------
#
#----------------------------------------------------------------------
if __name__ == "__main__":

    # init 
    p_sdate = ''
    p_edate = ''
    p_vdays = 0
    p_mode = 1
    p_costs = False

    # use current day as start unless -s is used
    sdate   = strftime(date_fmt, localtime())

    # check for options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:e:v:m:c", ["help", "startdate", "enddate", "vacationdays", "displaymode", "costs"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(("%s" % str(err))) # will print something like "option -a not recognized"
        usage()

    for o, a in opts:
        if o in ("-s", "--startdate"):
            p_sdate = a

        elif o in ("-e", "--endate"):
            p_edate = a

        elif o in ("-v", "--vacationdays"):
            p_vdays = a

        elif o in ("-m", "--displaymode"):
            p_mode = int(a)

        elif o in ("-c", "--costs"):
            p_costs = True

        elif o in ("-h", "--help"):
            usage()
        else:
            assert False, "unhandled option"


    if p_sdate != '':
        try:
            if parse(str(p_sdate)):
                sdate = p_sdate + ' 00:00:00'
        except:
            print("\nWARN: invalid start-date given\n")
            usage()


    if p_edate != '':
        try:
            if parse(str(p_edate)):
                RETIRE_DATE = p_edate + ' 00:00:00'
        except:
            print("\nWARN: invalid end-date given\n")
            usage()
    else:
        usage()


    if p_vdays != 0:
        if p_vdays.isdigit():
            URLAUBS_TAGE = int(p_vdays)
        else:
            print("\nWARN: invalid number of vacaction days given\n")
            usage()

    if p_mode < 1:
        p_mode = 1

    if p_mode > 2:
        p_mode = 2


    print()
    calc_dates(sdate, RETIRE_DATE, URLAUBS_TAGE, KRANK_TAGE, p_mode, p_costs)


