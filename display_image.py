import cv2
def display_bounding_box(image_path, coords):
    x, y, width, height = coords
    x_min = x
    y_min = y
    x_max = x+width
    y_max = y+height
    image = cv2.imread(image_path)
    box_image = cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,255,0),2)
    cv2.imwrite("out.png",box_image)

if __name__ == "__main__":
    image_path = 'untitled.png'
    display_bounding_box(image_path, (611, 190, 697, 724))