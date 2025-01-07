import os
import requests
import pandas as pd
from pathlib import Path
from io import StringIO
import json

# Constants
UPLOAD_API_URL = ""  # Replace with actual File Upload API endpoint
CHAT_API_URL = ""  # Replace with actual Chat API endpoint
API_KEY = ""  # Replace with your actual API key
IMAGE_DIRECTORY = "./images_parallel"  # Local directory containing receipt images
EXCEL_FILE_PATH = "data_parallel.xlsx"
USER_ID = "poc-user"  # User ID required by the API

EXPECTED_COLUMNS = ["mall_name", "mall_address", "shop_name", "shop_address",
                    "receipt_date", "receipt_number", "payment_method",
                    "total_list_price", "full_content_all_displayed_information"]

def upload_image(image_path):
    """Uploads image to the Dify AI platform and returns the upload_file_id."""
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    files = {
        'file': (image_path.name, open(image_path, 'rb'), f'image/{image_path.suffix[1:]}'),
    }
    data = {'user': USER_ID}
    response = requests.post(UPLOAD_API_URL, headers=headers, files=files, data=data)
    response.raise_for_status()  # raise an exception for HTTP errors
    return response.json()['id']  # assuming the response has 'id' key 

def process_image(upload_file_id):
    """Sends the uploaded image file ID to the Dify AI platform and returns the CSV response."""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    files = [
        {
            "type": "image",
            "transfer_method": "local_file",
            "upload_file_id": upload_file_id
        }
    ]
    
    data = {
        "inputs": {},
        "query": "Extract receipt data",
        "response_mode": "streaming",
        "conversation_id": "",
        "user": USER_ID,
        "files": files
    }

    try:
        with requests.post(CHAT_API_URL, headers=headers, json=data, stream=True) as response:
            response.raise_for_status()  # raise an exception for HTTP errors
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        json_data = json.loads(decoded_line[len("data: "):])
                        if json_data.get('event') == 'agent_thought':
                            thought = json_data.get('thought', '')
                            if thought:
                                print(f"Extracted CSV Text: \n{thought}\n")  # Debug output
                                return thought
            print("No 'agent_thought' event found in the response.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
        print(f"Request payload: {data}")
    except ValueError as json_err:
        print(f"JSON decode error occurred: {json_err}")
        print(f"Response content: {response.content}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def clean_csv_data(csv_data):
    """Cleans CSV data by appropriately handling newlines and ensuring proper quoting."""
    lines = csv_data.split('\n')
    cleaned_lines = []
    for line in lines:
        if line:
            quoted = '"' in line and line.count('"') % 2 == 0  # Check for even number of quotes
            cleaned_line = line
            if not quoted:
                cleaned_line = '"' + line.replace('"', '""').replace('\r', '').replace('\n', ' ') + '"'
            cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)

def main():
    all_data_frames = []
    image_files = [f for f in os.listdir(IMAGE_DIRECTORY) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        image_path = Path(IMAGE_DIRECTORY) / image_file
        print(f"Uploading and processing image: {image_path}")
        try:
            upload_file_id = upload_image(image_path)
            csv_data = process_image(upload_file_id)
            if csv_data:
                print(f"Original CSV Data for {image_file}:\n{csv_data}\n")  # Log the original CSV data
                cleaned_csv_data = clean_csv_data(csv_data)
                print(f"Cleaned CSV Data for {image_file}:\n{cleaned_csv_data}\n")  # Debug the cleaned CSV data
                # Convert cleaned CSV data to DataFrame manually
                try:
                    # Prepare manual header from EXPECTED_COLUMNS for the DataFrame
                    data = StringIO(cleaned_csv_data)
                    df = pd.read_csv(data, header=None)  # Read without header
                    if df.shape[1] == len(EXPECTED_COLUMNS):  # Ensure column count matches expected count
                        df.columns = EXPECTED_COLUMNS  # Manually set columns
                        df.insert(0, 'image_file', image_file)  # Insert image file name as the first column
                        all_data_frames.append(df)
                    else:
                        print(f"CSV data for {image_file} does not match expected format. Skipping.")
                except pd.errors.ParserError as parse_err:
                    print(f"Error parsing CSV data for {image_file}: {parse_err}")
                    print(f"Skipping file {image_file} due to CSV parsing error.")
            else:
                print(f"No CSV data returned for file: {image_file}")
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")

    if all_data_frames:
        combined_data_frame = pd.concat(all_data_frames, ignore_index=True)
        combined_data_frame.to_excel(EXCEL_FILE_PATH, index=False)
        print(f"All data successfully written to {EXCEL_FILE_PATH}")
    else:
        print(f"No data to write to Excel.")

if __name__ == "__main__":
    main()