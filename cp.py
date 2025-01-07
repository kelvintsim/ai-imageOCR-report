import os
import shutil
import openpyxl

def copy_files_from_excel(source_folder, destination_folder, excel_file, sheet_name):
    # Load the Excel workbook and sheet
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook[sheet_name]

    # Iterate through the rows in the sheet to get file names
    for row in sheet.iter_rows(min_row=1, max_col=1, values_only=True):
        file_name = row[0]
        if file_name:
            source_path = os.path.join(source_folder, file_name)
            destination_path = os.path.join(destination_folder, file_name)

            # Check if the file exists in the source folder
            if os.path.exists(source_path):
                # Copy the file to the destination folder
                shutil.copy(source_path, destination_path)
                print(f"Copied: {source_path} to {destination_path}")
            else:
                print(f"File does not exist: {source_path}")

if __name__ == "__main__":
    # Paths to the source folder, destination folder, and Excel file
    source_folder = './images'
    destination_folder = './images_parallel'
    excel_file = './difference.xlsx'
    sheet_name = 'Sheet1'  # Change to the name of your sheet if different

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Call the function to copy files
    copy_files_from_excel(source_folder, destination_folder, excel_file, sheet_name)