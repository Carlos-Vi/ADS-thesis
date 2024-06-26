import os
import re
import pandas as pd


# Function to extract all numbers from a given text
def extract_numbers(text):
 
     # Use regular expressions to find all numbers until 3 decimals in the text
    numbers = re.findall(r'\b\d+\.\d{1,3}|\b\d+\b', text)
    # Convert the found numbers to float and return as a set to ensure uniqueness
    return set(map(float, numbers))


# Function to compare numbers between two texts.
def compare_numbers(textA, textB):
    
    # Extract numbers from both texts
    numbers_A = extract_numbers(textA)
    numbers_B = extract_numbers(textB)

    # Count the numbers in both sets
    count_A = len(numbers_A)
    count_B = len(numbers_B)
    
    # Find common numbers, unique numbers in textA, and unique numbers in textB
    common_numbers = numbers_A.intersection(numbers_B)
    unique_A = numbers_A.difference(numbers_B)
    unique_B = numbers_B.difference(numbers_A)

    # Calculate precision and recall
    precision = 100 * len(common_numbers) / count_B if count_B else 0
    recall = 100 * len(common_numbers) / count_A if count_A else 100
    
    return {
        "accuracy": precision,
        "recall": recall,
        "human_count": count_A,
        "gpt_count": count_B,
        "TP": len(common_numbers),
        "FN": len(unique_A),
        "FP": len(unique_B)
    }


# Process folders containing text files, compare numbers, and save results to an Excel file.
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
                        human_file_path = os.path.join(column_path, human_file_name)
                        gpt_file_path = os.path.join(column_path, gpt_file_name)

                        # Read the contents of the human and GPT files
                        with open(human_file_path, 'r', encoding='utf-8') as fileA, open(gpt_file_path, 'r', encoding='utf-8') as fileB:
                            textA = fileA.read()
                            textB = fileB.read()

                        # Compare the numbers in the two texts
                        result = compare_numbers(textA, textB)

                        # Add the comparison results to the study results dictionary
                        for key, value in result.items():
                            study_results[f"{key}_column_{column_index}"] = value

                        column_index += 1
                    except FileNotFoundError:
                        # Print a message if expected files are missing and continue with the next folder
                        print(f"Missing files in {column_folder} of {study_folder}, skipping...")

            # Ensure there's more than just the study_name key before adding to results
            if len(study_results) > 1:
                results.append(study_results)

    # Create a DataFrame from the results and save it to an Excel file
    df = pd.DataFrame(results)
    df.to_excel(output_excel, index=False)

# Define base folder and output Excel file path
base_folder = 'Tables_split'
output_excel = 'numeric_comparison.xlsx'

# Process folders and save results to Excel
process_folders(base_folder, output_excel)
