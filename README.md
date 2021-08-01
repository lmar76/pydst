# pydst #

## Overview ##

`pydst` is a Python module containing tools to read Dst index files.

## Installation ##

To install the module:

```
$ cd INSTALLDIR
$ pip install ARCHIVE
```

## Dst index file format description ##

Each record has a fixed length of 120 bytes and it is composed by the following [columns][1]:

 Column  | Format | Short description
---------|--------|-------------------
 1-3     | A3     | Index name 'DST'  
 4-5     | I2     | The last two digits of the year
 6-7     | I2     | Month
 8       | A1     | '*' for index
 9-10    | I2     | Date
 11-12   | A2     | All spaces or may be "RR" for quick look
 13      | A1     | 'X' (for index)
 14      | A1     | Version (0: quicklook, 1: provisional, 2: final, 3 and up: corrected final or may be space)
 15-16   | I2     | Top two digits of the year (19 or space for 19XX, 20 from 2000)
 17-20   | I4     | Base value, unit 100 nT
 21-116  | 24I4	  | 24 hourly values, 4 digit number, unit 1 nT, value 9999 for the missing data. First data is
                    for the first hour of the day, and Last data is for the last hour of the day.
 117-120 | I4     | Daily mean value, unit 1 nT. Value 9999 for the missing data.

[1]: http://wdc.kugi.kyoto-u.ac.jp/dstae/format/dstformat.html