FROM python:3.12

RUN pip3 install pandas

COPY peptide_reader.py /code/peptide_reader.py
COPY peptide_list.csv /code/peptide_list.csv

ENV PATH="/code:$PATH"
