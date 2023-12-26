class ExpressionNodePanel(bpy.types.Panel):
    bl_idname = 'CUSTOM_PT_EXPRESSION_NODE_PANEL'
    bl_label = 'Expression Nodes'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Expression Nodes'

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.prop(scene.custom_expression_nodes_props, "expression")
        # layout.prop(scene.custom_expression_nodes_props, "in_group")
        layout.operator('wm.add_expression_nodes')
        props = self.layout.operator('object.gn')
        props.my_bool = True
        props.my_string = "Shouldn't that be 47?"

        # You can set properties dynamically:
        if context.object:
            props.my_float = context.object.location.x
        else:
            props.my_float = 327
