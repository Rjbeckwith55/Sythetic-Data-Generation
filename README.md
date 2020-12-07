# Sythetic-Data-Generation

This project has a gitsubmodule to for seam-carving make sure to clone the submodule properly if you would like to resize your backgroud images

## Instructions
generateDataset.blend is an empty project to run the script in.

Populate the Backgrounds/ and Models/ directory with your own assets or use the provided example assets.

The models within the Models/ directory must have the same object name as the file itself.

The background images must all be the same size. 600 x 600. If they are not we provide the utility resize_images.py to make all the images the same size. If usint this utility make sure SHOULD_DOWNSIZE = False is set in the seam_carving.py file. This resizing method will take a long time to run.
  
Open generateDataset.blend in Blender

Run the generateDataset.py from Blender using the scripting tab in the generateDataset.blend project.

After running the script, see results in the output/ directory.

To visualize the results of the bounding boxes run display_image.py

## Sources

https://github.com/andrewdcampbell/seam-carving

https://blender.stackexchange.com/questions/7198/save-the-2d-bounding-box-of-an-object-in-rendered-image-to-a-text-file

Image Credit:
https://libreshot.com/wp-content/uploads/2019/12/foggy-road.jpg
https://libreshot.com/wp-content/uploads/2018/12/road.jpg
https://upload.wikimedia.org/wikipedia/commons/b/bb/Silaanyo_road%2C_habarjeclo_Road..jpg
https://upload.wikimedia.org/wikipedia/commons/6/6b/Road_in_Norway.jpg

