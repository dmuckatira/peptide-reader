# Peptide Sequence Reader

## Overview

This project builds and deploys an interactive web dashboard that allows users to search known peptide sequences and predict the primary biological category of new peptide sequences using a machine learning model.

The motivation behind this project stems from a growing trend of individuals self-administering therapeutic peptides without fully understanding what they are or what they do. This tool was built to bring awareness to that trend by making peptide information more accessible. Users can input a peptide sequence and if it exists in the database, the application will return key details about it like its category and FDA status. If the sequence is not found, a trained machine learning model will predict its most likely biological function, giving users a starting point for understanding an unknown peptide.

---

## Deploying the Application

### Prerequisites

- Docker installed on your machine
- Python 3.12.3 or Python 3 (for training the model locally)

### Steps

#### 1. Install dependencies (local)

```bash
pip install -r requirements.txt
```

#### 2. Train the model

```bash
python3 peptide_reader_ml_model.py
```

#### 3. Run the dashboard with Docker

```bash
make compose
```

OR

```bash
docker compose up --build -d
```

#### 4. Open the application in your browser

```
<YOUR-IP>:8050
```

Example:

```
135.112.37.13:8050
```

---

## Using the Web App

1. Open the dashboard in your browser using the URL above
2. Browse the peptide table to explore the dataset
3. Type a peptide sequence into the input box at the bottom and press **Submit**

**If the sequence is found in the database:**

The app will return the peptide name, its biological category, and FDA approval status.

Example:
```
Your peptide is: "BPC-157". It is used for: "Tissue Repair / Recovery". FDA approved: "no".
```

**If the sequence is not found:**

The app will use a trained machine learning model to predict the most likely biological function of the peptide.

Example:
```
Peptide sequence not found. This sequence is most likely used for: "Oncology".
```

## Project Structure

- `app.py` : Main Dash web application that runs the dashboard, handles user input, searches the dataset, and calls the ML model for predictions
- `requirements.txt` : Python dependencies needed to run the app (dash, pandas, scikit-learn, plotly, dash-bootstrap-components)
- `Dockerfile` : Builds the application image using Python 3.12
- `docker-compose.yml` : Runs the dashboard service and maps it to port 8050
- `Makerfile` : Automates restarting the Docker app by shutting down existing containers and rebuilding and relaunching them in one command.
- `model/` : 
    - `peptide_reader_ml_model.py` : Trains and saves a ML model to predict peptide category based on sequence data
    - `peptide_category_pipeline.pkl` : Contains the trained ML pipeline
    - `peptide_list_expanded.csv` : Contains the peptide dataset 
- `README.md` : Project documentation including overview, deployment steps, and usage instructions

## AI Usage

Claude was used to help build and expand the peptide dataset (`peptide_list_expanded.csv`) used in this project.

**Dataset Sources:**

- Peptipedia: https://app.peptipedia.cl/download
- Dopamine Club Peptide Database: https://dopamine.club/database?category=Peptide

ChatGPT was used to:
- Help debug Python and Docker issues
- Format and make the README aesthetic

