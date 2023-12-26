import bpy
import ast
import mathutils

class ExpressionNodeOperator(bpy.types.Operator):
    bl_idname = 'wm.add_expression_nodes'
    bl_label = 'Create Nodes'
    bl_options = {'REGISTER', 'UNDO'}
    value_node_cache = {}
    init_position = [100, 300]
    space_x = 100
    space_y = 100





    def add_node(self, type, node_tree):
        node = node_tree.nodes.new(type=type)
        return node

    def create_binary_operator(self, value, location, node_tree):
        operation_map = {
            ast.Add: "ADD",
            ast.Mult: "MULTIPLY",
            ast.Sub: "SUBTRACT",
            ast.Div: "DIVIDE",
            ast.Mod: "MODULO",
            ast.Pow: "POWER",
        }
        left_node = self.create_nodes(value.left, [location[0]-self.space_x, location[1]+self.space_y], node_tree)
        right_node = self.create_nodes(value.right, [location[0]-self.space_x, location[1]-self.space_y], node_tree)
        node = self.add_node("ShaderNodeMath", node_tree)
        self.operator_node_list.append(node)
        node_tree.links.new(node.inputs[0], left_node.outputs[0])
        node_tree.links.new(node.inputs[1], right_node.outputs[0])
        node.operation = operation_map.get(type(value.op), "ADD")
        node.location = location
        return node

    def create_call(self, value, location, node_tree):
        func_map = {
            "sin": "SINE",
            "cos": "COSINE",
            "tan": "TANGENT",
            "asin": "ARCSINE",
            "arcsin": "ARCSINE",
            "acos": "ARCCOSINE",
            "arccos": "ARCCOSINE",
            "atan": "ARCTANGENT",
            "arctan": "ARCTANGENT",
            "atan2": "ARCTAN2",
            "arctan2": "ARCTAN2",
            "sinh": "SINH",
            "cosh": "COSH",
            "tanh": "TANH",
            "pow": "POWER",
            "log": "LOGARITHM",
            "sqrt": "SQRT",
            "abs": "ABSOLUTE",
            "exp": "EXPONENT",
            "min": "MINIMUM",
            "max": "MAXIMUM",
            "sign": "SIGN",
            "round": "ROUND",
            "floor": "FLOOR",
            "ceil": "CEIL",
            "trunc": "TRUNC",
            "fract": "FRACT",
            "rad": "RADIANS",
            "deg": "DEGREES"
        }
        arg_nodes = []
        for idx, arg in enumerate(value.args):
            arg_nodes.append(self.create_nodes(arg, [location[0]-self.space_x, location[1]+idx * self.space_y], node_tree))
        node = self.add_node("ShaderNodeMath", node_tree)
        node.operation = func_map.get(value.func.id, "ADD")
        node.location = location
        for idx, arg in enumerate(arg_nodes):
            node_tree.links.new(node.inputs[idx], arg.outputs[0])

        return node

    def create_name(self, value, location, node_tree):
        if value.id in self.value_node_cache:
            return self.value_node_cache[value.id]
        node = self.add_node("ShaderNodeValue", node_tree)
        node.label = value.id
        node.location = location
        self.value_node_cache[value.id] = node

        return node

    def create_constant(self, value, location, node_tree):
        node = self.add_node("ShaderNodeValue", node_tree)
        node.outputs[0].default_value = value.value
        node.label = str(value.value)
        node.location = location
        return node

    def create_invalid(self, *_, node_tree):
        return None

    def create_nodes(self, value, location, node_tree):
        types_map = {
            ast.BinOp: self.create_binary_operator,
            ast.Call: self.create_call,
            ast.Name: self.create_name,
            ast.Constant: self.create_constant
        }
        creator = types_map.get(type(value), self.create_invalid)
        return creator(value, location, node_tree)

    def parse_expressions(self, props, node_tree):
        module = ast.parse(props.expression)
        for expression in module.body:
            root = self.create_nodes(expression.value, self.init_position, node_tree)


    def execute(self, context):
        scene = context.scene
        space = context.space_data
        self.node_tree = space.node_tree
        self.value_node_cache = {}
        self.operator_node_list = []

        group = bpy.data.node_groups.new('EiE', 'GeometryNodeTree')
        group.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        input_node = group.nodes.new('NodeGroupInput')
        input_node.select = False
        input_node.location.x = -200 - input_node.width
        group.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
        output_node = group.nodes.new('NodeGroupOutput')
        output_node.is_active_output = True
        output_node.select = False
        output_node.location.x = 200 + output_node.width
        ng = self.node_tree.nodes.new('GeometryNodeGroup')

        ng.node_tree = group
        ngt = ng.node_tree

        self.parse_expressions(scene.custom_expression_nodes_props, ngt )

        a = self.add_node('GeometryNodeCurvePrimitiveLine', ngt)
        a.inputs['End'].default_value = mathutils.Vector((1.0, 2.0, 3.0))
        a1 = self.add_node('GeometryNodeResampleCurve', ngt)
        a1.inputs['Count'].default_value = 100
        b = self.add_node('GeometryNodeCurveToMesh', ngt)
        c = self.add_node('GeometryNodeCurvePrimitiveCircle', ngt)



        ngt.links.new(a.outputs['Curve'],a1.inputs['Curve'])
        ngt.links.new(a1.outputs['Curve'],b.inputs['Curve'])
        ngt.links.new(c.outputs['Curve'],b.inputs['Profile Curve'])
        ngt.links.new(b.outputs['Mesh'],output_node.inputs['Geometry'])

        return {'FINISHED'}


