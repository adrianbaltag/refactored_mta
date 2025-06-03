import os

from PIL import Image


def crop_by_index_top_only(image_index: int, crop_top: int = 400):
    """
    Crops the top side of an image located in a specific directory,
    selected by its index, and saves the cropped image.

    Args:
        image_index (int): The 0-based index of the image to process within the
                            'my_packages/images' directory (after sorting by filename).
        crop_top (int): The number of pixels to crop from the top of the image.
    """
    # Prepare project and image directory paths
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    images_dir = os.path.join(project_root, "my_packages", "img_to_read")

    # Ensure the images directory exists
    if not os.path.isdir(images_dir):
        print(f"Error: Image directory not found at '{images_dir}'.")
        return

    # Get a list of all files in the images directory
    all_files = os.listdir(images_dir)

    # Filter out only image files
    image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff")
    image_files = [
        f
        for f in all_files
        if f.lower().endswith(image_extensions)
        and os.path.isfile(os.path.join(images_dir, f))
    ]

    # Sort the image files.
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
    # To crop only from the top:
    # - left stays 0 (no horizontal crop)
    # - upper is crop_top (start cropping from this pixel down)
    # - right stays width (no horizontal crop)
    # - lower stays height (no crop from the bottom)
    box = (0, crop_top, width, height)

    # Validate crop values
    if crop_top >= height:
        print(
            f"Warning: Crop value (top={crop_top}) is greater than or equal to image height ({height})."
        )
        print("No cropping performed or image might be empty.")
        return

    # Crop the image
    cropped_img = img.crop(box)

    # Define the output path for the cropped image
    name, ext = os.path.splitext(selected_image_filename)
    # Use "_cropped_top" to clearly indicate the type of crop
    output_filename = f"{name}_cropped_top{ext}"
    output_path = os.path.join(images_dir, output_filename)

    # Save the cropped image
    try:
        cropped_img.save(output_path)
        print(f"Cropped image saved to: {output_path}")
    except Exception as e:
        print(
            f"An error occurred while saving the cropped image to '{output_path}': {e}"
        )

    # Display the cropped image (optional)
    # cropped_img.show()


### Example Usage


if __name__ == "__main__":
    # Crop the first image (index 0) by 100 pixels from the top
    print("--- Processing image at index 0 (top-only crop) ---")
    crop_by_index_top_only(0, crop_top=400)

    # If you want to crop by 0 pixels from the top (effectively no crop):
    # crop_image_by_index(0)
