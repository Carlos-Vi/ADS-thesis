# Filling in evidence tables with GPT-4o

This repository contains the data and code used for my master's thesis in Applied Data Science.

## Data
The "Data" folder contains the human curated evidence tables in Word format, divided into training and test datasets. The training dataset was used to refine the prompt given to the LLM, while the test dataset was used to generate the evidence tables for the evaluation by comparing them with the manually curated ones.

## Code
The "Code" folder contains all the Python scripts used in this project. To run the scripts automatically, you need two folders: one with the original studies in PDF format and another with evidence tables in Word format. It is recommended to name these files for easy identification, such as using the first author's name and the publication year. Once you have these folders, follow these steps:

### Generating Evidence Tables from PDF Studies
  1. Run the script 'pdf_studies2text' to convert the PDFs to text format using the path to your studies folder.
  2. Run the script 'compress_text_files' to reduce the size of the text files.
  3. Run the script 'GPT-4o_tables_generator' to generate the evidence tables from the compressed text files.

### Converting the Human-Curated Evidence Tables to Text Format
  1. Run the script 'word_evidence_tables2text' to convert the Word documents containing the human extracted evidence tables   to text format using the path to your evidence tables folder.

After this, you will have a folder with all the evidence tables generated by the LLM and another with the manually created ones in text format. To compare them, follow these steps:

### Numerical and Text Comparison of the Evidence Tables
  1. Run the script 'split_tables' to split the evidence tables created by humans and the LLM column by column and organize      them appropriately.
  2. Run the script 'numeric_comparison' to generate an Excel table with all relevant numeric metrics, column by column.
  3. Run the script 'text_comparison' to generate an Excel file with text similarities calculated by the different methods     (Jaccard, TF-IDF, BERT, Sentence-BERT and spaCy), column by column.

### Visualizing Results
Use the Jupyter notebook 'visualizations' to visualize these results.

## Evidence Tables for Manual Comparison
The "Evidence_tables_for_manually_comparison" folder contains the evidence tables extracted by the LLM and by humans from the test dataset. These can be used to manually compare their differences or to run the evaluation code without needing to generate the tables yourself, thus saving costs on the OpenAI API.
