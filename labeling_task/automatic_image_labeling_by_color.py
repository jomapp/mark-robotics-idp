from PIL import Image
import glob
import json

LOWER_TRESHOLD_COLOR = 160
MIN_POINTS_X_DISTANCE = 250
MAX_POINTS_X_DISTANCE = 375
MAX_X_DISTANCE_TO_LAST_X = 40
COLOR_RANGE_RGBA = range(LOWER_TRESHOLD_COLOR+20, 255), range(LOWER_TRESHOLD_COLOR, 255), range(LOWER_TRESHOLD_COLOR, 255)

def mean_sliding_window(array, initial_x, initial_y, width, height, window_range, previous_in_range):
    pixel_window_count = 0
    mean_red, mean_green, mean_blue = 0, 0, 0
    y_range = range(initial_y-window_range, initial_y+window_range)
    x_range = range(initial_x-window_range,
                    initial_x) if previous_in_range else range(initial_x, initial_x+window_range)
    for y in y_range:
        for x in x_range:
            if y > height-1 or y < 0:
                continue
            if x > width-1 or x < 0:
                continue
            red, green, blue = array[x, y]
            mean_red += red
            mean_green += green
            mean_blue += blue
            pixel_window_count += 1

    if pixel_window_count == 0:
        pixel_window_count = 1

    return mean_red/pixel_window_count, mean_green/pixel_window_count, mean_blue/pixel_window_count


def write_to_json_file(polygon_points, filepath):
    file = open(filepath)
    data = json.load(file)
    file.close()

    with open(filepath, 'w') as outfile:
        data['shapes'][0]['points'] = polygon_points
        json.dump(data, outfile)
        outfile.close()


def run_labeling_by_color_for_image(file_name):
    img_path = file_name
    json_path = file_name[:-4] + ".json"

    img = Image.open(img_path)
    pixel_array = img.load()
    img_w, img_h = img.size

    red_range, green_range, blue_range = COLOR_RANGE_RGBA
    previous_pixel_in_range = False

    polygon_points_up = []
    polygon_points_down = []
    last_added_pixel_index = (img_w, img_h)

    # iterate through image pixel by pixel bottom up
    for y in range(img_h, 0, -50):
        for x in range(0, img_w, 1):
            last_x, last_y = last_added_pixel_index
            max_points_x_distance = MAX_POINTS_X_DISTANCE * y/img_h
            min_points_x_distance = MIN_POINTS_X_DISTANCE * y/img_h
            max_x_distance_to_last_x = MAX_X_DISTANCE_TO_LAST_X * y/img_h

            pixel_red, pixel_green, pixel_blue = mean_sliding_window(
                pixel_array, x, y, img_w, img_h, 3, previous_pixel_in_range)
            #print("Colors: ", pixel_red, pixel_green, pixel_blue)

            if pixel_red in red_range and pixel_green in green_range and pixel_blue in blue_range and previous_pixel_in_range == False:
                if len(polygon_points_up) > 0 and not polygon_points_up[-1][0] >= float(x) - max_x_distance_to_last_x:
                    x = x - max_x_distance_to_last_x
                polygon_points_up.append([float(x), float(y)])
                last_added_pixel_index = (x,y)
                previous_pixel_in_range = True
            elif not(pixel_red in red_range and pixel_green in green_range and pixel_blue in blue_range) and previous_pixel_in_range and last_y == y and x >= last_x + min_points_x_distance:
                polygon_points_down.append([float(x), float(y)])
                last_added_pixel_index = (x,y)
                previous_pixel_in_range = False
                break
            elif last_y == y and last_x + min_points_x_distance <= x <= last_x + max_points_x_distance:
                polygon_points_down.append([float(x), float(y)])
                last_added_pixel_index = (x,y)
                previous_pixel_in_range = False
                break

        if y < 0.05 * img_h:
            break

    polygon_points = polygon_points_up
    for elm in reversed(polygon_points_down):
        polygon_points.append(elm)

    print("Points: ", polygon_points)
    write_to_json_file(polygon_points, json_path)

    print("Done! ✅")

IMAGES_PATH = "extracted_images/"
images_names = [image for image in glob.glob(IMAGES_PATH + "*.jpg")]

for image in images_names:
    run_labeling_by_color_for_image(image)
