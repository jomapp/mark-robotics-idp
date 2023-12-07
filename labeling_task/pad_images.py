import cv2
import glob
import numpy as np

path = r'./images_final/*.jpg'
imagePaths = glob.glob(path)

for imagePath in imagePaths:
    # read image
    img = cv2.imread(imagePath)
    old_image_height, old_image_width, channels = img.shape

    # create new image of desired size and color (blue) for padding
    new_image_width = 1080+20
    new_image_height = 1920+20
    color = (255,0,0)
    result = np.full((new_image_height,new_image_width, channels), color, dtype=np.uint8)

    # compute center offset
    x_center = (new_image_width - old_image_width) // 2
    y_center = (new_image_height - old_image_height) // 2

    # copy img image into center of result image
    result[y_center:y_center+old_image_height, 
        x_center:x_center+old_image_width] = img

    # save result
    cv2.imwrite(imagePath, result)