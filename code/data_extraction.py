import pandas as pd
import sqlalchemy as sqla
import numpy as np

urls = {
    'us_deaths': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv', 
    'us_confirmed': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv', 
    'vaccine': [
        'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/vaccine_data_us_timeline.csv',
        'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/people_vaccinated_us_timeline.csv', 
        'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/archive/vaccine_data_us_state_timeline.csv',
        'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/time_series_covid19_vaccine_doses_admin_US.csv'
    ], 
    'population': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv'
    }

df_vaxed = pd.read_csv(
    urls['vaccine'][0], parse_dates = ['Date'], usecols = [0, 1, 2, 3, 9, 10, 11]
)
df_vaxed.columns = ['state', 'date', 'type', 'fips', 'doses_admin_total', '1st_dose', '2nd_dose']
df_vaxed.head()
df_vaxed.info()
len(df_vaxed) # 120640

df_wide_format = pd.read_csv(urls['vaccine'][3])
df_wide_format.head()
df_ts_vaxed = df_wide_format.drop(columns = [
        'UID', 'iso2', 'iso3', 'code3', 'Admin2', 'Country_Region', 'Lat', 'Long_', 'Combined_Key'
    ], axis = 1)

df_ts_vaxed = df_ts_vaxed.melt(id_vars = ['FIPS', 'Province_State', 'Population'], var_name = 'date', value_name = 'total_doses_state_level')
df_ts_vaxed.columns = ['fips', 'state', 'pop_2019', 'date', 'total_doses_state_level']
df_ts_vaxed.date = pd.to_datetime(df_ts_vaxed.date)
df_ts_vaxed.head()
df_ts_vaxed[~df_ts_vaxed.fips.isna()]

regions_to_drop = [
    'America Samoa', 'American Samoa', 'Guam', 'Northern Mariana Islands', 'Puerto Rico', 
    'Virgin Islands', 'Department of Defense', 'Federal Bureau of Prisons', 
    'Indian Health Services', 'Long Term Care (LTC) Program', 'Veterans Health Administration'
    ]
df_ts_vaxed = df_ts_vaxed[~df_ts_vaxed['state'].isin(regions_to_drop)].copy()
df_ts_vaxed.info()
df_ts_vaxed.date.nunique() * df_ts_vaxed.state.nunique() #  360 unique dates * 51 unique states = 18360 number of rows 
len(df_ts_vaxed)


def parse_covid_data(data: str, colname: str):
    df = pd.read_csv(data)
    df = df.drop(columns = [
        'UID', 'iso2', 'iso3', 'code3', 'Admin2', 'Country_Region', 'Lat', 'Long_', 'Combined_Key'
    ], axis = 1)
    if 'Population' in df.columns:
        df = df.melt(id_vars = ['FIPS', 'Province_State', 'Population'], var_name = 'date', value_name = colname) #, 'Population'
        df = df.drop(columns = ['Population'], axis = 1)
        df.columns = ['fips', 'state', 'date', colname]
    else:
        df = df.melt(id_vars = ['FIPS', 'Province_State'], var_name = 'date', value_name = colname)
        df.columns = ['fips', 'state', 'date', colname]
    df.date = pd.to_datetime(df.date)
    return df

df_deaths = parse_covid_data(urls['us_deaths'], 'cum_deaths')
df_deaths.dropna(axis = 0, inplace = True)
df_deaths = df_deaths.reset_index(drop = True)

df_confirmed= parse_covid_data(urls['us_confirmed'], 'confirmed')
df_confirmed.dropna(axis = 0, inplace=True)
df_confirmed = df_confirmed.reset_index(drop = True)

df = df_deaths.merge(df_confirmed, on = ['date', 'state', 'fips'], how = 'outer')
df.info()
df.head()
df[df.isna().any(axis = 1)] # no NA's


regions_to_drop = [
    'America Samoa', 'American Samoa', 'Guam', 'Northern Mariana Islands', 'Puerto Rico', 
    'Virgin Islands', 'Department of Defense', 'Federal Bureau of Prisons', 
    'Indian Health Services', 'Long Term Care (LTC) Program', 'Veterans Health Administration'
    ]
df_states = df[~df['state'].isin(regions_to_drop)].copy()
df_states.state.nunique()

df = df.set_index(['date'])
cum_totals_to_date = df.groupby(['state'])[['cum_deaths', 'confirmed']].sum()

doses = df_vaxed.groupby(['date', 'state', 'type'])[['1st_dose', '2nd_dose']].aggregate(sum)
doses = doses.reset_index()
mask = doses[doses.type == 'All'].index
dose_sum = doses.drop(mask)
dose_sum = dose_sum.groupby(['date', 'state'])[['1st_dose', '2nd_dose']].aggregate(sum)
dose_sum = dose_sum.reset_index()


state_daily_totals = df_states.groupby(['date', 'state'])[['cum_deaths', 'confirmed']].aggregate(sum) # cumulative totals
state_daily_totals = state_daily_totals.reset_index()

df_covid_data = df_ts_vaxed.merge(state_daily_totals, on = ['date', 'state'], how = 'outer')

mask = ((df_covid_data['state'] == 'Grand Princess') or (df_covid_data['state'] == 'Diamond Princess'))
region_names = df_covid_data[~(df_covid_data['state'] != 'Grand Princess') & (df_covid_data['state'] != 'Diamond Princess')].index

region_names = df_covid_data[mask].index
df_covid_data.drop(region_names)

df_covid_data = df_covid_data[df_covid_data.state != 'Diamond Princess']
df_covid_data = df_covid_data[df_covid_data.state != 'Grand Princess']

region_index_drop = (df_covid_data[df_covid_data['state'] == 'Diamond Princess'].index, df_covid_data[df_covid_data['state'] == 'Grand Princess'].index)
df_covid_data = df_covid_data.drop(region_index_drop[0])
df_covid_data = df_covid_data.drop(region_index_drop[1])
df_covid_data = df_covid_data[df_covid_data.total_doses_state_level.notna()].reset_index(drop = True).copy()

complete_data = df_covid_data.merge(dose_sum, on = ['date', 'state'], how = 'outer')
complete_data = complete_data[complete_data.fips.notna()]
complete_data.state.nunique()

complete_data['est_booster_doses'] = 0

mask = complete_data[complete_data.date > '2021-09-20'].index

subset_df = complete_data[complete_data.date > '2021-09-20']
est_boosters = subset_df['total_doses_state_level'] - (subset_df['1st_dose'] + subset_df['2nd_dose'])

complete_data.loc[mask, 'est_booster_doses'] = est_boosters

complete_data.to_csv('complete_covid_data.csv', index = False)

len(complete_data)