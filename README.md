# Time Series Analysis of US COVID-19 Data
## STA141B Final Project - UC Davis
### Fall Quarter 2021
### Professor Farris
**Contributors to this repo:** Niraj Bangari [@ndbang](https://github.com/ndbang), Marvin Pepito [@mjpepito](https://github.com/mjpepito), Sophia Tierney [@sophiatierney](https://github.com/sophiatierney)
#

# Selected categories represented by this project
- [x] 1. Project organization, writeup readability, overall conclusions
- [x] 3. Custom and efficient data processing scripts
- [x] 4. Data munging: pandas filtering, joining, grouping, transforming; handle missing values, timestamps; set indices, extract custom features
- [x] 5. Data visualization
- [x] 7. Data storage: SQLite database

# Overview
### Project Directory Structure
- [**/notebooks/**](sta141b_final/notebooks) directory contains statistical analysis, time series forecasting, and visualizations
- [**/code/**](sta141b_final/code) directory contains source code for data extraction, data cleaning, and  data manipulation
- [**/data/**](sta141b_final/data) contains the cleaned data in csv format, ready to import into a jupyter notebook, and also contains an in-memory sqlite database

All data used for this project was sourced from the COVID-19 github repository, owned by the Center for Systems Science and Engineering at Johns Hopkins University which can be found [here](https://github.com/CSSEGISandData/COVID-19).

We gathered, transformed, and merged a total of ```4``` time series datasets which are updated with new data daily. First we combined ```2``` vaccine data sources, [this one](https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/vaccine_data_us_timeline.csv) containing the number of vaccine doses, broken down into *1st_dose* and *2nd_dose*, with [this](https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/time_series_covid19_vaccine_doses_admin_US.csv) containing the daily reports of vaccines administered in wide format. Then, we combined the [confirmed cases](https://raw.githubusercontent.com/CSSEGISandData/COVID19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv) and [cumulative deaths](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv). After processing, cleaning, and transforming the ```4``` data sources, we merged them into a pandas dataframe and saved the result to a csv file and also loaded into an in memory sqlite database using sqlalchemy & sqlite. 

The range of date observations were are interested in analyzing is from 01/03/21 to date, 12/09/21.
Note that 12/17/20 is the date when vaccines began rolling out to the public in the United states, however many states did not begin reporting vaccine counts until about a month later.

When merging the cases and deaths data with vaccine data, we filled in na values with ```0``` for date observations before states began reporting vaccine administration, for easier processing and computation. 

On 11/19/21, booster shots began to be administered and reported. So note that from that date forward, the sum of the 1st dose and 2nd dose counts do not total to the total administered. We attempt to estimate the number of booster shots by summing 1st doses and 2nd doses and subtracting this from the total doses administered. 

To access the data, you can either download the csv file, or you can query the database. The columns contained in the database table are as follows:
- fips 
- state
- pop (based of 2019 Census Data)
- date 
- total_doses_state_level
- cum_deaths
- confirmed
- first_dose
- sec_dose
- est_booster_doses

An example query to the database would be:
```SELECT COUNT(*), 
   FROM covid,
   GROUP BY state,
   ORDER BY date DESC;```
to count all rows in the sql table named *covid*.
