import bpy
import random
import os
from math import radians
import time

context = bpy.context

def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

def camera_view_bounds_2d(scene, camera_object, mesh_object):
    """
    Returns camera space bounding box of mesh object.

    Negative 'z' value means the point is behind the camera.

    Takes shift-x/y, lens angle and sensor size into account
    as well as perspective/ortho projections.

    :arg scene: Scene to use for frame size.
    :type scene: :class:`bpy.types.Scene`
    :arg obj: Camera object.
    :type obj: :class:`bpy.types.Object`
    :arg me: Untransformed Mesh.
    :type me: :class:`bpy.types.Mesh´
    :return: a Box object (call its to_tuple() method to get x, y, width and height)
    :rtype: :class:`Box`
    """

    mat = camera_object.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = mesh_object.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(mesh_object.matrix_world)
    me.transform(mat)

    camera = camera_object.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    # Sanity check
    if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
        return (0, 0, 0, 0)

    return (
        round(min_x * dim_x),            # X top left
        round(dim_y - max_y * dim_y),    # Y top left 
        round((max_x - min_x) * dim_x),  # Width
        round((max_y - min_y) * dim_y)   # Height
    )

def add_object(file_path): 
    """
    Filename must equal the object name
    """
    # file_path="/Users/alihasson/Documents/UIUC/CS445/Sythetic-Data-Generation/" + file_path.split('/')[-1].split('.')[0]
    inner_path = "Object"
    object_name = file_path.split('/')[-1].split('.')[0]

    bpy.ops.wm.append(
        filepath=os.path.join(file_path, inner_path, object_name),
        directory=os.path.join(file_path, inner_path),
        filename=object_name
    )
    return object_name
    
def place_camera_and_light():
    """Place the camera and light for first time setup"""
    # Place Camera
    bpy.context.scene.use_nodes = True
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



def setup_background_image(image_path):
    """Put the background image into the scene so that it can be rendered"""
    tree = bpy.context.scene.node_tree

    for node in tree.nodes:
        tree.nodes.remove(node)

    bpy.context.scene.render.film_transparent = True

    # Create the composite nodes
    img = bpy.data.images.load(image_path)
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

def move_object(object_name):
    """Move the object randomly"""
    # Select objects that will be rendered

    # bpy.ops.view3d.camera_to_view_selected()
    #bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    #bpy.ops.transform.rotate(value=-1.51653, orient_axis='Z', orient_type='VIEW', orient_matrix=((0.0593085, -0.99824, -2.32214e-06), (0.0278697, 0.00165364, 0.99961), (-0.997851, -0.0592853, 0.0279188)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    
    # resets object location to origin
    previous_context = bpy.context.area.type
    bpy.context.area.type = 'VIEW_3D'

    bpy.ops.view3d.snap_cursor_to_center()
    bpy.data.objects[object_name].select_set(True)
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)

    bpy.context.area.type = previous_context

    # randomly translate coords
    random_coord = random.uniform(-2.0,2.1)
    bpy.ops.transform.translate(value=(random_coord,20+random_coord,0))
    return random_coord

def render_image(file_path, object_name):
    """Render the scene to a file"""
    context.scene.render.filepath = file_path
    bpy.ops.render.render(write_still = True)

    coords = camera_view_bounds_2d(context.scene, context.scene.camera, bpy.data.objects[object_name])
    with open(file_path.replace(".png",".txt"),'w+') as f:
        for i,coord in enumerate(coords):
            f.write(str(coord))
            if(i!=3):
                f.write(',')
    

def save_bounding_box_viz(image_path, coords):
    """Save the visualized bounding box image to file"""
    x, y, width, height = coords
    x_min = x
    y_min = y
    x_max = x+width
    y_max = y+height
    image = cv2.imread(image_path)
    box_image = cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,255,0),2)
    cv2.imwrite("blender_image_visualized.png", box_image)


def cleanup():
    """ 
    The file should be blank from the start
    Blank out the blender file.
    """

    # Deselect all
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    pass

if __name__ == "__main__":
    cleanup()
    # save_bounding_box(image_path, (611, 190, 697, 724))
    # camera_view_bounds_2d(context.scene, context.scene.camera, bpy.data.objects['Cube'])
    background_dir = "Backgrounds/"
    model_dir = "Models/"
    number_of_moves = 10
    total_image_counter = 0

    abs_path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
    abs_path = abs_path.split('/')
    abs_path.pop()
    abs_path = '/'.join(abs_path)

    model_dir = abs_path + '/' + model_dir
    background_dir = abs_path + '/' + background_dir

    model_files_list = os.listdir(model_dir)
    background_images_list = os.listdir(background_dir)
    place_camera_and_light()
    print(model_files_list,background_images_list)
    
    for model_file in model_files_list:
        object_name = add_object(model_dir + '/' + model_file)
        for background_file in background_images_list:
            setup_background_image(background_dir + '/' + background_file)
            for i in range(number_of_moves):
                move_object(object_name)
                # time.sleep(1)
                render_image(abs_path + '/' + "test" + str(total_image_counter) + ".png", object_name)
                print(total_image_counter)
                total_image_counter+=1

        

    cleanup()
    print(f"DataSet of {total_image_counter} images Generated to {abs_path}")