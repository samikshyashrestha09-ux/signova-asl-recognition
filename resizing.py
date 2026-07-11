import cv2
import os

# Input and output folder paths
input_folder = r"C:\Users\rabin\OneDrive\Desktop\sign_language_project\asl_dataset\ASL_Raw_Images\asl_dataset\Z"
output_folder = "resized_images"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all files in input folder
for filename in os.listdir(input_folder):
    img_path = os.path.join(input_folder, filename)

    # Read image
    image = cv2.imread(img_path)

    # Skip if file is not an image
    if image is None:
        continue

    # Resize image to 640x640
    resized_image = cv2.resize(image, (640, 640))

    # Save resized image
    save_path = os.path.join(output_folder, filename)
    cv2.imwrite(save_path, resized_image)

    print(f"Resized and saved: {filename}")

print("All images resized successfully!")
