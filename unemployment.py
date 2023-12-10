import pandas as pd

# Read the original data from the CSV file
file_path = r"C:\Users\moham\Downloads\df_sex_unemployment_rates.csv"
nojob = pd.read_csv(file_path)

# Display basic information about the original DataFrame
nojob.info()

# Display the count of null values in each column
null_values = nojob.isnull().sum()
print("Null values in each column")
print(null_values)

# Identify and display rows with null values and the corresponding columns
null_rows = nojob.loc[nojob.isnull().any(axis=1)]
print("Dates with null values")
print(null_rows[['date'] + list(null_rows.columns[null_rows.isnull().any()])])

# Select a subset of columns to keep in the DataFrame
cols_to_keep = ['date', 'men_20_24_rate', 'women_20_24_rate', 'men_25plus_rate', 'women_25plus_rate',
                'men_25_34_rate', 'women_25_34_rate', 'men_35_44_rate', 'women_35_44_rate',
                'men_45_54_rate', 'women_45_54_rate', 'men_55plus_rate', 'women_55plus_rate']
nojob = nojob[cols_to_keep]

# Calculate new columns for overall rates based on selected columns
nojob['20_plus_overall_rate'] = nojob[['men_20_24_rate', 'women_20_24_rate', 'men_25plus_rate', 'women_25plus_rate',
                                        'men_25_34_rate', 'women_25_34_rate', 'men_35_44_rate', 'women_35_44_rate',
                                        'men_45_54_rate', 'women_45_54_rate', 'men_55plus_rate', 'women_55plus_rate']].mean(axis=1, skipna=True)

nojob['20_plus_men_rate'] = nojob[['men_20_24_rate', 'men_25plus_rate', 'men_25_34_rate', 'men_35_44_rate',
                                    'men_45_54_rate', 'men_55plus_rate']].mean(axis=1, skipna=True)

nojob['20_plus_women_rate'] = nojob[['women_20_24_rate', 'women_25plus_rate', 'women_25_34_rate',
                                      'women_35_44_rate', 'women_45_54_rate', 'women_55plus_rate']].mean(axis=1, skipna=True)

# Melt the DataFrame to convert from wide to long format
melted_df = pd.melt(nojob, id_vars=['date'], value_vars=['men_20_24_rate', 'women_20_24_rate',
                                                        'men_25_34_rate', 'women_25_34_rate',
                                                        'men_35_44_rate', 'women_35_44_rate',
                                                        'men_45_54_rate', 'women_45_54_rate',
                                                        'men_55plus_rate', 'women_55plus_rate'],
                   var_name='variable', value_name='value')

# Extract gender and age range information from the variable column
melted_df['Gender'] = melted_df['variable'].apply(lambda x: 'Women' if 'women' in x.lower() else 'Men')
melted_df['AgeRange'] = melted_df['variable'].apply(lambda x: f"{x.split('_')[1]}-{x.split('_')[2]}")

# Display detailed information about the melted DataFrame
print("Melted DataFrame Information:")
print(melted_df.info())

# Display the first 20 rows of the melted DataFrame
print("First 20 rows of the melted DataFrame:")
print(melted_df.head(20))



# Save the final melted DataFrame to a new CSV file
melted_df.to_csv('formatted_unemployment_data.csv', index=False)
