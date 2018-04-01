



bl_info = {
    "name":"Add a road ",
    "author":"Oscar",
    "version":(1,0),
    "blender":(2,79),
    "location":"View3D > Add > Mesh > Add road",
    "description":"Adds a new road",
    "warning":"",
    "wiki_url":"",
    "category":"Add Mesh"
    }

'''
Import logic: 

1. UI elements
2. curve setup
2. material setup
3. road mesh setup
4. accessories mesh setup
5. a two-way function that adds a road
6. init: brings all these together
'''


if "bpy" in locals():
    import importlib
    importlib.reload(curveSetup)
    importlib.reload(meshSetup)
    importlib.reload(materialSetup)
    

else:
    from . import curveSetup 
    from . import meshSetup 
    from . import materialSetup
    
    
    

import os
import bpy
import random
from mathutils import Vector
C=bpy.context
D=bpy.data
O=bpy.ops


# classes
class OBJECT_OT_add_road(bpy.types.Operator):

    
    """Adds a road to the 3D view"""
    bl_label = "Add road"
    bl_idname = "mesh.add_road"
    bl_options = {'REGISTER', 'UNDO'}
    
    '''
    We're assuming 1 blender unit = 1 meter
    based on that, here's some real world measurements. 
    ***UNIVERSITY DISTRICT STREET***
    5 feet:            1.5
    Human:             1.8
    Lanes:             1
    Lane width:        2
    divider width:     ?
    shoulder width:    1.8
    bike width:        0
    gutter width:      0.1
    greenway width:    1.5
    sidewalk width:    1.5
    
    
    
    '''
    
    
    roadPresets = bpy.props.EnumProperty(
        name ="Road presets",
        description = "Various default roads",
        
        items = [('university', "University Ave", "University Ave"), #identifier, name, description
                 ('mainstreet', "Main Street USA", "A generic beginner street"),
                 ('highway520', "Highway 520", "A highway with IUD lights in the middle, LOL")]
        #update = updateRoadPreset()
        )
    
    accDividerOn=bpy.props.BoolProperty(name="Divider accessories on/off", default=True, description="Turn on Accessories on the road divider")
    accShoulderOn=bpy.props.BoolProperty(name="Shoulder accessories on/off", default=True, description="Turn on Accessories on the shoulder")
    accGutterOn=bpy.props.BoolProperty(name="Gutter accessories on/off", default=True, description="Turn on Accessories on the gutter")
    accGreenwayOn=bpy.props.BoolProperty(name="Greenway accessories on/off", default=True, description="Turn on Accessories on the greenway")
    accSidewalkOn=bpy.props.BoolProperty(name="Sidewalk accessories on/off", default=True, description="Turn on Accessories on the sidewalk")
    
    accDivider=bpy.props.EnumProperty(
        name = "Divider accessory",
        description = "Selects which kind of divider accessory to insert",
        items = [("rail", "rail", "rail"), ("concrete", "concrete", "concrete"), ("poles", "poles", "poles")
            ]
        )
    
    
    lanes = bpy.props.IntProperty( 
        name = "Lanes",
        default = 2,
        description = "Number of lanes"
        )
    laneWidth = bpy.props.FloatProperty(
        name = "Lane Width",
        default = 3,
        description = "How wide across each lane is"
        )
    dividerWidth = bpy.props.FloatProperty(
        name = "Divider width",
        default = .5,
        description = "division size between east/west traffic lanes"
        )
    shoulderWidth = bpy.props.FloatProperty(
        name = "Shoulder width",
        default = 2,
        description = "width of shoulder or parking lane to left/right"
        )

    bikeWidth = bpy.props.FloatProperty(
        name = "Bike width",
        default = 1,
        description = "width of shoulder or parking lane to left/right"
        )
    gutterWidth = bpy.props.FloatProperty(
        name = "Gutter width",
        default = .2,
        description = "width of gutter as transition to pedestrian area" #needs a height modifier...?
        )
    greenwayWidth = bpy.props.FloatProperty(
        name="Greenway width",
        default = 1,
        description = "width of greenish area ala seattle" )    
    sidewalkWidth = bpy.props.FloatProperty(
        name="Sidewalk width",
        default = 1.5,
        description = "width of sidewalk" )
    name = bpy.props.StringProperty(
        name = "Name",
        default = "Road",
        description = "Name of added road"
        )
    
    def draw(self, context):
            layout = self.layout
            scene = bpy.data.window_managers["WinMan"].operators['MESH_OT_add_road']
            #that big long name is where used panels are
            #hence still uses our props
            layout.label(text="Add a road, dude!")   
            

            row = layout.row()
            row.prop(scene, "roadPresets")
           
            
            layout.label(text="pathway widths")
            row = layout.row()
            row.prop(scene, "lanes")
            row.prop(scene, "laneWidth")

            row = layout.row()
            row.prop(scene, "dividerWidth")
            row.prop(scene, "shoulderWidth")

            row = layout.row()
            row.prop(scene, "bikeWidth")
            row.prop(scene, "gutterWidth")

            row = layout.row()
            row.prop(scene, "greenwayWidth")
            row.prop(scene, "sidewalkWidth")
            
            layout.label(text="accessories")
            row = layout.row()
            row.prop(scene, "accDividerOn")
            row.prop(scene, "accShoulderOn")
            row.prop(scene, "accGutterOn")
            row.prop(scene, "accGreenwayOn")
            row.prop(scene, "accSidewalkOn")
            
            row = layout.row()
            row.prop(scene, "accDivider")
        
#mesh.splines[0].bezier_points[0].co[1]
    
#list of roads

#lanes, laneWidth, dividerWidth, shoulderWidth, bikeWidth, gutterWidth, greenwayWidth, sidewalkWidth, name

 
    roads = [[1, 2, .1, 1.8, 0, 0.1, 1.5, 1.5, "university"],
             [1, 2, .1, 1.8, 0, 0.1, 1.5, 1.5, "mainstreet"],
             [4, 2.5, 1, 3, 0, 0, 5, 0, "highway520"]]        
            


    def execute(self, context):
        
        
        def setPreset():
            bpy.data.window_managers["WinMan"].operators['MESH_OT_add_road'].roadPresets

    

        
        #combining them in a modifier stack
            
            


        

        #distance bookmarks


#assembling the default road
        
        O.curve.primitive_bezier_curve_add(radius=10)        

        roadCurve=C.object
        print(roadCurve) #whaaaaat the fuuuuck....this does it?

        
        if (self.dividerWidth !=0):
            meshSetup.groundMesh("divider", 0, self.dividerWidth)
            curveSetup.curveSetup (roadCurve, D.objects["divider"], 1)     
        
        if (self.laneWidth !=0):
            meshSetup.groundMesh("lanes", self.dividerWidth, self.dividerWidth+self.laneWidth)
            curveSetup.curveSetup (roadCurve, D.objects["lanes"], 1, self.lanes)     
        
        #since road is multiplicative, a custom variable
        newLaneStart = self.laneWidth*self.lanes
        newLaneStart +=self.dividerWidth
        
        if (self.shoulderWidth != 0):
            meshSetup.groundMesh("shoulder", newLaneStart, newLaneStart + self.shoulderWidth)
            newLaneStart+=self.shoulderWidth        
        
        if (self.bikeWidth !=0):
            meshSetup.groundMesh("bike", newLaneStart, newLaneStart + self.bikeWidth)
            newLaneStart+=self.bikeWidth        
        
        if (self.gutterWidth !=0):
            meshSetup.groundMesh("gutter", newLaneStart, newLaneStart + self.gutterWidth)
            newLaneStart+=self.gutterWidth        
        if (self.greenwayWidth !=0):
            meshSetup.groundMesh("greenway", newLaneStart, newLaneStart + self.greenwayWidth)
            newLaneStart+=self.greenwayWidth        
        if (self.sidewalkWidth !=0):
            meshSetup.groundMesh("sidewalk", newLaneStart, newLaneStart + self.sidewalkWidth)
            newLaneStart+=self.sidewalkWidth
        

     
        curveSetup.curveSetup (roadCurve, D.objects["shoulder"], 1)             
        curveSetup.curveSetup (roadCurve, D.objects["bike"], 1)     
        curveSetup.curveSetup (roadCurve, D.objects["gutter"], 1)     
        curveSetup.curveSetup (roadCurve, D.objects["greenway"], 1)             
        curveSetup.curveSetup (roadCurve, D.objects["sidewalk"], 1)             


        
        
        materialSetup.randomMaterial(D.objects["divider"])
        materialSetup.randomMaterial(D.objects["lanes"])
        materialSetup.randomMaterial(D.objects["shoulder"])        
        materialSetup.randomMaterial(D.objects["bike"])
        materialSetup.randomMaterial(D.objects["gutter"])
        materialSetup.randomMaterial(D.objects["greenway"])
        materialSetup.randomMaterial(D.objects["sidewalk"])
        
        return {'FINISHED'}



def add_object_button(self, context):
    self.layout.operator(
            OBJECT_OT_add_road.bl_idname)

# registration
def register():
    bpy.utils.register_class(OBJECT_OT_add_road)
    #bpy.utils.register_class(smooth_monkey_panel)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_road)
    #bpy.utils.unregister_class(smooth_monkey_panel)
    bpy.types.INFO_MT_mesh_add.remove(ct_button)

if __name__ == "__main__":
    register()