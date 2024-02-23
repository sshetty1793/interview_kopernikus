import cv2
import os

# {(2688, 1520, 3): 12, (640, 480, 3): 114, (1920, 1080, 3): 950, (10, 6, 3): 1, (1100, 619, 3): 1, (1200, 675, 3): 1, 'None': 1}

# (2688, 1520, 3): c10-1623871098865.png
# (640, 480, 3): c10-1623871124416.png
# (1920, 1080, 3): c20-1616768476276.png
# None: c21_2021_03_27__10_36_36.png
# (10, 6, 3): c21_2021_03_27__12_53_37.png
# (1100, 619, 3): c21_2021_04_27__12_04_38.png
# (1200, 675, 3): c21_2021_04_27__12_44_38.png


def main():
	dataset_path = "./dataset/"
	file_list = os.listdir(dataset_path)

	size_count = {}

	for filename in file_list:
		img_path = os.path.join(dataset_path, filename)
		try:
			img = cv2.imread(img_path)

			height, width, channel = img.shape
			size = (width, height, channel)
			if size in size_count:
				size_count[size] += 1
			else:
				size_count[size] = 1
				print(str(size) + ": " + filename)
		except Exception as e:
			print(f"Error processing {filename}: {e}")
			if "None" in size_count:
				size_count["None"] += 1
			else:
				size_count["None"] = 1
				print("None: " + filename)

	print(size_count)


if __name__ == "__main__":
    main()
