from openai import OpenAI
import os
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

# Initialize the OpenAI client
client = OpenAI(
    api_key='Use your API key'
)

# Function to read the content of a text file
def read_text_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return file.read()

# Function to save the response to a text file
def save_response_to_text(response, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(response)

# Function to get response from OpenAI with retry mechanism
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_openai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,  
        top_p=1,        
        n=1            
    )
    return response.choices[0].message.content



# Folder containing your text documents
txt_folder = 'Studies_text_format_compressed'
output_folder = 'GPT4o_evidence_tables_text_format_compressed'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)


# Iterate over all text files in the folder
study_count = 0
for filename in os.listdir(txt_folder):
    if filename.endswith('.txt'):
        study_count += 1
        text_file_path = os.path.join(txt_folder, filename)
        output_file_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_table_GPT4o.txt')
        
        # Read the content of the text file
        text_content = read_text_file(text_file_path)
        
        # Define the prompt
        prompt = f"""The following is the content of a document:\n\n{text_content}\n\n
        You are going to help healthcare experts develop medical guidelines. We are providing you with a text containing a Randomized Controlled Trial (RCT) from a medical study. The output must be structured into 8 clearly differentiated sections, labeled from one to eight, with the following information:
        
        1. Study reference: 
           - Write the name of the first author of the paper and the year of publication, separated by a comma.
        
        2. Study characteristics: 
           - Specify the "type of study" and its characteristics, the "setting and country" where it was conducted and its "funding and conflicts of interest".
        
        3. Patient characteristics: 
           - Explain the inclusion and exclusion criteria for participating in the study.
           - Provide the total number of participants at the beginning of the experiment, separated into the intervention and control groups.
           - List any other characteristics (e.g., age, sex, coexisting conditions, biological characteristics, etc.) you can find of the participants at the beginning of the study. Divide it into the intervention and control groups. Don’t omit any numerical information even if it doesn’t look relevant.
           - Decide if the groups were comparable at the beginning of the experiment based on this information.
        
        4. Intervention: 
           - Describe the treatment and process followed by the intervention group exactly as outlined in the article. Write the answer directly without starting with phrases like “Intervention:”
        
        5. Comparison/Control: 
           - Describe the treatment and process followed by the control group exactly as outlined in the article. Write the answer directly without starting with phrases like “Control:”
        
        6. Follow-up:
           - State the length of the follow-up, meaning the time the patients were monitored after the intervention.
           - State if there was “Loss-to-follow-up”, including the number, percentage and reasons for participants who could not be tracked or reached for further data collection, divided into the intervention and control groups. This can happen because of the relocation of the participants, loss of contact, health problems, death or loss of interest for example. 
           - Explain if there was “Incomplete outcome data”, including the number, percentage, and reasons for missing data, divided into the intervention and control groups. This can happen because of the loss of data due to administrative errors, incomplete measurements, not answering specific questions or dropping out of the study for example.
        Usually this information is not directly specify in the study, so you have to compare the number of participants at the beginning and at the end of the study.
        
        7. Outcome measures and effect size: 
           - Provide all the results from the experiment you can find, divided into the intervention and control groups. These results can include mortality, recovery, duration of the treatment, complications and any other information of the participants at the end or any stage of the experiment. Don't omit any numerical information present in the study even if it doesn't look relevant.
           - Include p-values and 95% Confidence Intervals if possible.
        
        8. Comments: 
           - Add any information that might be contradictory or confusing in the study.
        
        When providing the answers, do not use any special formatting such as italics or bold. To differentiate between sections, finish each one with the chain of characters "---". When listing the numerical values for the characteristics of the participants at the beginning or end of the study, use a separate line for each characteristic. Your answer will be saved in a plain text (.txt) file.
        IMPORTANT: Accuracy is crucial. Be as rigorous as possible when answering each section. Do not assume anything. If some information is missing, explicitly state that the information could not be found. Not finding something is acceptable. Quote directly from the study whenever possible. Provide not only the numerical values but also any other characteristics of these values (e.g., SD, IQR, etc.).
        """
        
            
        # Get the response from OpenAI
        response_content = get_openai_response(prompt)
        
        # Save the response to a text file
        save_response_to_text(response_content, output_file_path)
        
        print(f"Study {study_count}: Model evidence table successfully extracted from {filename} to {output_file_path}")
