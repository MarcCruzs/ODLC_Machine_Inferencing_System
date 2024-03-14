import os
import random
import shutil

images_folder = '/data03/home/jestrada2/synthetic_data_collection/combined_images/images'
labels_folder = '/data03/home/jestrada2/synthetic_data_collection/combined_images/labels'
output_folder = '/data03/home/jestrada2/synthetic_data_collection/organized_dataset'

train_folder = os.path.join(output_folder, 'train')
val_folder = os.path.join(output_folder, 'val')
test_folder = os.path.join(output_folder, 'test')

os.makedirs(train_folder, exist_ok=True)
os.makedirs(val_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

folders = [train_folder, val_folder, test_folder]

for folder in folders:
    os.makedirs(os.path.join(folder, 'images'), exist_ok=True)
    os.makedirs(os.path.join(folder, 'labels'), exist_ok=True) 

# Get a list of all the image files
image_files = os.listdir(images_folder)
random.shuffle(image_files)

# Split the files into train, validation, and test sets
num_files = len(image_files)
train_files = image_files[:int(num_files * 0.7)]
val_files = image_files[int(num_files * 0.7):int(num_files * 0.9)]
test_files = image_files[int(num_files * 0.9):]

# Move the image and label files to the appropriate directories
for file in train_files:
    basename = os.path.splitext(file)[0]
    print(basename)
    image_file = os.path.join(images_folder, file)
    label_file = os.path.join(labels_folder, basename + '.txt')
    if os.path.isfile(label_file):
        shutil.copy(image_file, os.path.join(train_folder, 'images', file))
        shutil.copy(label_file, os.path.join(train_folder, 'labels', basename + '.txt'))

for file in val_files:
    basename = os.path.splitext(file)[0]
    image_file = os.path.join(images_folder, file)
    label_file = os.path.join(labels_folder, basename + '.txt')
    if os.path.isfile(label_file):
        shutil.copy(image_file, os.path.join(val_folder, 'images', file))
        shutil.copy(label_file, os.path.join(val_folder, 'labels', basename + '.txt'))

for file in test_files:
    basename = os.path.splitext(file)[0]
    image_file = os.path.join(images_folder, file)
    label_file = os.path.join(labels_folder, basename + '.txt')
    if os.path.isfile(label_file):
        shutil.copy(image_file, os.path.join(test_folder, 'images', file))
        shutil.copy(label_file, os.path.join(test_folder, 'labels', basename + '.txt'))

# Shuffle the contents of each subdirectory
for root, dirs, files in os.walk(output_folder):
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        random.shuffle(os.listdir(dir_path))
