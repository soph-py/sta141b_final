# Time Series Analysis of COVID-19 Data
## STA141B Final Project - UC Davis
### Fall Quarter 2021
### Professor Farris
**Contributors to this repo:** Niraj Bangari, Marvin Pepito, Sophia Tierney
#
# Overview
### Project Directory Structure
- **/notebooks/** directory contains statistical analysis, time series forecasting, and visualizations
- **/code/** directory contains source code for data extraction, data cleaning, and  data manipulation
- **/data/** contains the cleaned data in csv format, ready to import into a jupyter notebook, and also contains an in-memory sqlite database

All data used for this project was sourced from the COVID-19 github repository, owned by the Center for Systems Science and Engineering at Johns Hopkins University which can be found [here](https://github.com/CSSEGISandData/COVID-19).
The range of date observations were from '' to ''
Note that after the date of '' is when vaccine data was introduced, even though vaccines began being administered on '', many states had about a month of delay in reporting the data 

When merging the cases and deaths data with vaccine data, we filled in na values before the date vax data began being reported for most states with 0 for easier processing and computation. 

After '', booster shots began to be administered and reported, so from that date on, the sum of the 1st dose and 2nd dose does not total to the total administered. We attempt to estimate the number of booster shots by summing 1st doses and 2nd doses and subtracting this from the total doses administered. 

All data was sourced from - link JHU github repo
Extracted, transformed, cleaned with pandas, loaded into an in memory sqlite database using sqlalchemy & pandas.
All visualizations and modeling were done by extracting the data from the sqlite table named 'covid' 

All code used for data extraction, transformation, and cleaning can be located in the /code/ dir
In the /notebooks/ dir you can find code used to query the database

To access the data, you can either download the csv file, or you can query the database. The columns contained in the database table are as follows:
- ''
- ''

fips, state, pop_2019, date total_doses_state_level, cum_deaths, confirmed, 1st_dose, 2nd_dose, est_booster_doses

An example query would be :
```count (*) from covid```
to count all rows in the sql table