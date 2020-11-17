import bpy
from math import radians
#https://unsplash.com/s/photos/road
bpy.context.scene.use_nodes = True
# Place Camera
camera = bpy.data.cameras.new("Camera")
camera_obj = bpy.data.objects.new("Camera", camera)
camera_obj.location = (0,0,0)
camera_obj.rotation_euler = (radians(90),0,0)
bpy.context.scene.camera = camera_obj
bpy.context.scene.collection.objects.link(camera_obj)


# create light datablock, set attributes
light_data = bpy.data.lights.new(name="light_2.80", type='POINT')
light_data.energy = 30

# create new object with our light datablock
light_object = bpy.data.objects.new(name="light_2.80", object_data=light_data)

# link light object
bpy.context.collection.objects.link(light_object)

# make it active 
bpy.context.view_layer.objects.active = light_object

#change location
light_object.location = (0, -0.5, 0)

print(type(bpy.context.scene))
tree = bpy.context.scene.node_tree
# clear default nodes
for node in tree.nodes:
   tree.nodes.remove(node)

bpy.context.scene.render.film_transparent = True


file_path = "/Users/alihasson/Documents/UIUC/CS445/Sythetic-Data-Generation/background.jpg"
img = bpy.data.images.load(file_path)
image_node = tree.nodes.new("CompositorNodeImage")
image_node.image = img
image_node.location = 0,0

render_layers = tree.nodes.new("CompositorNodeRLayers")
render_layers.location = 150,-250

alpha_over = tree.nodes.new("CompositorNodeAlphaOver")
alpha_over.location = 400,0

composite = tree.nodes.new("CompositorNodeComposite")
composite.location = 600,0


# Link the composite tree
links = tree.links
link = links.new(image_node.outputs[0], alpha_over.inputs[1])
link2 = links.new(render_layers.outputs[0], alpha_over.inputs[2])
link3 = links.new(alpha_over.outputs[0], composite.inputs[0])

# Render Scene
bpy.context.scene.render.filepath = "/Users/alihasson/Documents/UIUC/CS445/Sythetic-Data-Generation/render-test.jpg"
bpy.ops.render.render(write_still = True)