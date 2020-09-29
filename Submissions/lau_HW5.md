## Assignment 5: Forecast week 5 & Pandas DataFrames
**Name: Alcely Lau**

**Date: 09/27/2020**
___
## Grade
3/3 - Great job. Nice tables and nice coding!
___
#### Forecast summary
This river makes me worry about its extremely low flows.

For this week I followed the next steps:

1. Download the stream gauge observations from the USGS NWIS website, [mapper](https://maps.waterdata.usgs.gov/mapper/) and download the daily streamflow data using the following parameters:
  - Station  09506000 Verde River Near Camp Verde
  - Daily Data
  - Parameter 00060 Discharge (mean)
  - Start date = 1989-01-01
  - End date = Today
  - Select 'tab separated'


2. Explore the data using **Pandas DataFrames**. First, checking the streamflow registered in the last 3 weeks, the last 2 weeks and the last week. Then, I analyzed the mean, min, max, and percentiles (33%, 50%, 66%):
  + Using all years in the dataset, without the year 2020, for September and October.
  + Using the last 10 years, without the year 2020, for September.
  + Using the year 2019, for September and October.
  + Using the average of the previous week and the forecast week.

Finally, I decided to use for my forecast the average of the min and percentile 33% flow values of the year 2019 for the same forecast period.
____
#### Assignment questions
Using data until 9/27/2020.

1. Provide a summary of the data frames properties.
  - What are the column names?
  - What is its index?
  - What data types do each of the columns have?

  **Response:**  The following table shows the index, names and type of each column in the dataframe:

|  Index|      Name|   type|
|:-----:|:--------:|:-----:|  
|      0| agency_cd| object|  
|      1|   site_no|  int64|  
|      2|  datetime| object|
|      3|      flow|float64|
|      4|      code| object|
|      5|      year|  int32|
|      6|     month|  int32|
|      7|       day|  int32|


2. Provide a summary of the flow column including the min, mean, max, standard deviation and quartiles.

**Response:**

|       |     flow |
|:------|---------:|
| count | 11592    |
| mean  |   345.63 |
| std   |  1410.83 |
| min   |    19    |
| 25%   |    93.7  |
| 50%   |   158    |
| 75%   |   216    |
| max   | 63400    |


3. Provide the same information but on a monthly basis. (Note: you should be able to do this with one or two lines of code)

**Response:**

|   month |   ('flow', 'count') |   ('flow', 'mean') |   ('flow', 'std') |   ('flow', 'min') |   ('flow', '25%') |   ('flow', '50%') |   ('flow', '75%') |   ('flow', 'max') |
|--------:|--------------------:|-------------------:|------------------:|------------------:|------------------:|------------------:|------------------:|------------------:|
|       1 |                 992 |            706.321 |          2749.15  |             158   |           202     |            219.5  |            292    |             63400 |
|       2 |                 904 |            925.252 |          3348.82  |             136   |           201     |            244    |            631    |             61000 |
|       3 |                 992 |            941.732 |          1645.8   |              97   |           179     |            387.5  |           1060    |             30500 |
|       4 |                 960 |            301.24  |           548.141 |              64.9 |           112     |            142    |            214.5  |              4690 |
|       5 |                 992 |            105.442 |            50.775 |              46   |            77.975 |             92.95 |            118    |               546 |
|       6 |                 960 |             65.999 |            28.966 |              22.1 |            49.225 |             60.5  |             77    |               481 |
|       7 |                 992 |             95.571 |            83.512 |              19   |            53     |             70.9  |            110    |              1040 |
|       8 |                 992 |            164.354 |           274.464 |              29.6 |            76.075 |            114    |            170.25 |              5360 |
|       9 |                 956 |            172.689 |           286.776 |              36.6 |            88.075 |            120    |            171.25 |              5590 |
|      10 |                 961 |            146.169 |           111.779 |              69.9 |           107     |            125    |            153    |              1910 |
|      11 |                 930 |            205.105 |           235.674 |             117   |           156     |            175    |            199    |              4600 |
|      12 |                 961 |            337.098 |          1097.28  |             155   |           191     |            204    |            228    |             28700 |


4. Provide a table with the 5 highest and 5 lowest flow
values for  the period of record. Include the date, month and flow values in your summary.

**Response:**

The 5 highest historical flows

|      | datetime   |   month |   flow |
|-----:|:-----------|--------:|-------:|
| 1468 | 1993-01-08 |       1 |  63400 |
| 1511 | 1993-02-20 |       2 |  61000 |
| 2236 | 1995-02-15 |       2 |  45500 |
| 5886 | 2005-02-12 |       2 |  35600 |
| 2255 | 1995-03-06 |       3 |  30500 |


The 5 lowest historical flows

|      | datetime   |   month |   flow |
|-----:|:-----------|--------:|-------:|
| 8584 | 2012-07-03 |       7 |   23.4 |
| 8580 | 2012-06-29 |       6 |   22.5 |
| 8581 | 2012-06-30 |       6 |   22.1 |
| 8583 | 2012-07-02 |       7 |   20.1 |
| 8582 | 2012-07-01 |       7 |   19   |


5.  Find the highest and lowest flow  values for every month of the year (i.e. you will find 12 maxes and 12 mins) and report back what year these occurred in.

**Response:**

|   Year|     Min|   Year|       Max|
|:-----:|:------:|:-----:|:--------:|
|  2003 |  158.0 |  1993 |  63400.0 |
|  1991 |  136.0 |  1993 |  61000.0 |
|  1989 |   97.0 |  1995 |  30500.0 |
|  2018 |   64.9 |  1991 |   4690.0 |
|  2004 |   46.0 |  1992 |    546.0 |
|  2012 |   22.1 |  1992 |    481.0 |
|  2012 |   19.0 |  2006 |   1040.0 |
|  2019 |   29.6 |  1992 |   5360.0 |
|  2020 |   36.6 |  2004 |   5590.0 |
|  2012 |   69.9 |  2010 |   1910.0 |
|  2016 |  117.0 |  2004 |   4600.0 |
|  2012 |  155.0 |  2004 |  28700.0 |


6. Provide a list of historical dates with flows that are within 10% of your week 1 forecast value. If there are none than increase the %10 window until you have at least one other  value and report the date and the new window you used.

**Response:** There are a list of 611 dates with flows that are within 10% of my week 1 forecast value = 61.31. Hence, for not extending too long, in the following tables are listed the 5 first and the 5 last dates.

The 5 first dates with flows that are within 10'%' of my week 1 forecast value.

|     | datetime   |   flow |
|----:|:-----------|-------:|
| 152 | 1989-06-02 |     64 |
| 153 | 1989-06-03 |     62 |
| 160 | 1989-06-10 |     58 |
| 162 | 1989-06-12 |     57 |
| 163 | 1989-06-13 |     63 |

The 5 last dates with flows that are within 10'%' of my week 1 forecast value.

|       | datetime   |   flow |
|------:|:-----------|-------:|
| 11587 | 2020-09-22 |   60   |
| 11588 | 2020-09-23 |   64.5 |
| 11589 | 2020-09-24 |   62.2 |
| 11590 | 2020-09-25 |   58.1 |
| 11591 | 2020-09-26 |   55.7 |
