import pandas as pd

# Get and store csv into data
url = 'https://raw.githubusercontent.com/dmuckatira/peptide-reader/main/peptide_list.csv'
data = pd.read_csv(url)

#What does the data look like
print(f"Loaded {data.shape[0]} peptides with {data.shape[1]} attributes\n")
#Column names
print("Attributes:", list(data.columns), "\n")
#Show a few of the peptides
print("Sample peptides:")
display(data.head())
#Show the category of peptides
print("\nPeptides by primary category:")
display(data['primary_category'].value_counts())
#How many are FDA Apporoved
print("\nFDA Approved count:")
display(data['fda_approved'].value_counts())
#How many are WADA banned
print("\nWADA Banned count:")
display(data['wada_banned'].value_counts())