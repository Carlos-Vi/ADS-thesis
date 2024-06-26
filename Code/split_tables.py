import os

# Function to split sections from human and GPT-generated evidence tables and save them in separate folders
def split_sections(input_folder_human, input_folder_gpt, output_base_folder):
    human_files = sorted(os.listdir(input_folder_human))
    gpt_files = sorted(os.listdir(input_folder_gpt))

    # Iterate over each pair of human and GPT files
    for idx, (human_file, gpt_file) in enumerate(zip(human_files, gpt_files)):
        human_file_path = os.path.join(input_folder_human, human_file)
        gpt_file_path = os.path.join(input_folder_gpt, gpt_file)
        
        # Read the contents of the human file
        with open(human_file_path, 'r', encoding='utf-8') as file:
            human_content = file.read()

        # Read the contents of the GPT file
        with open(gpt_file_path, 'r', encoding='utf-8') as file:
            gpt_content = file.read()

        # Split the content into sections based on the '---' delimiter
        human_sections = human_content.split('---')
        gpt_sections = gpt_content.split('---')
        
        # Remove any empty sections and strip whitespace
        human_sections = [section.strip() for section in human_sections if section.strip()]
        gpt_sections = [section.strip() for section in gpt_sections if section.strip()]
        
        # Determine the base name for the output folder from the human file name
        file_base_name = os.path.splitext(human_file)[0]
        output_folder = os.path.join(output_base_folder, file_base_name)
        os.makedirs(output_folder, exist_ok=True)

        # Iterate over each section and save them in separate files
        for i, (human_section, gpt_section) in enumerate(zip(human_sections, gpt_sections)):
            section_number = i + 1
            column_folder = os.path.join(output_folder, f'Column_{section_number}')
            os.makedirs(column_folder, exist_ok=True)

            # Define the output paths for the human and GPT sections
            human_output_file_path = os.path.join(column_folder, f'human_section_{section_number}.txt')
            gpt_output_file_path = os.path.join(column_folder, f'gpt_section_{section_number}.txt')

            # Write the human section to a file
            with open(human_output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(human_section)

            # Write the GPT section to a file
            with open(gpt_output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(gpt_section)

        print(f'Study {idx + 1} ({human_file} and {gpt_file}) has been split and saved.')

# Define input and output folders
input_folder_human = 'Human_evidence_tables_text_format'
input_folder_gpt = 'GPT4o_evidence_tables_text_format_compressed'
output_base_folder = 'Tables_split'

# Create the output base folder if it doesn't exist
os.makedirs(output_base_folder, exist_ok=True)

# Call the function to split the files into sections and save them
split_sections(input_folder_human, input_folder_gpt, output_base_folder)
