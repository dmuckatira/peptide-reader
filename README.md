# Peptide Reader

A bioinformatics dashboard for exploring and analyzing biotherapeutic peptides that people are actively using on themselves. Enter a peptide sequence and instantly learn what that peptide is, what it is used for, and how safe it is. If the sequence is not in the database, a machine learning model predicts its function based on patterns from known sequences.

## Build the Docker Image
```
docker build -t username/peptide-reader:1.0 .
```

## Run the Container
```
docker run --rm -v "$PWD:/data" -u "$(id -u):$(id -g)" username/peptide-reader:1.0 peptide_reader.py
```

## Data

The project uses a CSV file (`peptide_list.csv`) containing 15 of the most well-known therapeutic peptides including BPC-157, GHK-Cu, TB-500, and more. It can be loaded directly with:

```python
import pandas as pd

url = 'https://raw.githubusercontent.com/dmuckatira/peptide-reader/main/peptide_list.csv'
data = pd.read_csv(url)
data['tags'] = data['tags'].str.split('|')
```

### Columns

Column: Description 
`name` : Common name of the peptide 
`aliases` : Other names the peptide is known by 
`sequence` : Amino acid sequence in single-letter code 
`sequence_type` : `standard`, `modified`, or `fragment` 
`sequence_notes` : Notes on any modifications or limitations for sequence matching 
`length` : Number of amino acids 
`molecular_weight_da` : Molecular weight in Daltons 
`origin` : Where the peptide naturally comes from 
`admin_route` : How it is typically administered 
`primary_category` : Main therapeutic category 
`tags` : Pipe-separated bioactivity tags (e.g. `wound_healing\|anti_inflammatory`) 
`fda_approved` : Whether the peptide is FDA approved (`yes`/`no`) 
`wada_banned` : Whether the peptide is banned by WADA (`yes`/`no`) 
`biohacker_popularity` | Relative popularity in the biohacking community 
`pubchem_cid` : PubChem compound ID if available 
`sources` : Literature and database sources 

## Repository Contents

File : Description 

`peptide_reader.py` : Python script that loads the CSV and transforms it into a pandas DataFrame 
`peptide_list.csv` : Curated dataset of 15 biotherapeutic peptides 
`Dockerfile` : Recipe for containerizing the project 


## AI Usage

I used Claude to help me make the csv file and format the README.