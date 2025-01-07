# Image Processing and Recognition Python Scripts

This repository contains Python scripts for processing receipt images to extract relevant data and calculate average image dimensions within a directory.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Image Recognition Script](#image-recognition-script)
  - [Average Image Dimensions Script](#average-image-dimensions-script)
- [Configuration](#configuration)
  - [Image Recognition Script Configuration](#image-recognition-script-configuration)
  - [Average Image Dimensions Script Configuration](#average-image-dimensions-script-configuration)
- [License](#license)
- [Contact](#contact)

## Overview

### Image Recognition Script
This script performs the following tasks:
1. Uploads receipt images to the Dify AI platform.
2. Processes the uploaded images to extract relevant data in CSV format.
3. Cleans and normalizes the extracted CSV data.
4. Converts the cleaned data into a pandas DataFrame, and combines this data from all images.
5. Exports the combined data to an Excel file.

### Average Image Dimensions Script
This script processes images within a specified directory to calculate and return the average width and height of the images.

## Prerequisites

- Python 3.6 or higher.
- Following Python packages:
  - `requests`
  - `pandas`
  - `openpyxl`
  - `Pillow`
  - `numpy`
  - `concurrent.futures`

Ensure you have a valid API key for the Dify AI platform for the image recognition script.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/<your-repo>/image-processing.git
    cd image-processing
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Image Recognition Script

1. Place all receipt images in the specified directory (default is `./images_parallel`).
2. Modify configuration constants as necessary.
3. Run the script:
    ```sh
    python image_recognition.py
    ```

4. The script will output the extracted data and save it into an Excel file.

### Average Image Dimensions Script

1. Place all images in the specified directory (default is `./images`).
2. Modify the `directory_path` variable to point to your images directory.
3. Run the script:
    ```sh
    python average_image_dimensions.py
    ```

4. The script will output the average width and height of images in the specified directory.

## Configuration

### Image Recognition Script Configuration

The following configuration variables are available at the beginning of the script:
- `UPLOAD_API_URL`: URL for uploading images.
- `CHAT_API_URL`: URL for processing the uploaded images.
- `API_KEY`: API key for authenticating with the Dify AI platform.
- `IMAGE_DIRECTORY`: Directory containing the images to be processed.
- `EXCEL_FILE_PATH`: Path to save the output Excel file.
- `USER_ID`: User ID required for the API.

### Average Image Dimensions Script Configuration

The `directory_path` variable at the bottom of the script specifies the directory containing the images:
```python
directory_path = './images'  # Replace with the path to your directory containing images
```

## License

This project is licensed under the MIT License.

## Contact

For any issues or questions, please contact [your-email@example.com].

---

This README provides a comprehensive guide for using the image processing and recognition Python scripts. Ensure you update any placeholder details with actual values before deployment.