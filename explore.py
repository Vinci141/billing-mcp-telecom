import pandas as pd
df = pd.read_csv("billing.csv")
#print(df.head())

print('Columns details:',df.columns)

print('Shape:',df.shape)

df['payment_status'] = df['payment_status'].str.strip()

print(df['payment_status'].value_counts())
