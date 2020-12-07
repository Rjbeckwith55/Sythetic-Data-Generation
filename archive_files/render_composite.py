import bpy
from math import radians

# Place Camera
camera = bpy.data.cameras.new("Camera")
camera_obj = bpy.data.objects.new("Camera", camera)
camera_obj.location = (0,0,0)
camera_obj.rotation_euler = (radians(90),0,0)
bpy.context.scene.camera = camera_obj
bpy.context.scene.collection.objects.link(camera_obj)


tree = bpy.context.scene.node_tree
# clear default nodes
for node in tree.nodes:
    tree.nodes.remove(node)

bpy.context.scene.render.film_transparent = True


file_path = "H:/Downloads/empty_road2.jpg"
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
#bpy.context.scene.render.filepath = 'H:/Downloads/test_render.jpg'
#bpy.ops.render.render(write_still = True)