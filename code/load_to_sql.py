import pandas as pd
import sqlalchemy as sqla

# /Users/sofaloaf/Desktop/fall_quarter_2021/STA141B/final_project/
covid_reader = pd.read_csv('data/complete_covid_data.csv', chunksize = 1000, low_memory = False)
covid_chunk = next(covid_reader)
covid_cols = covid_chunk.columns
covid_chunk.info()
covid_chunk.head()

# /Users/sofaloaf/Desktop/fall_quarter_2021/STA141B/final_project/
sqlite_file = 'data/complete_covid_data.sqlite'
covid_conn = sqla.create_engine('sqlite:///' + sqlite_file)

## create a table in the empty sqlite db we initiated
covid_chunk.to_sql('covid', covid_conn, if_exists = 'replace')
for covid_chunk in covid_reader:
    covid_chunk.to_sql('covid', covid_conn, if_exists = 'append') # append 1000 rows for each iteration to our existing covid table 

covid_cols