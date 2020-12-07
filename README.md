# Sythetic-Data-Generation

generateDataset.blend is an empty project to run the script in.

## Instructions
Populate the Backgrounds/ and Models/ directory with your own assets.

The Models must have the same object name as the File itself.

The background images must all be the same size. 600 x 600. 

We provide the utility resize_images.py to make all the images the same size.

The SHOULD_DOWNSIZE = False must be set in the seam_carving.py file

This utility uses seam carving to resize the images. (It taks a long time to run)
  
Open generateDataset.blend in Blender

Run the generateDataset.py from Blender.

## Sources

https://blender.stackexchange.com/questions/7198/save-the-2d-bounding-box-of-an-object-in-rendered-image-to-a-text-file
