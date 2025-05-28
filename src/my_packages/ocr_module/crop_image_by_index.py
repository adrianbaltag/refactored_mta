import os

from PIL import Image


def crop_image_by_index(image_index: int, crop_left: int = 350, crop_right: int = 420):
    """
    Crops the left and right sides of an image located in a specific directory,
    selected by its index, and saves the cropped image.

    Args:
        image_index (int): The 0-based index of the image to process within the
                           'my_packages/images' directory (after sorting by filename).
        crop_left (int): The number of pixels to crop from the left side of the image.
        crop_right (int): The number of pixels to crop from the right side of the image.
    """
    # Prepare project and image directory paths
    # This assumes the script is run from a location where
    # os.path.dirname(__file__) correctly points to a script
    # inside a structure like 'project_root/some_folder/your_script.py'
    # relative to 'project_root/my_packages/images'.
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    images_dir = os.path.join(project_root, "my_packages", "images")

    # Ensure the images directory exists
    if not os.path.isdir(images_dir):
        print(f"Error: Image directory not found at '{images_dir}'.")
        return

    # Get a list of all files in the images directory
    all_files = os.listdir(images_dir)

    # Filter out only image files (you might need to adjust extensions)
    image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff")
    image_files = [
        f
        for f in all_files
        if f.lower().endswith(image_extensions)
        and os.path.isfile(os.path.join(images_dir, f))
    ]

    # Sort the image files. This is crucial for consistent indexing.
    # For numerical sorting (e.g., 'image1.png', 'image10.png', 'image2.png' -> 'image1.png', 'image2.png', 'image10.png'),
    # you might need the 'natsort' library: `pip install natsort`
    # and then use `image_files = natsort.natsorted(image_files)`
    image_files.sort()

    if not image_files:
        print(f"Error: No image files found in '{images_dir}'.")
        return

    if image_index < 0 or image_index >= len(image_files):
        print(f"Error: Image index {image_index} is out of bounds.")
        print(
            f"There are {len(image_files)} image(s) available (indices 0 to {len(image_files) - 1})."
        )
        return

    # Get the filename of the image at the specified index
    selected_image_filename = image_files[image_index]

    # Construct the full path to the selected image
    image_path = os.path.join(images_dir, selected_image_filename)

    # Open the image
    try:
        img = Image.open(image_path)
        print(f"Successfully opened image: {image_path}")
    except FileNotFoundError:
        print(
            f"Error: The image file '{image_path}' was not found. Please check the path and filename."
        )
        return
    except Exception as e:
        print(f"An error occurred while opening the image '{image_path}': {e}")
        return

    # Get image dimensions
    width, height = img.size

    # Calculate the cropping box coordinates (left, upper, right, lower)
    # Upper will be 0 and lower will be height for cropping only left and right
    box = (crop_left, 0, width - crop_right, height)

    # Validate crop values to prevent negative dimensions or invalid boxes
    if crop_left >= width - crop_right:
        print(
            f"Warning: Crop values (left={crop_left}, right={crop_right}) result in zero or negative width."
        )
        print("No cropping performed or image might be empty.")
        # Optionally, you could return or raise an error here
        return

    # Crop the image
    cropped_img = img.crop(box)

    # Define the output path for the cropped image
    # Add "_cropped" before the extension for clarity.
    name, ext = os.path.splitext(selected_image_filename)
    output_filename = f"{name}_cropped{ext}"
    output_path = os.path.join(
        images_dir, output_filename
    )  # Save in the same directory

    # Save the cropped image
    try:
        cropped_img.save(output_path)
        print(f"Cropped image saved to: {output_path}")
    except Exception as e:
        print(
            f"An error occurred while saving the cropped image to '{output_path}': {e}"
        )

    # Display the cropped image (optional)
    cropped_img.show()


# --- Example Usage ---
if __name__ == "__main__":
    # To crop the first image (index 0)
    print("--- Processing image at index 0 ---")
    crop_image_by_index(0)

    # To crop the second image (index 1) with custom crop amounts
    # Make sure you have at least two images in your folder for this to work
    # print("\n--- Processing image at index 1 with custom crop amounts ---")
    # crop_image_by_index(1, crop_left=100, crop_right=150)

    # Example of an out-of-bounds index (will print an error)
    # print("\n--- Attempting to process image at an invalid index (e.g., 99) ---")
    # crop_image_by_index(99)
