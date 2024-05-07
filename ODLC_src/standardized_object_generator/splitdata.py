import os
import re
import shutil

# Define your list of 8 regex patterns
regex_patterns = [
    ".+_circle.+",
    ".+rectangle.+",
    ".+cross.+",
    ".+star.+",
    ".+triangle.+",
    ".+pentagon.+",
    ".+semicircle.+",
    ".+quartercircle.+",
]

target_directory = "/data03/home/jestrada2/synthetic_data_collection/solidbg_dataset"

# Iterate through each regex pattern
for pattern in regex_patterns:
    # Compile the regex pattern
    regex = re.compile(pattern)

    # Get a list of all files in the current directory
    current_directory = (
        "/data03/home/jestrada2/synthetic_data_collection/unc_dataset/images"
    )
    label_directory = (
        "/data03/home/jestrada2/synthetic_data_collection/unc_dataset/labels"
    )
    all_files = os.listdir(current_directory)
    print(len(all_files))

    # Filter files matching the regex pattern
    matching_files = [file for file in all_files if regex.match(file)]

    print(f"Matched: {len(matching_files)} {pattern}'s")

    # Limit the number of files to move (31500 in your case)
    num_matched = len(matching_files)
    train_num = int(num_matched * 0.7)
    test_num = int(num_matched * 0.1)
    val_num = int(num_matched * 0.2)

    # move to train
    for i in range(train_num):
        curr_file = matching_files[i]
        source_img = os.path.join(current_directory, curr_file)
        source_label = os.path.join(label_directory, curr_file.replace(".png", ".txt"))

        dest_img = os.path.join(target_directory, "train", "images", curr_file)
        dest_label = os.path.join(
            target_directory, "train", "labels", curr_file.replace(".png", ".txt")
        )
        shutil.move(source_img, dest_img)
        shutil.move(source_label, dest_label)

    # move to test
    for i in range(train_num, train_num + test_num):
        curr_file = matching_files[i]
        source_img = os.path.join(current_directory, curr_file)
        source_label = os.path.join(label_directory, curr_file.replace(".png", ".txt"))

        dest_img = os.path.join(target_directory, "test", "images", curr_file)
        dest_label = os.path.join(
            target_directory, "test", "labels", curr_file.replace(".png", ".txt")
        )
        shutil.move(source_img, dest_img)
        shutil.move(source_label, dest_label)

    # move to val
    for i in range(train_num + test_num, train_num + test_num + val_num):
        curr_file = matching_files[i]
        source_img = os.path.join(current_directory, curr_file)
        source_label = os.path.join(label_directory, curr_file.replace(".png", ".txt"))

        dest_img = os.path.join(target_directory, "val", "images", curr_file)
        dest_label = os.path.join(
            target_directory, "val", "labels", curr_file.replace(".png", ".txt")
        )
        shutil.move(source_img, dest_img)
        shutil.move(source_label, dest_label)

print("All files moved successfully!")
