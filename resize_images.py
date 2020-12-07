"""Utility reads the Backgrounds/ directory and resizes them to be the set size of 600 x 600 expected from the tool"""
import subprocess
import os
import cv2
import seam_carving.seam_carving as sc

DEFAULT_DIM = 600

def do_seam_carving(resized, img_path):
    h, w, _ = resized.shape
    if(h != DEFAULT_DIM and w!=DEFAULT_DIM):
        return
    elif(w > h and h == DEFAULT_DIM):
        dy = 0
        dx = int(h-w)
    elif(h > w and w == DEFAULT_DIM):
        dy = int(w-h)
        dx = 0
    else:
        print("Should not have gotten here")
    
    assert dy is not None and dx is not None
    output = sc.seam_carve(resized, dy, dx, None, True)
    cv2.imwrite(img_path, output)


if __name__ == "__main__": 
    background_dir = "Backgrounds/"
    background_image_list = os.listdir(background_dir)
    for back_image_path in background_image_list:
        img_path = background_dir + back_image_path
        image = cv2.imread(img_path)
        h, w, _ = image.shape
        print(w,h)
        if(w == DEFAULT_DIM and h == DEFAULT_DIM):
            continue
        elif(w > DEFAULT_DIM or h > DEFAULT_DIM):
            if w == h: # Image is square already
                new_h = DEFAULT_DIM
                new_w = DEFAULT_DIM
            elif w > h:
                new_h = DEFAULT_DIM
                new_w = int((w/float(h)) * DEFAULT_DIM)
            else:
                new_w = DEFAULT_DIM
                new_h = int((h/float(w)) * DEFAULT_DIM)
            resized = cv2.resize(image,(new_w,new_h))
            cv2.imwrite(img_path, resized)
            print(f"Initial Resize of image to: {new_w}x{new_h}")
            do_seam_carving(resized,img_path)

        elif(w < DEFAULT_DIM or h < DEFAULT_DIM):
            resized = cv2.resize(image,(DEFAULT_DIM,DEFAULT_DIM))

