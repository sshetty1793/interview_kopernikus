import os

def get_unique_files(folder1, folder2):
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))
    
    unique_to_folder1 = files1 - files2
    unique_to_folder2 = files2 - files1
    
    return sorted(unique_to_folder1), sorted(unique_to_folder2)

def print_unique_files(folder1, folder2):
    unique_to_folder1, unique_to_folder2 = get_unique_files(folder1, folder2)
    
    print("Files unique to", folder1, ":\n")
    for unique in unique_to_folder1:
    	print(unique)
    print()
    print("\nFiles unique to", folder2, ":\n", unique_to_folder2)
    for unique in unique_to_folder2:
    	print(unique)

# Example usage:
folder1 = "./unique_images_200_3/"
folder2 = "./unique_images_200_5/"

print_unique_files(folder1, folder2)
