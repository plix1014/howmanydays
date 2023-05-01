# howmanydays

shows number of years, months, days, hours, workingdays until a given target date

## Prerequisites

* sudo apt-get install python3-dateutil
* sudo apt-get install python3-pandas
* sudo pip3 install holidays


Die Moduleabhängigkeiten werden mit dem requirements.txt installiert
* Modul 'python3-dateutil'
* Modul 'python3-pandas'
* Modul 'holidays'

## Installation


## Usage
```
$ ./howmanydays.py 

usage: ./howmanydays.py -e yyyy-mm-dd [-s yyyy-mm-dd] [-v n] [-m n]
		-e|--enddate yyyy-mm-dd 	.... End date
		-s|--startdate yyyy-mm-dd 	.... Start date
		-v|--vacationdays n 		.... number of vacation days
		-m|--displaymode n  		.... displaymode [1|2]

	./howmanydays.py -e 2030-11-01
	./howmanydays.py -e 2030-11-01 -v 30
	./howmanydays.py -e 2030-11-01 -s 2022-09-30 -v 30
	./howmanydays.py -e 2030-11-01 -s 2022-09-30 -v 30 -m 2
```



```sh
$ ./howmanydays.py -e 2025-08-15

=================================================
Starttag           : 2022-09-30 00:00:00
Zieltag            : 2025-08-15 00:00:00
Dauer              : relativedelta(years=+2, months=+10, days=+16)

gesamt Monate      :        34
gesamt Wochen      :       150
gesamt Tage        :     1.050
gesamt Stunden     :    25.200
gesamt Minuten     : 1.512.000

Urlaubstage p/a    :        25
gesamt Urlaubst.   :        73
Werktage(MO-FR)    :       750
Arbeitstage        :       717
------------------------------
netto Arbeitstage  :       644
------------------------------
```


Zweite Variante der Ausgabe
```sh
./howmanydays.py -e 2025-08-15 -s 2022-09-30 -m 2

=================================================
Starttag: Freitag, 30. September 2022, 00:00:00
Zieltag : Freitag, 15. August 2025, 00:00:00
Ergebnis: 1050 Tage, 0 Stunden, 0 Minuten und 0 Sekunden

Oder 2 Jahre, 10 Monate, 16 Tage, 0 Stunden
Oder 34 Monate, 16 Tage, 0 Stunden
Oder 150 Wochen, 0 Tage

1050 Tage, 0 Stunden, 0 Minuten und 0 Sekunden sind:
   90.720.000 Sekunden
    1.512.000 Minuten
       25.200 Stunden

1050 Tage bis Ende, sind:
    750 Werktage(MO-FR)
 -  300 Wochenenden(SA-SO)
 -   33 Feiertage
 =  717 Arbeitstage
 -   73 Urlaubstage (25 p/a)
------------------------------
    644 netto Arbeitstage
------------------------------
```

## Author

* **plix1014** - [plix1014](https://github.com/plix1014)


## License

This project is licensed under the Attribution-NonCommercial-ShareAlike 4.0 International License - see the [LICENSE.md](LICENSE.md) file for details


