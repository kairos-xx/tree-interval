AST_TYPES = {
    # Module level
    "Module": {
        "description": "Root node for entire file",
        "statement": True,
        "is_set": False
    },
    "Import": {
        "description": "Import statement",
        "statement": True,
        "is_set": False
    },
    "ImportFrom": {
        "description": "From import statement",
        "statement": True,
        "is_set": False
    },
    # Function and Class
    "FunctionDef": {
        "description": "Function definition",
        "statement": True,
        "is_set": False
    },
    "AsyncFunctionDef": {
        "description": "Async function definition",
        "statement": True,
        "is_set": False
    },
    "ClassDef": {
        "description": "Class definition",
        "statement": True,
        "is_set": False
    },
    "Return": {
        "description": "Return statement",
        "statement": True,
        "is_set": False
    },
    "Args": {
        "description": "Function arguments",
        "statement": False,
        "is_set": False
    },
    "arguments": {
        "description": "Function argument definitions",
        "statement": False,
        "is_set": False
    },
    # Variables and Assignments
    "Assign": {
        "description": "Assignment operation",
        "statement": True,
        "is_set": True
    },
    "AnnAssign": {
        "description": "Annotated assignment",
        "statement": True,
        "is_set": True
    },
    "AugAssign": {
        "description": "Augmented assignment (+=, -=, |=, etc)",
        "statement": True,
        "is_set": True
    },
    "Name": {
        "description": "Variable or function name",
        "statement": False,
        "is_set": False
    },
    "Attribute": {
        "description": "Attribute access (obj.attr)",
        "statement": False,
        "is_set": False
    },
    # Control Flow
    "If": {
        "description": "If conditional statement",
        "statement": True,
        "is_set": False
    },
    "For": {
        "description": "For loop",
        "statement": True,
        "is_set": False
    },
    "AsyncFor": {
        "description": "Async for loop",
        "statement": True,
        "is_set": False
    },
    "While": {
        "description": "While loop",
        "statement": True,
        "is_set": False
    },
    "Break": {
        "description": "Break statement",
        "statement": True,
        "is_set": False
    },
    "Continue": {
        "description": "Continue statement",
        "statement": True,
        "is_set": False
    },
    "Try": {
        "description": "Try block",
        "statement": True,
        "is_set": False
    },
    "TryStar": {
        "description": "Try block with star",
        "statement": True,
        "is_set": False
    },
    "ExceptHandler": {
        "description": "Except clause",
        "statement": True,
        "is_set": False
    },
    "With": {
        "description": "With statement",
        "statement": True,
        "is_set": False
    },
    "AsyncWith": {
        "description": "Async with statement",
        "statement": True,
        "is_set": False
    },
    "Match": {
        "description": "Pattern matching (Python 3.10+)",
        "statement": True,
        "is_set": False
    },
    # Expressions
    "Expr": {
        "description": "Expression statement",
        "statement": True,
        "is_set": False
    },
    "Call": {
        "description": "Function call",
        "statement": False,
        "is_set": False
    },
    "Constant": {
        "description": "Literal constant",
        "statement": False,
        "is_set": False
    },
    "List": {
        "description": "List literal",
        "statement": False,
        "is_set": False
    },
    "Tuple": {
        "description": "Tuple literal",
        "statement": False,
        "is_set": False
    },
    "Dict": {
        "description": "Dictionary literal",
        "statement": False,
        "is_set": False
    },
    "Set": {
        "description": "Set literal",
        "statement": False,
        "is_set": False
    },
    "ListComp": {
        "description": "List comprehension",
        "statement": False,
        "is_set": False
    },
    "SetComp": {
        "description": "Set comprehension",
        "statement": False,
        "is_set": False
    },
    "DictComp": {
        "description": "Dictionary comprehension",
        "statement": False,
        "is_set": False
    },
    "GeneratorExp": {
        "description": "Generator expression",
        "statement": False,
        "is_set": False
    },
    "Lambda": {
        "description": "Lambda expression",
        "statement": False,
        "is_set": False
    },
    # Operators
    "BoolOp": {
        "description": "Boolean operation (and, or)",
        "statement": False,
        "is_set": False
    },
    "BinOp": {
        "description": "Binary operation (+, -, *, /)",
        "statement": False,
        "is_set": False
    },
    "UnaryOp": {
        "description": "Unary operation (not, ~, +, -)",
        "statement": False,
        "is_set": False
    },
    "Compare": {
        "description": "Comparison operation",
        "statement": False,
        "is_set": False
    },
    # Special
    "Delete": {
        "description": "Delete statement",
        "statement": True,
        "is_set": True
    },
    "Assert": {
        "description": "Assert statement",
        "statement": True,
        "is_set": False
    },
    "Raise": {
        "description": "Raise exception",
        "statement": True,
        "is_set": False
    },
    "Pass": {
        "description": "Pass statement",
        "statement": True,
        "is_set": False
    },
    "Yield": {
        "description": "Yield expression",
        "statement": False,
        "is_set": False
    },
    "YieldFrom": {
        "description": "Yield From expression",
        "statement": False,
        "is_set": False
    },
    "Await": {
        "description": "Await expression",
        "statement": False,
        "is_set": False
    },
    "Global": {
        "description": "Global declaration",
        "statement": True,
        "is_set": False
    },
    "Nonlocal": {
        "description": "Nonlocal declaration",
        "statement": True,
        "is_set": False
    },
    # Subscripting
    "Subscript": {
        "description": "Subscript operation",
        "statement": False,
        "is_set": False
    },
    "Slice": {
        "description": "Slice operation",
        "statement": False,
        "is_set": False
    },
    "Starred": {
        "description": "Starred expression (*args)",
        "statement": False,
        "is_set": False
    },
    # Comprehension parts
    "comprehension": {
        "description": "Comprehension clauses",
        "statement": False,
        "is_set": False
    },
    "alias": {
        "description": "Import alias",
        "statement": False,
        "is_set": False
    }
}
