import cv2
import os
import imutils
import random
import numpy as np


def draw_color_mask(img, borders, color=(0, 0, 0)):
    h = img.shape[0]
    w = img.shape[1]

    x_min = int(borders[0] * w / 100)
    x_max = w - int(borders[2] * w / 100)
    y_min = int(borders[1] * h / 100)
    y_max = h - int(borders[3] * h / 100)

    img = cv2.rectangle(img, (0, 0), (x_min, h), color, -1)
    img = cv2.rectangle(img, (0, 0), (w, y_min), color, -1)
    img = cv2.rectangle(img, (x_max, 0), (w, h), color, -1)
    img = cv2.rectangle(img, (0, y_max), (w, h), color, -1)

    return img


def preprocess_image_change_detection(img, gaussian_blur_radius_list=None, black_mask=(5, 10, 5, 0)):
    gray = img.copy()
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    if gaussian_blur_radius_list is not None:
        for radius in gaussian_blur_radius_list:
            gray = cv2.GaussianBlur(gray, (radius, radius), 0)

    gray = draw_color_mask(gray, black_mask)

    return gray


def compare_frames_change_detection(prev_frame, next_frame, min_contour_area):
    frame_delta = cv2.absdiff(prev_frame, next_frame)
    thresh = cv2.threshold(frame_delta, 45, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    score = 0
    res_cnts = []
    for c in cnts:
        if cv2.contourArea(c) < min_contour_area:
            continue

        res_cnts.append(c)
        score += cv2.contourArea(c)

    return score, res_cnts, thresh


def main():
	dataset_path = "./dataset/"
	file_list = os.listdir(dataset_path)

	for _ in range(1):
		random_index = random.randint(0, len(file_list) - 1)
		
		# Choose one file and its immediately following file
		# img_file1 = file_list[random_index]
		# img_file2 = file_list[random_index + 1]

		img_file1 = "c10-1623871098865.png"
		img_file2 = "c10-1623871124416.png"

		# Read the images
		img_path1 = os.path.join(dataset_path, img_file1)
		img_path2 = os.path.join(dataset_path, img_file2)
    
		try:
			img1 = cv2.imread(img_path1)
			img2 = cv2.imread(img_path2)

			img1 = cv2.resize(img1, (480, 270))
			img2 = cv2.resize(img2, (480, 270))

			

			img1 = preprocess_image_change_detection(img1, gaussian_blur_radius_list=[7])
			img2 = preprocess_image_change_detection(img2, gaussian_blur_radius_list=[7])

			cv2.imshow("Image 1", img1)
			cv2.imshow("Image 2", img2)

			score, contours, thresh = compare_frames_change_detection(img1, img2, min_contour_area=0)

			# contour_img = np.zeros_like(thresh)

			# Draw contours on the blank image
			thresh = cv2.drawContours(thresh, contours, -1, (0, 255, 0), 2)

			# Display the image with contours
			cv2.imshow("Contour with Gaussian Blur", thresh)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		except Exception as e:
			print(f"Error processing: {e}")



if __name__ == "__main__":
    main()
