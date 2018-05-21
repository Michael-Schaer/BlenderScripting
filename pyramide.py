import bpy
import bmesh
import mathutils

# === Definitions ===

def CubeName():
    return "Stone"  

def CubeSize():
    return 1  

def CubeHalf():
    return CubeSize() / 2   

def PyramideDepth():
    return 1
 

# === Logic ===

def create_pyramide():
    create_cube()
    create_side()
    '''join_objects(True)
    duplicate_side()
    join_objects(False)
    apply_modifiers()'''
    
    
def create_side():    
    Stone = bpy.data.objects[CubeName()]
  
    for z in range(1, PyramideDepth()):
        for y in range(0, z): 
            Stone.select = True
            Stone.location = mathutils.Vector((CubeHalf()*z, -CubeHalf()*z+y, -z))
            bpy.ops.object.duplicate()
            bpy.ops.object.select = False #TODO deselect not working

    
def duplicate_side():
    print ("dupli")   
    Stone = bpy.data.objects[CubeName()]
    Stone.select = True
    
    for x in range(0, 3):
        print(x)
        bpy.ops.object.duplicate()
        bpy.ops.transform.rotate(value=-1.5708, axis=(-0, -0, -1))


def join_objects(ignoreTopStone):
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH' and (not ignoreTopStone or ob.name != CubeName() + '.001'):
            ob.select = True
            bpy.context.scene.objects.active = ob
        else:
            ob.select = False
    bpy.ops.object.join()
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)    
    
    
def create_cube():
    bpy.ops.mesh.primitive_cube_add(
        radius=CubeHalf(), 
        location=(0, 0, 0)
    )
    NewObject = bpy.context.active_object
    NewObject.name = CubeName()
    bpy.ops.object.duplicate()  


def apply_modifiers():
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.transform.vertex_random()
    

create_pyramide() 