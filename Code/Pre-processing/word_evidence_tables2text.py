import docx
import os

# Folder containing your Word documents
doc_folder = 'Path to a folder containing your evidence tables for each study in Word format'
txt_folder = 'Evidence_tables_text_format'

# Create the output folder if it doesn't exist
os.makedirs(txt_folder, exist_ok=True)

# Function to extract table from Word document and write to text file
def extract_table_to_text(file_path, output_path):
    try:
        # Load the Word document
        doc = docx.Document(file_path)
        
        # Assume the table we want to extract is the first table in the document
        table = doc.tables[0]
        
        # Extract data into a list of lists (each sublist is a row)
        data = [[cell.text for cell in row.cells] for row in table.rows]
        
        # Transpose data to separate columns
        columns = list(zip(*data))
        
        # Open a file to write the output with UTF-8 encoding
        with open(output_path, 'w', encoding='utf-8') as file:
            for i, col in enumerate(columns):
                file.write(f"{i+1}. ")
                file.write("\n".join(col))
                file.write("\n\n---\n\n")     
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

# Iterate over all Word files in the folder
study_count = 0
for filename in os.listdir(doc_folder):
    if filename.endswith('.docx'):
        study_count += 1
        doc_path = os.path.join(doc_folder, filename)
        txt_output_path = os.path.join(txt_folder, f'{os.path.splitext(filename)[0]}.txt')
        
        # Extract table from Word document and write to text file
        extract_table_to_text(doc_path, txt_output_path)

        print(f"Study {study_count}: Evidence table saved successfully from {filename} to {txt_output_path}")
