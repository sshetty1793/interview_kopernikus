import cv2
import imutils
import os

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
    target_size = (480, 270)
    dataset_path = "./dataset/"

    # Grid Search for various parameter values
    contour_areas = [0, 100, 200, 500, 1000, 2000]
    kernel_sizes = [None, 3, 5, 7]

    for min_contour_area in contour_areas:
        for kernel_size in kernel_sizes:

            output_path = "./processed_images_" + str(min_contour_area) + "_" + str(kernel_size) + "/"
            print(output_path)

            if not os.path.exists(output_path):
                os.makedirs(output_path)
            
            file_list = os.listdir(dataset_path)

            prev_frame = None
            for filename in file_list:
                img_path = os.path.join(dataset_path, filename)

                try:
                    img = cv2.imread(img_path)
                    img = cv2.resize(img, target_size)  # Resize the image to a common size

                    if prev_frame is None:
                        prev_frame = preprocess_image_change_detection(img, gaussian_blur_radius_list=kernel_size if kernel_size is None else [kernel_size])
                        cv2.imwrite(os.path.join(output_path, filename), img)
                    else:
                        next_frame = preprocess_image_change_detection(img, gaussian_blur_radius_list=kernel_size if kernel_size is None else [kernel_size])
                        score, _, _ = compare_frames_change_detection(prev_frame, next_frame, min_contour_area=min_contour_area)

                        if score > 0:
                            cv2.imwrite(os.path.join(output_path, filename), img)

                        prev_frame = next_frame

                except Exception as e:
                    print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    main()