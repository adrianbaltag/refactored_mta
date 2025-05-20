"""This script deletes all image files in the selected' folder located in src/my_packages/."""

import glob
import os


def delete_images_in_folder(folder):
    """
    Deletes all image files in the selected folder located in the src/my_packages/.
    Common image extensions are targeted: jpg, jpeg, png, gif, bmp, tiff, webp.
    __param folder: The name of the folder containing the images.
    __return: True if images are deleted successfully, False otherwise.
    """
    # Path to the images folder in the current directory
    images_folder = os.path.join(os.getcwd(), f"src/my_packages/{folder}")

    # Check if the folder exists
    if not os.path.exists(images_folder):
        print(f"Error: The folder {images_folder} does not exist.")
        return False

    # List of common image file extensions
    image_extensions = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.gif",
        "*.bmp",
        "*.tiff",
        "*.webp",
    ]

    # Counter for deleted files
    deleted_count = 0

    # Delete all image files
    for ext in image_extensions:
        image_pattern = os.path.join(images_folder, ext)
        for image_file in glob.glob(image_pattern):
            try:
                os.remove(image_file)
                print(f"Deleted: {image_file}")
                deleted_count += 1
            except (FileNotFoundError, PermissionError) as e:
                print(f"Error deleting {image_file}: {str(e)}")

    print(f"Total images deleted: {deleted_count}")
    return True


# Example usage
if __name__ == "__main__":
    delete_images_in_folder("images")
