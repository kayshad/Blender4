bl_info = {
    "name": "Expression Nodes",
    "author": "Kays",
    "version": (0, 1, 0),
    "blender": (4, 0, 1),
    "location": "Nodes > Sidebar > Expression Nodes",
    "description": "Generate math nodes based on a given expresion",
    "doc_url": "",
    "category": "Node",
}

import bpy
import ast
from . props import *
from . opsexp import *
from . opsmy import *
from . pano import *




def register():
    bpy.utils.register_class(ExpressionNodePropertyGroup)
    bpy.utils.register_class(ExpressionNodeOperator)
    bpy.utils.register_class(OBJECT_OT_gn)
    bpy.utils.register_class(ExpressionNodePanel)
    bpy.types.Scene.custom_expression_nodes_props = bpy.props.PointerProperty(type=ExpressionNodePropertyGroup)


def unregister():
    bpy.utils.unregister_class(ExpressionNodePropertyGroup)
    bpy.utils.unregister_class(ExpressionNodeOperator)
    bpy.utils.unregister_class(OBJECT_OT_gn)
    bpy.utils.unregister_class(ExpressionNodePanel)

if __name__ == '__main__':
    register()
