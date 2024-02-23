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
	img_path = "./dataset/c10-1623871098865.png"

	img = cv2.imread(img_path)

	cv2.imshow("Original Image", img)
	cv2.waitKey(0)

	img = cv2.resize(img, (480, 270))
	cv2.imshow("Resized Image", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == "__main__":
    main()