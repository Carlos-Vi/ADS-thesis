import os
import re
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch
from sentence_transformers import SentenceTransformer, util

# Suppress all warnings
import warnings
warnings.filterwarnings('ignore')

# Function to compare texts using TF-IDF and cosine similarity
def compare_texts_tfidf(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    similarity = cosine_similarity(vectors)
    return similarity[0, 1] * 100

# Function to preprocess text by converting to lowercase and extracting words
def preprocess_text(text):
    return set(re.findall(r'\b\w+\b', text.lower()))

# Function to calculate Jaccard similarity between two texts
def jaccard_similarity(text1, text2):
    set1 = preprocess_text(text1)
    set2 = preprocess_text(text2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) * 100

# Function to compare texts using spaCy's pre-trained model
def compare_texts_spacy(text1, text2):
    nlp = spacy.load("en_core_web_md")
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    similarity = doc1.similarity(doc2) * 100
    return similarity

# Function to compare texts using BERT embeddings and cosine similarity
def compare_texts_bert(text1, text2):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    # Tokenize and encode texts
    inputs1 = tokenizer(text1, return_tensors='pt', truncation=True, max_length=512)
    inputs2 = tokenizer(text2, return_tensors='pt', truncation=True, max_length=512)
    with torch.no_grad():
        # Get BERT embeddings
        outputs1 = model(**inputs1)
        outputs2 = model(**inputs2)
    embedding1 = outputs1.last_hidden_state.mean(dim=1)
    embedding2 = outputs2.last_hidden_state.mean(dim=1)
    # Calculate cosine similarity
    similarity = torch.nn.functional.cosine_similarity(embedding1, embedding2)
    return similarity.item() * 100

# Function to compare texts using Sentence-BERT
def compare_texts_sbert(text1, text2):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    # Encode texts
    embeddings = model.encode([text1, text2])
    # Calculate cosine similarity
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return similarity.item() * 100

# Function to process folders, compare text sections, and save results to an Excel file
def process_folders(base_folder, output_excel):
    results = []

    # Iterate over each study folder in the base folder
    for study_folder in os.listdir(base_folder):
        study_path = os.path.join(base_folder, study_folder)
        
        if os.path.isdir(study_path):
            # Initialize a dictionary to store results for the current study
            study_results = {"study_name": study_folder}
            column_index = 1  
            
            # Iterate over each column folder in the study folder
            for column_folder in sorted(os.listdir(study_path)):
                column_path = os.path.join(study_path, column_folder)
                if os.path.isdir(column_path):
                    # Define the expected file names for human and GPT sections
                    human_file_name = f'human_section_{column_index}.txt'
                    gpt_file_name = f'GPT_section_{column_index}.txt'

                    try:
                        # Construct the full file paths
                        human_file_path = os.path.join(column_path, human_file_name)
                        gpt_file_path = os.path.join(column_path, gpt_file_name)

                        # Read the contents of the human and GPT files
                        with open(human_file_path, 'r', encoding='utf-8') as fileA, open(gpt_file_path, 'r', encoding='utf-8') as fileB:
                            textA = fileA.read()
                            textB = fileB.read()

                        # Compare texts and store results under dynamically generated keys
                        study_results.update({
                            f"tfidf_{column_index}": compare_texts_tfidf(textA, textB),
                            f"jaccard_{column_index}": jaccard_similarity(textA, textB),
                            f"spacy_{column_index}": compare_texts_spacy(textA, textB),
                            f"bert_{column_index}": compare_texts_bert(textA, textB),
                            f"sbert_{column_index}": compare_texts_sbert(textA, textB),
                        })
                        column_index += 1
                    except FileNotFoundError:
                        # Print a message if expected files are missing and continue with the next folder
                        print(f"Missing files in {column_folder} of {study_folder}, skipping...")

            if len(study_results) > 1:  # Ensures there's more than just the study_name key
                results.append(study_results)

    # Create a DataFrame from the results and save it to an Excel file
    df = pd.DataFrame(results)
    df.to_excel(output_excel, index=False)

# Define base folder and output excel file path
base_folder = 'Tables_split'
output_excel = 'text_comparison.xlsx'

# Process folders and save results to Excel
process_folders(base_folder, output_excel)

