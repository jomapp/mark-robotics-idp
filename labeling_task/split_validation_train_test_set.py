import os
import random
import shutil

def split_data(source_folder, train_folder, val_folder, test_folder, split_ratio=(0.7, 0.15, 0.15)):
    # Get a list of all file pairs in the source folder
    file_pairs = [(f, f.replace('.jpg', '.json')) for f in os.listdir(source_folder) if f.endswith('.jpg')]

    # Calculate the number of pairs for each split
    total_pairs = len(file_pairs)
    num_train = int(total_pairs * split_ratio[0])
    num_val = int(total_pairs * split_ratio[1])
    num_test = total_pairs - num_train - num_val

    # Randomly shuffle the file pairs
    random.shuffle(file_pairs)

    # Split the file pairs into train, val, and test sets
    train_pairs = file_pairs[:num_train]
    val_pairs = file_pairs[num_train:num_train+num_val]
    test_pairs = file_pairs[num_train+num_val:]

    # Copy files to their respective folders
    copy_pairs(train_pairs, source_folder, train_folder)
    copy_pairs(val_pairs, source_folder, val_folder)
    copy_pairs(test_pairs, source_folder, test_folder)

def copy_pairs(pair_list, source_folder, destination_folder):
    for jpg_file, json_file in pair_list:
        source_path_jpg = os.path.join(source_folder, jpg_file)
        source_path_json = os.path.join(source_folder, json_file)

        destination_path_jpg = os.path.join(destination_folder, jpg_file)
        destination_path_json = os.path.join(destination_folder, json_file)

        shutil.copyfile(source_path_jpg, destination_path_jpg)
        shutil.copyfile(source_path_json, destination_path_json)

if __name__ == "__main__":
    source_folder = "./images_final"
    train_folder = "./dataset/train"
    val_folder = "./dataset/val"
    test_folder = "./dataset/test"

    # Create destination folders if they don't exist
    for folder in [train_folder, val_folder, test_folder]:
        os.makedirs(folder, exist_ok=True)

    # Split the data
    split_data(source_folder, train_folder, val_folder, test_folder)