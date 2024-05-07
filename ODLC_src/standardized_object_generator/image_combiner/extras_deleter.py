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

target_directory = "/data03/home/jestrada2/synthetic_data_collection/unc_dataset/images"
target_labels = "/data03/home/jestrada2/synthetic_data_collection/unc_dataset/labels"

match_list = []
for pattern in regex_patterns:
    reg = re.compile(pattern)
    todos = os.listdir(target_directory)
    matched = [file for file in todos if reg.match(file)]
    match_list.append(len(matched))

min_matched = min(match_list)

# Iterate through each regex pattern
for pattern in regex_patterns:
    # Compile the regex pattern
    regex = re.compile(pattern)

    # Get a list of all files in the current directory
    all_files = os.listdir(target_directory)
    print(len(all_files))

    # Filter files matching the regex pattern
    matching_files = [file for file in all_files if regex.match(file)]

    print(f"Matched: {len(matching_files)} {pattern}'s")

    # Move the files to the target directory
    for i in range(len(matching_files) - min_matched):
        file_name = matching_files[i]
        os.remove(os.path.join(target_directory, file_name))

        file_name = file_name.replace("png", "txt")
        os.remove(os.path.join(target_labels, file_name))

print("All files moved successfully!")
print(f"min is {min_matched}")
