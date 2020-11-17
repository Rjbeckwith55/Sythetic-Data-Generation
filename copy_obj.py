import bpy
from math import radians
import os
#https://unsplash.com/s/photos/road
bpy.context.scene.use_nodes = True

file_path="/Users/alihasson/Documents/UIUC/CS445/Sythetic-Data-Generation/test1.blend"
inner_path = "Object"
object_name = "Cube"

bpy.ops.wm.append(
    filepath=os.path.join(file_path, inner_path, object_name),
    directory=os.path.join(file_path, inner_path),
    filename=object_name
    )

# Render Scene
bpy.context.scene.render.filepath = "/Users/alihasson/Documents/UIUC/CS445/Sythetic-Data-Generation/render-testcopy.jpg"
bpy.ops.render.render(write_still = True)