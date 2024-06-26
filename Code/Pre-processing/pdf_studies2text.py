import fitz  
import camelot
import os

# Folder containing your PDF files
pdf_folder = 'Path to a folder containing the studies in PDF format'
txt_folder = 'Studies_text_format'

# Create the output folder if it doesn't exist
os.makedirs(txt_folder, exist_ok=True)

# Ghostscript necessary for working with the imported libraries
ghostscript_path = r"C:\Program Files\gs\gs10.03.1\bin\gswin64c.exe"
os.environ["PATH"] += os.pathsep + os.path.dirname(ghostscript_path)

# Function to extract and write text from PDF
def extract_text(pdf_path, output_path):
    pdf_document = fitz.open(pdf_path)
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text("text")
            txt_file.write(text + '\n\n')

# Function to extract and write tables from PDF
def extract_tables(pdf_path, output_path):
    try:
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
        with open(output_path, 'a', encoding='utf-8') as txt_file:
            for i, table in enumerate(tables):
                txt_file.write(f"\nTable {i + 1}\n")
                txt_file.write(table.df.to_string(index=False))
                txt_file.write('\n\n')
    except Exception as e:
        print(f"An error occurred while extracting tables from {pdf_path}: {e}")

# Iterate over all PDF files in the folder
study_count = 0
for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        study_count += 1
        pdf_path = os.path.join(pdf_folder, filename)
        txt_output_path = os.path.join(txt_folder, f'{os.path.splitext(filename)[0]}.txt')
        
        # Extract text from PDF and write to text file
        extract_text(pdf_path, txt_output_path)
        
        # Extract tables from PDF and append to the same text file
        extract_tables(pdf_path, txt_output_path)
        
        print(f'Study {study_count}: Text and tables have been successfully extracted from {filename} to {txt_output_path}')