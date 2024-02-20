# House-GAN-Addon
**Tool for Generating 3D models of buildings in Blender.**


The process begins with the user initiating the creation of a graph using  [House-GAN++](https://github.com/ennauata/houseganpp), an AI-based external tool that generates apartment models in the form of abstract graphs. Next, the user browses through the generated apartment models and selects the one that best fits their needs.

The next step is saving the chosen model in SVG format by House-GAN++, containing a visual representation of the apartment plan. Using the Blender add-on, the user loads the SVG file. Then, through the add-on interface, the user runs the "convertSVG.py" script which converts the SVG file to a JSON file, more compatible with the data structure used in Blender.

The House-GAN++ add-on in Blender loads the JSON file containing spatial data ready for further processing. The next step is converting the data from JSON format to 3D structures, including generating geometry of objects such as walls, floors, or doors. The user has the option to customize the generated model, for example, changing wall heights or floor thickness, and can generate entire floors using interactive panels in the add-on. Based on the converted and customized data, the add-on generates a complete 3D model that the user can edit, enhance, or directly use in their projects.

After finishing editing and customizing the model to meet requirements, the user saves the 3D model using functions available in Blender. The process concludes with a finished 3D model that can be used in further stages of work, such as rendering scenes, creating animations, games, or 3D printing.

The "HouseGanAdd.py" file is an add-on for the Blender program which, using the loaded JSON files, creates a 3D model from a 2D apartment model in the Blender scene.

## Examples
Examples of data generated in the House-GAN++ application are located in the SVG folder.

The converted data using the converter are located in the JSON folder.

**Operation of the House-GAN++ interface:** <br /><br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/819c456f-ad92-4bc1-91c9-6578857bbde2)

**Addon interface:** <br /><br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/414135bd-7684-462a-b7f7-e573ee3b8ba9)

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

The model generated with a large number of rooms:<br />
![image](https://github.com/Al27Ms/House-GAN-Addon/assets/102626627/37979255-4873-4283-a8af-cff95f0bc80f)
