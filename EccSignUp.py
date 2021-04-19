import pandas as pd
import pandasql as ps
import numpy as np
import xlsxwriter
import sys

inputFile=sys.argv[1]
outputFile=sys.argv[2]

df = pd.read_csv(inputFile)

# Remove null/garbage rows
df = df[df['First Name'].notna()]
df = df[df['Last Name'].notna()]
#Insert default values/remove nulls.
df['Number Sitting Together (besides yourself)'] = df['Number Sitting Together (besides yourself)'].fillna(0)

# Get only ECC information for shacharit and kabalast shabbat (kab)
df = ps.sqldf("SELECT * FROM  df WHERE df.Item LIKE '%ECC%' AND (df.Item LIKE '%Shacharit%' OR df.Item LIKE '%Kab%')")

# Create utiliy columns
df["Display Name"] = df["First Name"] + " " + df["Last Name"]
df["Seats"] = df['Number Sitting Together (besides yourself)'] + 1

# Remove duplicate columns
df = ps.sqldf("SELECT DISTINCT * FROM df")

# create relevant dataframes.
fridayNight = ps.sqldf("SELECT DISTINCT df.'Display Name' FROM  df WHERE df.Item LIKE '%Kab%' AND df.'Sign Up' LIKE '%Men%' ORDER BY UPPER(df.'Last Name') ASC")

saturdayMen = ps.sqldf("SELECT DISTINCT df.'Display Name' FROM  df WHERE df.Item LIKE '%Shacharit%' AND df.'Sign Up' NOT LIKE '%Women%' ORDER BY UPPER(df.'Last Name') ASC")

saturdayWomen = ps.sqldf("SELECT DISTINCT df.'Display Name' FROM  df WHERE df.Item LIKE '%Shacharit%' AND df.'Sign Up' LIKE '%Women%' ORDER BY UPPER(df.'Last Name') ASC")

MenCounts = ps.sqldf("SELECT df.Seats, count(*) AS cnt FROM df WHERE df.Item LIKE '%Shacharit%' AND df.'Sign Up' NOT LIKE '%Women%' GROUP BY df.Seats")
WomenCounts = ps.sqldf("SELECT df.Seats, count(*) as cnt FROM df WHERE df.Item LIKE '%Shacharit%' AND df.'Sign Up' LIKE '%Women%' GROUP BY df.Seats")


# Men groups with >= 4 people in the pod
BigMen = ps.sqldf("SELECT DISTINCT df.'Display Name', df.Seats FROM df WHERE df.Seats >= 4 AND df.'Sign Up' NOT LIKE 'Women'")
# Women groups with >= 4 people in the pod
BigWomen = ps.sqldf("SELECT DISTINCT df.'Display Name', df.Seats FROM df WHERE df.Seats >= 4 AND df.'Sign Up' LIKE 'Women'")

# How many pods for both men and women. Yes, I used a UNION. Shut up.
totalPods = ps.sqldf("SELECT 'Women' as 'Gender', SUM(wc.cnt) as 'Count' FROM WomenCounts AS wc UNION SELECT 'Men', SUM(mc.cnt) FROM MenCounts AS mc")

#Write to excel file. I found this code on the Internet. How it works, I don't really know. Yeah me!
writer = pd.ExcelWriter(outputFile, engine='xlsxwriter')

fridayNight.to_excel(writer, sheet_name='Friday Night')
saturdayMen.to_excel(writer, sheet_name='Saturday Men')
saturdayWomen.to_excel(writer, sheet_name='Saturday Women')
BigMen.to_excel(writer, sheet_name='Men Large Family Seating')
BigWomen.to_excel(writer, sheet_name='Women Large Family Seating')
totalPods.to_excel(writer, sheet_name='Pod Totals')
writer.close()