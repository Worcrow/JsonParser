from src.parser.parser import *


class Converter:
    def __init__(self):
        return

    def convert(self, root):
        if root.value.type == JsonStructuredTypeSymbol.BEGINOBJECT:
            result = dict()
            for child in root.child:
                key_node, value_node = child.key, child.value
                key = key_node.value[1:-1]
                if key in result:
                    raise SyntaxError(
                        f"Duplicate key '{key}' detected in object at line {key_node.position[0]}, column {key_node.position[1]}. "
                        f"Each key in a JSON object must be unique. Consider renaming or removing the duplicate."
                    )
                value = self.convert(value_node)
                result[key] = value
            return result

        if root.value.type == JsonStructuredTypeSymbol.BEGINARRAY:
            result = []
            for child in root.child:
                result.append(self.convert(child))
            return result

        if root.value.type == JsonTokenType.STRING:
            return root.value.value[1:-1]

        if root.value.type == JsonTokenType.NUMBER:
            if '.' in root.value.value:
                return float(root.value.value)
            else:
                return int(root.value.value)

        if root.value.type == JsonTokenType.NULL:
            return None

        if root.value.type == JsonTokenType.BOOLEAN:
            return True if root.value.value == 'true' else False

       