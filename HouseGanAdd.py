import os
import webbrowser
import bpy
import json
import math
import subprocess

bl_info = {
    "name": "House-GAN++Addon",
    "blender": (4, 0, 2),
    "category": "Object",
}

# Property Group for storing addon properties
class MyProperties(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Choose a file path",
        subtype='FILE_PATH'
    )
    level: bpy.props.IntProperty(
        name="Level",
        description="Level of the generated model",
        default=0,
        min=0,
        max=9
    )
    json_file_path: bpy.props.StringProperty(
        name="JSON File Path",
        description="Path to the JSON file",
        subtype='FILE_PATH'
    )
    use_color: bpy.props.BoolProperty(
        name="Color",
        description="Use color for objects",
        default=True
    )
    floor_height: bpy.props.FloatProperty(
        name="Floor Height",
        default=0.3,
        min=0.1,
        max=5.0,
        description="Height of the floor"
    )
    wall_thickness: bpy.props.FloatProperty(
        name="Wall Thickness",
        default=0.5,
        min=0.1,
        max=2,
        description="Thickness of the walls"
    )
    wall_height: bpy.props.FloatProperty(
        name="Wall Height",
        default=35.0,
        min=30.0,
        max=100.0,
        description="Height of the walls"
    )
    door_height: bpy.props.FloatProperty(
        name="Door height",
        default=25,
        description="Height of the door"
    )
    roof_height: bpy.props.FloatProperty(
        name="Roof height",
        default=0.3,
        min=0.1,
        max=5.0,
        description="Thickness of the roof"
    )


# Panel for open House-GAN++
class HouseGanPanel(bpy.types.Panel):
    bl_label = "House-GAN++"
    bl_idname = "PT_HouseGanPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'House-GAN++Addon'

    def draw(self, context):
        layout = self.layout
        # Button to run Python code and open the browser
        layout.operator("object.open_operator", text="Open House-GAN++")

# Panel for the SVG to JSON conversion
class ConverterPanel(bpy.types.Panel):
    bl_label = "Converter"
    bl_idname = "PT_ConverterPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'House-GAN++Addon'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.load_svg_operator", text="Load SVG")

        # Display the name of the loaded SVG file
        svg_file_path = context.scene.svg_file_path
        if svg_file_path:
            layout.label(text="Loaded SVG:")
            box = layout.box()
            box.label(text=bpy.path.basename(svg_file_path))

        layout.operator("object.convert_to_json_operator", text="Convert to JSON")

# Panel for managing data
class DataPanel(bpy.types.Panel):
    bl_label = "Data"
    bl_idname = "PT_DataPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'House-GAN++Addon'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.load_json_operator", text="Load JSON")

        # Logic to display the name of the loaded JSON file
        json_filepath = context.scene.json_file_path

        if json_filepath:
            layout.label(text="Loaded JSON:")
            box = layout.box()
            box.label(text=bpy.path.basename(json_filepath))

# Panel for managing floor parameters
class FloorPanel(bpy.types.Panel):
    bl_label = "Floor"
    bl_idname = "PT_FloorPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'House-GAN++Addon'

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene.my_tool, "floor_height", text="Floor Height")
        layout.operator("object.generate_shapes_operator", text="Generate")


# Panel for managing wall parameters
class WallsPanel(bpy.types.Panel):
    bl_label = "Walls"
    bl_idname = "PT_WallsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'House-GAN++Addon'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.my_tool, "wall_height", text="Wall Height")
        layout.prop(context.scene.my_tool, "wall_thickness", text="Wall Thickness")
        layout.operator("object.generate_walls_operator", text="Generate Walls")
        layout.operator("object.generate_doors_operator", text="Generate Doors")

# Panel for managing roof parameters
class RoofPanel(bpy.types.Panel):
    bl_label = "Roof"
    bl_idname = "PT_RoofPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'House-GAN++Addon'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.my_tool, "roof_height", text="Roof Height")
        layout.operator("object.generate_roof_operator", text="Generate Roof")

# Panel for final generation options
class GeneratePanel(bpy.types.Panel):
    bl_label = "Generate"
    bl_idname = "PT_GeneratePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'House-GAN++Addon'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.my_tool, "level", text="Level")
        layout.operator("object.generate_all_operator", text="Generate Level")
        layout.prop(context.scene.my_tool, "use_color", text="Use Color")
        layout.operator("object.save_generated_object_operator", text="Save Generated Object")
def add_material(obj, hex_color):
    # Convert hexadecimal color to RGB values in the range [0, 1]
    color = [float(value) / 255.0 for value in bytes.fromhex(hex_color[1:])] + [1.0]

    # Create a new material
    material = bpy.data.materials.new(name=f"Material_{obj.name}")

    # Disable shader nodes for simplicity
    material.use_nodes = False

    # Set the diffuse color of the material
    material.diffuse_color = color

    # Append the material to the object's data
    obj.data.materials.append(material)

def process_shape_data(shape_data):
    # Processing vertex data
    vertices = [tuple(map(float, point)) for point in shape_data.get("points", [])]

    # Ensure each vertex has three coordinates (x, y, z=0.0)
    vertices = [(v[0], v[1], 0.0) for v in vertices]

    # Processing edge data
    edges = [(i, (i + 1) % len(vertices)) for i in range(len(vertices))]

    # Processing face data
    faces = [tuple(range(len(vertices)))] if len(vertices) >= 3 else []

    return vertices, edges, faces

# Operator for loading an SVG file
class OBJECT_OT_LoadSVGOperator(bpy.types.Operator):
    bl_label = "Load SVG File"
    bl_idname = "object.load_svg_operator"
    # Set the home directory and SVG directory
    home_directory = os.path.expanduser("~")
    svg_directory = os.path.join(home_directory, "Blender", "svg")

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Choose a file path",
        subtype='FILE_PATH',
        default=svg_directory
    )
    filter_glob: bpy.props.StringProperty(
        default="*.svg",
        options={'HIDDEN'}
    )
    def execute(self, context):
        # Set the loaded SVG file path
        context.scene.svg_file_path = self.filepath
        self.report({'INFO'}, f"SVG file loaded: {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        # Create the folder if it doesn't exist
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)

        # Open the file selection dialog
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Operator for converting SVG to JSON
class OBJECT_OT_ConvertToJSONOperator(bpy.types.Operator):
    bl_label = "Convert SVG to JSON"
    bl_idname = "object.convert_to_json_operator"

    # Path to the user's home directory
    home_directory = os.path.expanduser("~")
    # Full path to the SVG directory in the user's Blender
    svg_directory = os.path.join(home_directory, "Blender", "svg")
    json_directory = os.path.join(home_directory, "Blender", "json")
    # Path to the conversion script
    convert_script_path = os.path.join(home_directory, "Blender", "convertSVG.py")

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Choose a file path",
        subtype='FILE_PATH',
        default=svg_directory  # Set the default path
    )

    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'}
    )

    def execute(self, context):
        if not os.path.exists(self.json_directory):
            os.makedirs(self.json_directory)

        svg_file_path = context.scene.svg_file_path
        file_name = bpy.path.display_name_from_filepath(svg_file_path)
        # Full path to the output JSON file
        output_json_path = os.path.join(self.home_directory, "Blender", "json", f"{file_name}.json")

        # Check if the conversion script exists
        if os.path.exists(self.convert_script_path):
            # Run the conversion script
            subprocess.call(['python',
                             os.path.abspath(self.convert_script_path),
                             os.path.abspath(svg_file_path),
                             os.path.abspath(output_json_path)])
            self.report({'INFO'}, "Converted SVG to JSON")
        else:
            self.report({'ERROR'}, "Conversion script (convertSVG.py) not found!")

        return {'FINISHED'}


# Operator for loading a JSON file
class OBJECT_OT_LoadJSONOperator(bpy.types.Operator):
    bl_label = "Load JSON"
    bl_idname = "object.load_json_operator"

    home_directory = os.path.expanduser("~")
    json_directory = os.path.join(home_directory, "Blender", "json")

    # Set the default path for the operator
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Choose a file path",
        subtype='FILE_PATH',
        default=json_directory
    )
    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'}
    )

    def execute(self, context):
        # Save the file path to a global variable or scene property
        context.scene.json_file_path = self.filepath
        self.report({'INFO'}, f"JSON file loaded: {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Operator for opening a browser
class OBJECT_OT_OpenOperator(bpy.types.Operator):
    bl_label = "Open Browser"
    bl_idname = "object.open_operator"

    def execute(self, context):
        webbrowser.open("http://127.0.0.1:5000/")

        self.report({'INFO'}, "Opening browser")
        return {'FINISHED'}

class OBJECT_OT_GenerateShapesOperator(bpy.types.Operator):
    bl_label = "Generate Shapes"
    bl_idname = "object.generate_shapes_operator"

    def execute(self, context):
        json_file_path = bpy.path.abspath(context.scene.json_file_path)
        if not json_file_path:
            self.report({'ERROR'}, "No JSON file path provided")
            return {'CANCELLED'}
        try:
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        # Calculate the total height of the model, considering floor, wall, and roof heights
        floor_height = context.scene.my_tool.floor_height
        model_height = floor_height + context.scene.my_tool.wall_height + context.scene.my_tool.roof_height
        # Calculate the height at the current level based on the model height and the specified level
        level_height = model_height * context.scene.my_tool.level

        # Iterate through shape data from the JSON file
        for shape_data in json_data.get("shapes", []):
            # Process vertex data for the shape
            vertices, edges, faces = process_shape_data(shape_data)

            # Adjust the Z-coordinate of each vertex based on the level height
            for i in range(len(vertices)):
                vertices[i] = (vertices[i][0], vertices[i][1], vertices[i][2] + level_height)

            if shape_data.get("stroke", "").lower() != "none":
                self.create_floor(context, vertices, edges, faces, shape_data)
        return {'FINISHED'}

    def create_floor(self, context, vertices, edges, faces, shape_data):
        level = context.scene.my_tool.level

        if shape_data.get("stroke") == "grey" and level != 0:
            return

        # Create a new mesh with a unique name based on shape data and level
        mesh = bpy.data.meshes.new(name=f"FloorMesh_{shape_data.get('id')}_Level{level}")
        mesh.from_pydata(vertices, edges, faces)
        mesh.update()

        # Create a new object with a unique name based on shape data and level
        obj = bpy.data.objects.new(f"FloorObject_{shape_data.get('id')}_Level{level}", mesh)

        # Link the object to the collection, set it as the active object, and select it
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        if context.scene.my_tool.use_color:
            add_material(obj, shape_data['fill'])

        obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        obj.modifiers["Solidify"].thickness = context.scene.my_tool.floor_height

# Operator for generating walls based on JSON data
class OBJECT_OT_GenerateWallsOperator(bpy.types.Operator):
    bl_label = "Generate Walls"
    bl_idname = "object.generate_walls_operator"

    def execute(self, context):
        json_file_path = bpy.path.abspath(context.scene.json_file_path)
        if not json_file_path:
            self.report({'ERROR'}, "No JSON file path provided")
            return {'CANCELLED'}

        try:
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        wall_height = context.scene.my_tool.wall_height
        wall_thickness = context.scene.my_tool.wall_thickness
        adjusted_wall_height = context.scene.my_tool.door_height

        for shape_data in json_data.get("shapes", []):
            if shape_data.get("stroke", "").lower() == "black":
                self.generate_walls_for_shape(context, shape_data, wall_height, wall_thickness)
            elif shape_data.get("stroke", "").lower() == "grey":
                self.generate_walls_for_shape(context, shape_data, adjusted_wall_height, wall_thickness)

        self.report({'INFO'}, "Walls generated")
        return {'FINISHED'}

    def generate_walls_for_shape(self, context, shape_data, wall_height, wall_thickness, scale_factor=1.0):
        vertices = [tuple(map(float, point)) for point in shape_data.get("points", [])]

        edge_indices = range(len(vertices))

        for i in edge_indices:
            start = vertices[i]
            end = vertices[(i + 1) % len(vertices)]

            # Ensure scale factor is within valid range
            scale_factor = max(0.1, min(1.0, scale_factor))
            wall_thickness_scaled = wall_thickness * scale_factor

            if shape_data.get("stroke", "").lower() == "grey":
                if context.scene.my_tool.level != 0:
                    return

                adjusted_wall_height = wall_height + context.scene.my_tool.floor_height
                mid_point_z = adjusted_wall_height / 2
            else:
                adjusted_wall_height = wall_height
                mid_point_z = wall_height / 2 + context.scene.my_tool.floor_height

            self.create_wall(context, start, end, shape_data.get('id'), i,
                             shape_data.get('fill'), adjusted_wall_height, wall_thickness_scaled, mid_point_z)

    def create_wall(self, context, start, end, shape_id, index, fill_color, wall_height, wall_thickness, mid_point_z):
        level = context.scene.my_tool.level
        # Calculate the length of the wall
        wall_length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

        # Add a new cube object for the wall
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        wall_obj = context.active_object
        wall_obj.scale.x = wall_length / 2
        wall_obj.scale.y = wall_thickness / 2
        wall_obj.scale.z = wall_height / 2

        # Calculate the midpoint of the wall
        mid_point_x = (start[0] + end[0]) / 2
        mid_point_y = (start[1] + end[1]) / 2
        model_height = (context.scene.my_tool.floor_height + context.scene.my_tool.wall_height +
                        context.scene.my_tool.roof_height)
        mid_point_z += model_height * context.scene.my_tool.level

        # Calculate the orientation angle of the wall
        angle = math.atan2(end[1] - start[1], end[0] - start[0])

        # Offset the wall inward
        offset_x = math.sin(angle) * wall_thickness / 2
        offset_y = -math.cos(angle) * wall_thickness / 2
        wall_obj.location = (mid_point_x + offset_x, mid_point_y + offset_y, mid_point_z)
        wall_obj.rotation_euler[2] = angle

        # Assign a name and add material
        wall_obj.name = f"Wall_{shape_id}_{index}_Level{level}"
        if context.scene.my_tool.use_color:
            add_material(wall_obj, fill_color)

class OBJECT_OT_GenerateDoorsOperator(bpy.types.Operator):
    bl_label = "Generate Doors"
    bl_idname = "object.generate_doors_operator"

    def execute(self, context):
        json_file_path = bpy.path.abspath(context.scene.json_file_path)
        if not json_file_path:
            self.report({'ERROR'}, "No JSON file path provided")
            return {'CANCELLED'}
        try:
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        floor_height = context.scene.my_tool.floor_height
        level = context.scene.my_tool.level
        model_height = (context.scene.my_tool.floor_height + context.scene.my_tool.wall_height
                        + context.scene.my_tool.roof_height)

        for shape_data in json_data.get("shapes", []):
            vertices, edges, faces = process_shape_data(shape_data)

            for i in range(len(vertices)):
                # Adjust Z coordinate based on level
                vertices[i] = (vertices[i][0], vertices[i][1], vertices[i][2] + floor_height + model_height * level)

            if shape_data.get("stroke", "").lower() == "none":
                self.create_door(context, vertices, edges, faces, shape_data)

        return {'FINISHED'}

    def create_door(self, context, vertices, edges, faces, shape_data):
        level = context.scene.my_tool.level
        if shape_data.get("stroke") == "grey" and level != 0:
            return

        scale_factor_x = 0.65  # Scale factor for X axis
        scale_factor_y = 0.65  # Scale factor for Y axis
        center_x = sum(v[0] for v in vertices) / len(vertices)
        center_y = sum(v[1] for v in vertices) / len(vertices)

        # Scale vertices around the center
        scaled_vertices = [(center_x + (v[0] - center_x) * scale_factor_x,
                            center_y + (v[1] - center_y) * scale_factor_y,
                            v[2]) for v in vertices]

        mesh = bpy.data.meshes.new(name=f"DoorMesh_{shape_data.get('id')}_Level{level}")
        mesh.from_pydata(scaled_vertices, edges, faces)
        mesh.update()

        obj = bpy.data.objects.new(f"DoorObject_{shape_data.get('id')}_Level{level}", mesh)
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        if context.scene.my_tool.use_color:
            add_material(obj, shape_data['fill'])

        obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        obj.modifiers["Solidify"].thickness -= context.scene.my_tool.door_height


# Operator for generating roof based on JSON data
class OBJECT_OT_GenerateRoofOperator(bpy.types.Operator):
    bl_label = "Generate Roof"
    bl_idname = "object.generate_roof_operator"
    def execute(self, context):
        json_file_path = bpy.path.abspath(context.scene.json_file_path)
        if not json_file_path:
            self.report({'ERROR'}, "No JSON file path provided")
            return {'CANCELLED'}
        try:
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        wall_height = context.scene.my_tool.wall_height
        floor_height = context.scene.my_tool.floor_height
        level = context.scene.my_tool.level
        model_height = (context.scene.my_tool.floor_height + context.scene.my_tool.wall_height +
                        context.scene.my_tool.roof_height)

        for shape_data in json_data.get("shapes", []):
            vertices, edges, faces = process_shape_data(shape_data)
            for i in range(len(vertices)):
                if shape_data.get("stroke", "").lower() == "grey":
                    vertices[i] = (
                    vertices[i][0], vertices[i][1], vertices[i][2] + floor_height + context.scene.my_tool.door_height)
                else: vertices[i] = (vertices[i][0], vertices[i][1], vertices[i][2] +
                                     floor_height + wall_height + model_height * level)
            self.create_roof_object(context, vertices, edges, faces, shape_data)
        self.report({'INFO'}, "Roof generated")
        return {'FINISHED'}

    def create_roof_object(self, context, vertices, edges, faces, shape_data):

        level = context.scene.my_tool.level
        # Skip if stroke is "none"
        if shape_data.get("stroke") == "none":
            return

        if shape_data.get("stroke") == "grey" and level != 0:
            return

        # Create a new mesh
        mesh = bpy.data.meshes.new(name=f"DoorMesh_{shape_data.get('id')}_Level{level}")
        mesh.from_pydata(vertices, edges, faces)
        mesh.update()

        # Create a new object and link it to the collection
        obj = bpy.data.objects.new(f"DoorObject_{shape_data.get('id')}_Level{level}", mesh)
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        if context.scene.my_tool.use_color:
            add_material(obj, shape_data['fill'])

        obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        obj.modifiers["Solidify"].thickness = context.scene.my_tool.roof_height

# Operator for generating all components
class OBJECT_OT_GenerateAllOperator(bpy.types.Operator):
    bl_label = "Generate All"
    bl_idname = "object.generate_all_operator"

    def execute(self, context):

        json_file_path = bpy.path.abspath(context.scene.json_file_path)

        if not json_file_path:
            self.report({'ERROR'}, "No JSON file path provided")
            return {'CANCELLED'}

        # Call other operators to generate shapes, walls, roof, and doors
        bpy.ops.object.generate_shapes_operator()
        bpy.ops.object.generate_walls_operator()
        bpy.ops.object.generate_roof_operator()
        bpy.ops.object.generate_doors_operator()

        return {'FINISHED'}


# Operator for saving the generated object
class OBJECT_OT_SaveGeneratedObject(bpy.types.Operator):
    bl_label = "Save Generated Object"
    bl_idname = "object.save_generated_object_operator"

    # Filepath property for the operator
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        
        # Save the current scene or selected object to the specified filepath
        bpy.ops.wm.save_as_mainfile(filepath=self.filepath)
        self.report({'INFO'}, f"Saved Generated Object: {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        # Open the file browser for selecting the save location
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def register():
    # Register custom properties
    bpy.utils.register_class(MyProperties)

    # Register panels
    bpy.utils.register_class(HouseGanPanel)
    bpy.utils.register_class(ConverterPanel)
    bpy.utils.register_class(DataPanel)
    bpy.utils.register_class(FloorPanel)
    bpy.utils.register_class(WallsPanel)
    bpy.utils.register_class(RoofPanel)
    bpy.utils.register_class(GeneratePanel)

    # Register operators
    bpy.utils.register_class(OBJECT_OT_OpenOperator)
    bpy.utils.register_class(OBJECT_OT_LoadSVGOperator)
    bpy.utils.register_class(OBJECT_OT_ConvertToJSONOperator)
    bpy.utils.register_class(OBJECT_OT_LoadJSONOperator)
    bpy.utils.register_class(OBJECT_OT_GenerateShapesOperator)
    bpy.utils.register_class(OBJECT_OT_GenerateWallsOperator)
    bpy.utils.register_class(OBJECT_OT_GenerateDoorsOperator)
    bpy.utils.register_class(OBJECT_OT_GenerateRoofOperator)
    bpy.utils.register_class(OBJECT_OT_GenerateAllOperator)
    bpy.utils.register_class(OBJECT_OT_SaveGeneratedObject)

    # Register scene properties
    bpy.types.Scene.svg_file_path = bpy.props.StringProperty(name="SVG File Path")
    bpy.types.Scene.json_file_path = bpy.props.StringProperty(name="JSON File Path")
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)


def unregister():
    # Unregister custom properties
    bpy.utils.unregister_class(MyProperties)

    # Unregister panels
    bpy.utils.unregister_class(HouseGanPanel)
    bpy.utils.unregister_class(ConverterPanel)
    bpy.utils.unregister_class(DataPanel)
    bpy.utils.unregister_class(FloorPanel)
    bpy.utils.unregister_class(WallsPanel)
    bpy.utils.unregister_class(RoofPanel)
    bpy.utils.unregister_class(GeneratePanel)

    # Unregister operators
    bpy.utils.unregister_class(OBJECT_OT_OpenOperator)
    bpy.utils.unregister_class(OBJECT_OT_LoadSVGOperator)
    bpy.utils.unregister_class(OBJECT_OT_ConvertToJSONOperator)
    bpy.utils.unregister_class(OBJECT_OT_LoadJSONOperator)
    bpy.utils.unregister_class(OBJECT_OT_GenerateShapesOperator)
    bpy.utils.unregister_class(OBJECT_OT_GenerateWallsOperator)
    bpy.utils.unregister_class(OBJECT_OT_GenerateDoorsOperator)
    bpy.utils.unregister_class(OBJECT_OT_GenerateRoofOperator)
    bpy.utils.unregister_class(OBJECT_OT_GenerateAllOperator)
    bpy.utils.unregister_class(OBJECT_OT_SaveGeneratedObject)

    # Remove scene properties
    del bpy.types.Scene.my_tool
    del bpy.types.Scene.svg_file_path
    del bpy.types.Scene.json_file_path



if __name__ == "__main__":
    register()