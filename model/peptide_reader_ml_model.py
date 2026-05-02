#!/usr/bin/env python3

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import argparse
import logging
import socket
import pickle
import sys


parser = argparse.ArgumentParser(
    description="Train peptide primary category classifier"
)

parser.add_argument(
    '-l', '--loglevel',
    required=False,
    default='WARNING',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help='Set log level'
)

parser.add_argument(
    '-d', '--data',
    required=False,
    default='peptide_list_expanded.csv',
    help='Path to peptide CSV file'
)

args = parser.parse_args()

format_str = (
    f'[%(asctime)s {socket.gethostname()}] '
    '%(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
)

logging.basicConfig(level=args.loglevel, format=format_str)


def amino_acid_features(sequence_data):
    """
    Convert peptide sequences into amino acid count features.

    Args:
        sequence_data: Peptide sequence data

    Returns:
        DataFrame of amino acid count features
    """
    #Defind all 20 amino acids
    amino_acids = list("ACDEFGHIKLMNPQRSTVWY")
    features = pd.DataFrame()

    #Compute length of sequence
    features["length"] = sequence_data.str.len()

    #Count how many of each amino acid there is
    for acid in amino_acids:
        features[acid + "_count"] = sequence_data.str.count(acid)

    return features


def train_model(data_file: str) -> None:
    """
    Train peptide classifier, evaluate it, and save it to disk.

    Args:
        data_file: Path to peptide CSV file

    Returns:
        None
    """
    logging.info("Loading peptide dataset")

    df = pd.read_csv(data_file)
    #Set X as numerical sequence and y as primary category predictor
    X = amino_acid_features(df["sequence"].astype(str))
    y = df["primary_category"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=123
    )

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', SGDClassifier(loss="perceptron", alpha=0.01, random_state=1))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    print("Peptide Primary Category Model Results")
    print(f'accuracy = {accuracy_score(y_test, y_pred)}')
    print(classification_report(y_test, y_pred, digits=4))

    logging.info("Saving model to peptide_category_pipeline.pkl")

    with open('peptide_category_pipeline.pkl', 'wb') as f:
        pickle.dump(pipeline, f)


def main() -> None:
    logging.info("Starting training workflow")

    try:
        train_model(args.data)

    except FileNotFoundError:
        logging.error("Dataset file not found. Exiting.")
        sys.exit(1)

    logging.info("Training workflow complete")


if __name__ == '__main__':
    main()