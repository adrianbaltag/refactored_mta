from pathlib import Path


def move_file_by_index(source_dir: str, destination_dir: str, index: int) -> None:
    """_summary_: Moves a file from the source directory to the destination directory based on the provided index.
    This function lists all files in the source directory, sorts them, and moves the file at the specified index
    to the destination directory. If the index is out of range, it raises an IndexError.
    If the source or destination directories do not exist or are not directories, it raises NotADirectoryError.
    If no files are found in the source directory, it raises FileNotFoundError.

    Args:
        source_dir (str):The source directory from which the file will be moved.
        destination_dir (str): The destination directory to which the file will be moved.
        index (int): The index of the file to be moved, starting from 0.

    Raises:
        NotADirectoryError: If the source or destination path is not a directory.
        FileNotFoundError: If no files are found in the source directory.
        IndexError: If the provided index is out of range of the files found in the source directory.


    """
    source_path = Path(source_dir)
    destination_path = Path(destination_dir)

    print(f"Source path: {source_path.resolve()}")
    print(f"Destination path: {destination_path.resolve()}")

    if not source_path.is_dir():
        raise NotADirectoryError(f"{source_path} is not a valid directory.")

    if not destination_path.is_dir():
        raise NotADirectoryError(f"{destination_path} is not a valid directory.")

    files = sorted([f for f in source_path.iterdir() if f.is_file()])
    print(f"Found {len(files)} file(s): {[f.name for f in files]}")

    if not files:
        raise FileNotFoundError(f"No files found in {source_path}.")

    if index < 0 or index >= len(files):
        raise IndexError(
            f"Index {index} is out of range. Only {len(files)} file(s) found."
        )

    file_to_move = files[index]
    new_file_path = destination_path / file_to_move.name

    file_to_move.rename(new_file_path)
    print(f"Moved '{file_to_move.name}' to '{new_file_path}'")


# Example usage:
if __name__ == "__main__":
    move_file_by_index("src/my_packages/img_to_read", "src/my_packages/images", 1)
# moves the first file in 'static' folder
