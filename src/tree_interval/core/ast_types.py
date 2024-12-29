
AST_TYPES = {
    # Module level
    "Module": {
        "description": "Root node for entire file",
        "statement": True
    },
    "Import": {
        "description": "Import statement",
        "statement": True
    },
    "ImportFrom": {
        "description": "From import statement",
        "statement": True
    },
    # Function and Class
    "FunctionDef": {
        "description": "Function definition",
        "statement": True
    },
    "AsyncFunctionDef": {
        "description": "Async function definition", 
        "statement": True
    },
    "ClassDef": {
        "description": "Class definition",
        "statement": True
    },
    "Return": {
        "description": "Return statement",
        "statement": True
    },
    "Args": {
        "description": "Function arguments",
        "statement": False
    },
    "arguments": {
        "description": "Function argument definitions",
        "statement": False
    },
    # Variables and Assignments
    "Assign": {
        "description": "Assignment operation",
        "statement": True
    },
    "AnnAssign": {
        "description": "Annotated assignment",
        "statement": True
    },
    "AugAssign": {
        "description": "Augmented assignment (+=, -=, etc)",
        "statement": True
    },
    "Name": {
        "description": "Variable or function name",
        "statement": False
    },
    "Attribute": {
        "description": "Attribute access (obj.attr)",
        "statement": False
    },
    # Control Flow
    "If": {
        "description": "If conditional statement",
        "statement": True
    },
    "For": {
        "description": "For loop",
        "statement": True
    },
    "AsyncFor": {
        "description": "Async for loop",
        "statement": True
    },
    "While": {
        "description": "While loop",
        "statement": True
    },
    "Break": {
        "description": "Break statement",
        "statement": True
    },
    "Continue": {
        "description": "Continue statement",
        "statement": True
    },
    "Try": {
        "description": "Try block",
        "statement": True
    },
    "TryStar": {
        "description": "Try block with star",
        "statement": True
    },
    "ExceptHandler": {
        "description": "Except clause",
        "statement": True
    },
    "With": {
        "description": "With statement",
        "statement": True
    },
    "AsyncWith": {
        "description": "Async with statement",
        "statement": True
    },
    "Match": {
        "description": "Pattern matching (Python 3.10+)",
        "statement": True
    },
    # Expressions
    "Expr": {
        "description": "Expression statement",
        "statement": True
    },
    "Call": {
        "description": "Function call",
        "statement": False
    },
    "Constant": {
        "description": "Literal constant",
        "statement": False
    },
    "List": {
        "description": "List literal",
        "statement": False
    },
    "Tuple": {
        "description": "Tuple literal",
        "statement": False
    },
    "Dict": {
        "description": "Dictionary literal",
        "statement": False
    },
    "Set": {
        "description": "Set literal",
        "statement": False
    },
    "ListComp": {
        "description": "List comprehension",
        "statement": False
    },
    "SetComp": {
        "description": "Set comprehension",
        "statement": False
    },
    "DictComp": {
        "description": "Dictionary comprehension",
        "statement": False
    },
    "GeneratorExp": {
        "description": "Generator expression",
        "statement": False
    },
    "Lambda": {
        "description": "Lambda expression",
        "statement": False
    },
    # Operators
    "BoolOp": {
        "description": "Boolean operation (and, or)",
        "statement": False
    },
    "BinOp": {
        "description": "Binary operation (+, -, *, /)",
        "statement": False
    },
    "UnaryOp": {
        "description": "Unary operation (not, ~, +, -)",
        "statement": False
    },
    "Compare": {
        "description": "Comparison operation",
        "statement": False
    },
    # Special
    "Delete": {
        "description": "Delete statement",
        "statement": True
    },
    "Assert": {
        "description": "Assert statement",
        "statement": True
    },
    "Raise": {
        "description": "Raise exception",
        "statement": True
    },
    "Pass": {
        "description": "Pass statement",
        "statement": True
    },
    "Yield": {
        "description": "Yield expression",
        "statement": False
    },
    "YieldFrom": {
        "description": "Yield From expression",
        "statement": False
    },
    "Await": {
        "description": "Await expression",
        "statement": False
    },
    "Global": {
        "description": "Global declaration",
        "statement": True
    },
    "Nonlocal": {
        "description": "Nonlocal declaration",
        "statement": True
    },
    # Subscripting
    "Subscript": {
        "description": "Subscript operation",
        "statement": False
    },
    "Slice": {
        "description": "Slice operation",
        "statement": False
    },
    "Starred": {
        "description": "Starred expression (*args)",
        "statement": False
    },
    # Comprehension parts
    "comprehension": {
        "description": "Comprehension clauses",
        "statement": False
    },
    "alias": {
        "description": "Import alias",
        "statement": False
    }
}
