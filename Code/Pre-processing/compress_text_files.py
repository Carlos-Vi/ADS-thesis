import os
import re

# Function to remove unnecessary spaces
def remove_unnecessary_spaces(text):
    # Removing extra spaces, tabs, and new lines
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text) 
    return text

# Input and output folder paths
input_folder = 'Studies_text_format'
output_folder = 'Studies_text_format_compressed'

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process each file in the input folder
for idx, filename in enumerate(os.listdir(input_folder)):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Clean the content
        cleaned_content = remove_unnecessary_spaces(content)
        
        # Define output file path
        output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_compressed.txt')
        # Save the cleaned content to the output file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)
        
        print(f"Study {idx + 1}: {filename} has been cleaned and saved.")

print("All files have been processed and cleaned.")
