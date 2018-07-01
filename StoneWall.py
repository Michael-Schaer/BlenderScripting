import bpy
import bmesh
import random
import mathutils

# === Setup ===

WallHeight = 4
WallLength = 20
CubeSpace = 0.0 #is better 0 when using random modifier

CubeName = "Stone"
Stone = None
CubeSize = 1
CubeHalf = CubeSize / 2
scn = bpy.context.scene
IndexSelection = [2,3,6,7]
LastWidth = 0.0
LastStoneReference = 0.0


# === Logic ===

def create_object():
    global LastStoneReference
    LastStoneReference = CubeSize * WallLength * 1.5
    create_cube()
    for z in range(0, WallHeight):
        build_horizontal(z)
        reset_stone(z)
    join_objects()
    apply_modifiers()  
    objs = bpy.data.objects      
    objs.remove(objs[CubeName], True)
    
    
def build_horizontal(zIndex):
    Stone = bpy.data.objects[CubeName]
    global LastWidth
    NextPosition = 0.0     
    while NextPosition < LastStoneReference:
        Width = round(random.random()*5)/5
        Stone.select = True
        print(LastWidth, NextPosition)
        Stone.location = mathutils.Vector((0, NextPosition, zIndex))
        NextPosition = Stone.location.y + Width + CubeSpace + CubeSize
        if NextPosition >= LastStoneReference:
            Width = LastStoneReference - Stone.location.y - CubeHalf   
        duplicate_selected(Stone, Width, LastWidth)
        LastWidth = Width
        

def duplicate_selected(Stone, Width, LastWidth):
    Stone.select = True
    bpy.ops.object.editmode_toggle()
    select_vertices()
    bpy.ops.transform.translate(value=(0, Width-LastWidth, 0), constraint_orientation='LOCAL')
    bpy.ops.object.editmode_toggle()
    new_obj = Stone.copy()
    new_obj.data = Stone.data.copy()
    new_obj.animation_data_clear()
    scn.objects.link(new_obj)
    bpy.ops.object.select_all(action='DESELECT')
    

def select_vertices():
    obj = bpy.context.object
    objData = obj.data
    mesh = bmesh.from_edit_mesh(objData)
    vertices = [e for e in mesh.verts]
    for vert in vertices:
        if vert.index in IndexSelection: # relevant indexes: 2,3,6,7
            vert.select = True
        else:
            vert.select = False
    bmesh.update_edit_mesh(objData, True) 
    

def join_objects():
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH' and ob.name != CubeName:
            ob.select = True
            bpy.context.scene.objects.active = ob
        else:
            ob.select = False
    bpy.ops.object.join()
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)    
    

def reset_stone(zIndex):
    Stone = bpy.data.objects[CubeName]
    Stone.select = True
    Stone.location = (0, 0, zIndex)
    
    
def create_cube():
    bpy.ops.mesh.primitive_cube_add(
        radius=CubeHalf, 
        location=(0, 0, 0)
    )
    NewObject = bpy.context.active_object
    NewObject.name = CubeName


def apply_modifiers():
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.transform.vertex_random()
    

create_object() 