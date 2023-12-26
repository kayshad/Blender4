class ExpressionNodeOperator(bpy.types.Operator):
    bl_idname = 'wm.add_expression_nodes'
    bl_label = 'Create Nodes'
    bl_options = {'REGISTER', 'UNDO'}

    value_node_cache = {}
    init_position = [100, 300]
    space_x = 100
    space_y = 100




    def add_node(self, type):
        bpy.ops.node.add_node(type=type)
        return bpy.context.active_node

    def create_binary_operator(self, value, location):
        operation_map = {
            ast.Add: "ADD",
            ast.Mult: "MULTIPLY",
            ast.Sub: "SUBTRACT",
            ast.Div: "DIVIDE",
            ast.Mod: "MODULO",
            ast.Pow: "POWER",
        }
        left_node = self.create_nodes(value.left, [location[0]-self.space_x, location[1]+self.space_y])
        right_node = self.create_nodes(value.right, [location[0]-self.space_x, location[1]-self.space_y])
        node = self.add_node("ShaderNodeMath")
        print(node.location)
        self.operator_node_list.append(node)
        self.node_tree.links.new(node.inputs[0], left_node.outputs[0])
        self.node_tree.links.new(node.inputs[1], right_node.outputs[0])
        node.operation = operation_map.get(type(value.op), "ADD")
        node.location = location
        return node

    def create_call(self, value, location):
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
            arg_nodes.append(self.create_nodes(arg, [location[0]-self.space_x, location[1]+idx * self.space_y]))
        node = self.add_node("ShaderNodeMath")
        node.operation = func_map.get(value.func.id, "ADD")
        node.location = location
        for idx, arg in enumerate(arg_nodes):
            self.node_tree.links.new(node.inputs[idx], arg.outputs[0])
        return node

    def create_name(self, value, location):
        if value.id in self.value_node_cache:
            return self.value_node_cache[value.id]
        node = self.add_node("ShaderNodeValue")
        node.label = value.id
        node.location = location
        self.value_node_cache[value.id] = node
        return node

    def create_constant(self, value, location):
        node = self.add_node("ShaderNodeValue")
        node.outputs[0].default_value = value.value
        node.label = str(value.value)
        node.location = location
        return node

    def create_invalid(self, *_):
        return None

    def create_nodes(self, value, location):
        types_map = {
            ast.BinOp: self.create_binary_operator,
            ast.Call: self.create_call,
            ast.Name: self.create_name,
            ast.Constant: self.create_constant
        }
        creator = types_map.get(type(value), self.create_invalid)
        return creator(value, location)

    def parse_expressions(self, props):
        module = ast.parse(props.expression)
        for expression in module.body:
            root = self.create_nodes(expression.value, self.init_position)

    def execute(self, context):
        scene = context.scene
        space = context.space_data
        self.node_tree = space.node_tree
        self.value_node_cache = {}
        self.operator_node_list = []
        self.parse_expressions(scene.custom_expression_nodes_props)
        return {'FINISHED'}
