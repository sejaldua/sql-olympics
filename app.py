import streamlit as st
import psycopg2
# from pprint import pprint
import pandas.io.sql as sqlio
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')

# Connect to an existing database
conn = psycopg2.connect("dbname=postgres user=sejaldua")

st.markdown("""
```sql
SELECT year, COUNT(*) AS num_athletes FROM olympics
WHERE season = 'Summer'
GROUP BY year
```
""")

sql = """
SELECT year, COUNT(*) AS num_athletes FROM olympics
WHERE season = 'Summer'
GROUP BY year
"""
df = sqlio.read_sql_query(sql, conn)
# df
fig = plt.figure(figsize=(18,12))
plt.bar(df['year'].astype(str), df['num_athletes'])
plt.ylabel('Summer Olympics', fontsize=18)
plt.xlabel('Number of Athletes', fontsize=18)
plt.xticks(rotation=90);
st.write(fig)

# most popular sports by number of athletes
sql = """
SELECT sport FROM olympics
GROUP BY sport
HAVING COUNT(*) > 2000
ORDER BY COUNT(*) DESC
"""
pop_sports = sqlio.read_sql_query(sql, conn)['sport']

# get all regions / countries
sql = """
SELECT DISTINCT region FROM noc_regions
"""
regions = sqlio.read_sql_query(sql, conn)['region']

sql = """
SELECT DISTINCT name, height, weight, region, 
    SUM(CASE medal
        WHEN 'Gold' THEN 1
        ELSE 0
        END) AS num_gold,
    SUM(CASE medal
        WHEN 'Silver' THEN 1
        ELSE 0
        END) AS num_silver,
    SUM(CASE medal
        WHEN 'Bronze' THEN 1
        ELSE 0
        END) AS num_bronze
FROM olympics
LEFT OUTER JOIN noc_regions
ON olympics.noc = noc_regions.noc
WHERE sport = '{}' AND sex = '{}' AND region in {}
GROUP BY 
  name, height, weight, region
ORDER BY num_gold DESC
LIMIT 200;
"""
col1, col2 = st.beta_columns(2)
with col1:
    selected_sport = st.selectbox('Sports', pop_sports)
with col2:
    sex = st.selectbox('Sex', ['F', 'M'])
regions = str(tuple(st.multiselect('Regions', regions, ['USA', 'Japan', 'China'])))
df = sqlio.read_sql_query(sql.format(selected_sport, sex, regions), conn)
st.dataframe(df)
clean_df = df[(df.height != 'NA') & (df.weight != 'NA')]
clean_df['weight'] = clean_df['weight'].astype('float')
clean_df['height'] = clean_df['height'].astype('float')
fig, ax = plt.subplots(figsize=(10, 6))
ax = sns.scatterplot(data=clean_df, x='height', y='weight', hue='region')
st.write(fig)