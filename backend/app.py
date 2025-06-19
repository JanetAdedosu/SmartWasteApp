
# if __name__ == '__main__':
#     app.run(debug=True)

import zipfile
import os

# Specify the zip file path and output directory
zip_path = "archive.zip"  # Zip file in the backend folder
extract_to = "dataset"    # Directory to extract files to

# Print the current working directory for debugging
print(f"Current working directory: {os.getcwd()}")

# Check if the zip file exists before extracting
if os.path.exists(zip_path):
    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Dataset extracted to {extract_to}")
else:
    print(f"Error: {zip_path} does not exist. Please check the file path.")

