class ExpressionNodePropertyGroup(bpy.types.PropertyGroup):
    expression: bpy.props.StringProperty(
        name="Expression",
        default="2 * sin(x)",
        maxlen=1024,
        )
    in_group: bpy.props.BoolProperty(name="Group", default=False)
