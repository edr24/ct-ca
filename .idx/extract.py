import pandas as pd
import re

def process_column(text):
    # Initialize the result dictionary with keys as the new column names
    result = {
        'Heart Size': '',
        'Lungs to Scan Quality': '',
        'Scan Quality to HR': '',
        'HR to B-Blockade': '',
        'B-Blockade to BMI': '',
        'BMI to DLP': '',
        'Dominance': '',
        'Left Mainstem': '',
        'LAD': '',
        'Circumflex': '',
        'Right Coronary Artery': '',
        'Aortic and Mitral Valve': '',
        'Left Ventricle': '',
        'Non Cardiac Findings': '',
        'Impression': '',
        'Clinical History': ''
    }

    if text.startswith("CT Cardiac"):
        patterns = {
            'Heart Size': r"Heart size :(.*?)Lungs",
            'Lungs to Scan Quality': r"Lungs(.*?)scan quality",
            'Scan Quality to HR': r"scan quality(.*?)HR",
            'HR to B-Blockade': r"HR(.*?)B-Blockade",
            'B-Blockade to BMI': r"B-Blockade(.*?)BMI",
            'BMI to DLP': r"BMI(.*?)DLP",
            'Dominance': r"dominance (Right|Left)",
            'Left Mainstem': r"Left Mainstem(.*?)(?=LAD|Circumflex|Right coronary artery|$)",
            'LAD': r"LAD(.*?)(?=Circumflex|Right coronary artery|$)",
            'Circumflex': r"Circumflex(.*?)(?=Right coronary artery|$)",
            'Right Coronary Artery': r"Right coronary artery(.*?)(?=Aortic and mitral valve|$)",
            'Aortic and Mitral Valve': r"Aortic and mitral valve(.*?)(?=Left ventricle|$)",
            'Left Ventricle': r"Left ventricle(.*?)(?=Non cardiac findings|$)",
            'Non Cardiac Findings': r"Non cardiac findings(.*?)(?=Impression|$)",
            'Impression': r"Impression(.*?)$"
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                result[key] = match.group(1).strip()

        # Handle 'Clinical History' separately
        if "Clinical history" in text:
            result['Clinical History'] = text.split("Clinical history")[-1].strip()

    return result

def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    if df.shape[1] < 7:
        print("The specified column index does not exist in the data.")
        return

    # Process the 7th column
    expanded_data = df.iloc[:, 6].apply(process_column).apply(pd.Series)

    # Keep the initial 6 columns and append the new ones
    result_df = pd.concat([df.iloc[:, :6], expanded_data], axis=1)

    result_df.to_csv(output_csv, index=False)

# Example usage
input_csv_path = 'input.csv'
output_csv_path = 'processed_output.csv'
process_csv(input_csv_path, output_csv_path)
