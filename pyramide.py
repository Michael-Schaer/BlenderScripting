import bpy
import bmesh
import mathutils


def create_pyramide(height):
    print("Hello! Please create an object with the name 'Stone' and run the script")
    Stone = bpy.data.objects["Stone"]

    # Create stones of one side    
    for z in range(1, height):
        for y in range(0, z):
            #print (y, z) 
            print (-0.5*z+y, -z)          
            Stone.select = True
            Stone.location = mathutils.Vector((0.5*z, -0.5*z+y, -z))
            bpy.ops.object.duplicate()
    
    join_objects(True)

    # Duplicate and Rotate objects
    Stone = bpy.data.objects["Stone"]
    Stone.select = True
    for x in range(0, 3):
        bpy.ops.object.duplicate()
        bpy.ops.transform.rotate(value=-1.5708, axis=(-0, -0, -1))
    
    join_objects(False)
    

def join_objects(ignoreTopStone):
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH' and (not ignoreTopStone or ob.name != 'Top_Stone'):
            ob.select = True
            bpy.context.scene.objects.active = ob
        else:
            ob.select = False
    bpy.ops.object.join()
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)    
    
create_pyramide(10)    
