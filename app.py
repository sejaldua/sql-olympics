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

sql = """
SELECT DISTINCT name, height, weight, noc, 
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
WHERE sport = '{}' AND sex = '{}'
GROUP BY 
  name, height, weight, noc
ORDER BY num_gold DESC;
"""
col1, col2 = st.beta_columns(2)
with col1:
    selected_sport = st.selectbox('Sports', pop_sports)
with col2:
    sex = st.selectbox('Sex', ['F', 'M'])
df = sqlio.read_sql_query(sql.format(selected_sport, sex), conn)
st.dataframe(df)