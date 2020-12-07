"""
Utility to visualize bounding box from txt file
"""
import imgaug
import os
def save_bounding_box(image_path, box_path):
    output_name = image_path.split('.')[0] + '_viz' + '.png'
    with open(box_path) as f:
        coords = f.readline()
        coords = coords.replace('\n',"")
    x, y, width, height = coords.split(',')
    x_min = int(x)
    y_min = int(y)
    x_max = x_min+int(width)
    y_max = y_min+int(height)
    image = cv2.imread(image_path)
    box_image = cv2.rectangle(image, (x_min,y_min), (x_max,y_max), (0,255,0), 2)
    cv2.imwrite(output_name, box_image)

if __name__ == "__main__":
    OUTPUT_DIR = 'output/'
    bounding_boxes = os.listdir(OUTPUT_DIR)
    image_paths = os.listdir(OUTPUT_DIR)
    image_paths = [OUTPUT_DIR+i for i in image_paths if not ".txt" in i and not "_viz" in i]
    bounding_boxes = [OUTPUT_DIR+i for i in bounding_boxes if not ".png" in i]
    print(len(image_paths))
    print(len(bounding_boxes))

    for k in range(len(image_paths)):
        save_bounding_box(image_paths[k], bounding_boxes[k])