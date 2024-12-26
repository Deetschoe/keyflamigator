import os
import zipfile
import tkinter as tk
from tkinter import filedialog
import shutil
from pathlib import Path

def select_zip_files():
    """Open file dialog to select multiple ZIP files."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(
        title="Select ZIP files",
        filetypes=[("ZIP files", "*.zip")]
    )
    return file_paths

def create_output_folder():
    """Create output folder on desktop."""
    desktop_path = os.path.expanduser("~/Desktop")
    output_folder = os.path.join(desktop_path, "ExtractedKeyframes")
    
    # If folder exists, remove it and its contents
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    
    os.makedirs(output_folder)
    return output_folder

def is_image_file(filename):
    """Check if file is an image based on extension."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def extract_and_rename_images():
    """Main function to extract and rename images from ZIP files."""
    # Select ZIP files
    zip_files = select_zip_files()
    if not zip_files:
        print("No files selected. Exiting...")
        return

    # Create output folder
    output_folder = create_output_folder()
    
    # Counter for renaming images
    image_counter = 1
    
    # Process each ZIP file
    for zip_path in sorted(zip_files):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Get list of image files in ZIP
                image_files = [f for f in zip_ref.namelist() if is_image_file(f)]
                
                # Sort image files to maintain order
                image_files.sort()
                
                # Extract and rename each image
                for image_file in image_files:
                    # Determine output extension (preserve original extension)
                    original_ext = Path(image_file).suffix
                    new_filename = f"image_{image_counter}{original_ext}"
                    
                    # Extract image to temp location
                    zip_ref.extract(image_file, output_folder)
                    
                    # Build paths
                    temp_path = os.path.join(output_folder, image_file)
                    new_path = os.path.join(output_folder, new_filename)
                    
                    # Rename file
                    os.rename(temp_path, new_path)
                    
                    # Clean up any empty directories created during extraction
                    temp_dir = os.path.dirname(temp_path)
                    while temp_dir != output_folder:
                        try:
                            os.rmdir(temp_dir)
                        except OSError:
                            break
                        temp_dir = os.path.dirname(temp_dir)
                    
                    print(f"Extracted and renamed: {new_filename}")
                    image_counter += 1
                    
        except Exception as e:
            print(f"Error processing {os.path.basename(zip_path)}: {str(e)}")

    print(f"\nComplete! Extracted {image_counter-1} images to: {output_folder}")

if __name__ == "__main__":
    extract_and_rename_images()