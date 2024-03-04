# House-GAN-Addon
**Tool for Generating 3D models of buildings in Blender.**

The add-on introduces automation to the model generation process, leveraging advanced artificial intelligence algorithms to streamline the work of designers and architects. Its main achievement is the integration of Generative Adversarial Networks (GANs) with an interactive 3D modeling environment, enabling the dynamic creation of realistic building structures. 

Users have the ability to easily manipulate building parameters such as wall height, roof thickness, or the number of floors, opening up new perspectives in spatial design. Thanks to this tool, the model creation process is not only faster but also more intuitive, which can significantly accelerate the initial design stage in architecture. This add-on serves as a good example of integrating artificial intelligence with creative tools such as Blender.

## The functionality of the add-on

The process begins with the user initiating the creation of a graph using  [House-GAN++](https://github.com/ennauata/houseganpp), an AI-based external tool that generates apartment models in the form of abstract graphs. Next, the user browses through the generated apartment models and selects the one that best fits their needs.

The next step is saving the chosen model in SVG format by House-GAN++, containing a visual representation of the apartment plan. Using the Blender add-on, the user loads the SVG file. Then, through the add-on interface, the user runs the "convertSVG.py" script which converts the SVG file to a JSON file, more compatible with the data structure used in Blender.

The House-GAN++ add-on in Blender loads the JSON file containing spatial data ready for further processing. The next step is converting the data from JSON format to 3D structures, including generating geometry of objects such as walls, floors, or doors. The user has the option to customize the generated model, for example, changing wall heights or floor thickness, and can generate entire floors using interactive panels in the add-on. Based on the converted and customized data, the add-on generates a complete 3D model that the user can edit, enhance, or directly use in their projects.

After finishing editing and customizing the model to meet requirements, the user saves the 3D model using functions available in Blender. The process concludes with a finished 3D model that can be used in further stages of work, such as rendering scenes, creating animations, games, or 3D printing.

The "HouseGanAdd.py" file is an add-on for the Blender program which, using the loaded JSON files, creates a 3D model from a 2D apartment model in the Blender scene.


## Addon interface:
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/414135bd-7684-462a-b7f7-e573ee3b8ba9)

**The interface consists of:**
<br />
- House-GAN++: It includes the "Open House-GAN++" button, which opens a web browser to the Flask server address where House-GAN++ is running (http://127.0.0.1:5000/).
- Converter Panel: It contains the "Load SVG" button, allowing the user to load an SVG file and displays the name of the loaded SVG file if one exists. The "Convert to JSON" button performs the conversion of the loaded SVG file to JSON format.
- Data Panel: It includes the "Load JSON" button, enabling the user to load a JSON file and displays the name of the loaded JSON file if one exists.
- Floor Panel: It has a field for entering the floor height and a "Generate" button that generates floor objects based on SVG data.
- Walls Panel: It has fields for entering the height and thickness of walls, and "Generate Walls" and "Generate Doors" buttons for generating walls and doors.
- Roof Panel: It has a field for entering the thickness of the roof and a "Generate Roof" button for generating the roof.
- Generate Panel: It has a field for entering the floor generation level and a "Generate Level" button that generates all objects at the specified level. It has an option "Use Color" to disable color overlay and a "Save Generated Object" button to save the generated objects.


## Examples
Examples of data generated in the House-GAN++ application are located in the SVG folder.

The converted data using the converter are located in the JSON folder.

**Operation of the House-GAN++ interface:** <br /><br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/819c456f-ad92-4bc1-91c9-6578857bbde2)

The user interface presents a system for generating apartment layouts using the House-GAN++ application. On the left side, an interactive graph is displayed where the user can add nodes and edges, representing individual rooms and their connections. Each room on the graph is marked with a different color, facilitating the identification of each room's function, such as living room (red), kitchen (orange), or bathroom (gray). 

On the right side of the interface, examples of generated apartment layouts are displayed, which visualize the graph on the left side. The user can browse through various sample configurations and choose the layout that best suits them, which is then used for generation in Blender through an add-on. 
A modification of the original House-GAN++ was the design of a function to save the main model to an SVG file.

**The model created from the graph:**<br /><br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/d5b95664-980f-4ca0-8da5-5838cf10412f)
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/9f0e9b90-da77-4ed4-8c91-b91610a41918)

**Created model:** floor, dors:<br /><br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/9c52e97e-d701-44ba-b95e-148999abb854)

**Created model: floor, dors, walls:**<br /><br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/0762c895-fb6d-42e7-b5cb-68dcbcc24d66)

**Created model: floor, dors, walls, roof:**<br /><br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/f4719a14-1d23-47c9-b581-c5951082f501)

**Created model: floor, dors, walls, roof, levels:**<br /><br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/2ab3431a-f447-43aa-9f79-5ee6d4c63d30)

**Created model without colors:**<br /><br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/5971ea40-f90a-4c22-a8d6-ba92e63dafd8)

**The model generated with a large number of rooms:**<br /><br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/37979255-4873-4283-a8af-cff95f0bc80f)
<br/>
## Libraries used in the script:

- os
- webbrowser
- bpy
- json
- math
- subprocess
