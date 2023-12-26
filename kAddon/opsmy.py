class OBJECT_OT_gn(bpy.types.Operator):

    bl_idname = "object.property_gn"
    bl_label = "Property Example"
    bl_options = {'REGISTER', 'UNDO'}

    def create_node(self, node_tree, type_name, node_x_location, node_location_step_x=0, node_y_location=0):
        node_obj = node_tree.nodes.new(type=type_name)
        node_obj.location.x = node_x_location
        node_obj.location.y = node_y_location
        node_x_location += node_location_step_x
        return node_obj, node_x_location

    my_float: bpy.props.FloatProperty(name="Some Floating Point")
    my_bool: bpy.props.BoolProperty(name="Toggle Option")
    my_string: bpy.props.StringProperty(name="String Value")

    def gdn(self,name):
        group = bpy.data.node_groups.new(name, 'GeometryNodeTree')
        group.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        input_node = group.nodes.new('NodeGroupInput')
        input_node.select = False
        input_node.location.x = -200 - input_node.width
        group.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
        output_node = group.nodes.new('NodeGroupOutput')
        output_node.is_active_output = True
        output_node.select = False
        output_node.location.x = 200 + output_node.width
        node_x_location = 0
        node_location_step_x = 300
        return group

    def execute(self, context):



        node_tree = self.gdn('GiG')


        mesh_cube_node, node_x_location = self.create_node(node_tree, "GeometryNodeMeshCube", node_x_location, node_location_step_x)
        subdivide_mesh_node, node_x_location = self.create_node(node_tree, "GeometryNodeSubdivideMesh", node_x_location, node_location_step_x)
        subdivide_mesh_node.inputs["Level"].default_value = 3
        triangulate_node, node_x_location = self.create_node(node_tree, "GeometryNodeTriangulate", node_x_location, node_location_step_x)
        split_edges_node, node_x_location = self.create_node(node_tree, "GeometryNodeSplitEdges", node_x_location, node_location_step_x)
        join_geometry_node, node_x_location = self.create_node(node_tree, "GeometryNodeJoinGeometry", node_x_location, node_location_step_x)
        node_tree.links.new(mesh_cube_node.outputs["Mesh"],subdivide_mesh_node.inputs["Mesh"])
        node_tree.links.new(subdivide_mesh_node.outputs["Mesh"],triangulate_node.inputs["Mesh"])
        node_tree.links.new(triangulate_node.outputs["Mesh"],split_edges_node.inputs["Mesh"])
        node_tree.links.new(split_edges_node.outputs["Mesh"],join_geometry_node.inputs["Geometry"])
        node_tree.links.new(join_geometry_node.outputs["Geometry"], output_node.inputs["Geometry"])
        modifier = cube.modifiers.new("Geometry Nodes Kays", "NODES")



        modifier.node_group = self.gdn('Groupe')

        ne = modifier.node_group.nodes.new(type='GeometryNodeGroup')
        ne.node_tree = node_tree
        modifier.node_group.links.new(ne.outputs["Geometry"], output_node.inputs["Geometry"])

        return {'FINISHED'}
