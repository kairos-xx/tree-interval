
AST_TYPES = {
    # Module level
    "Module": "Root node for entire file",
    "Import": "Import statement",
    "ImportFrom": "From import statement",
    
    # Function and Class
    "FunctionDef": "Function definition",
    "AsyncFunctionDef": "Async function definition",
    "ClassDef": "Class definition",
    "Return": "Return statement",
    "Args": "Function arguments",
    "arguments": "Function argument definitions",
    
    # Variables and Assignments
    "Assign": "Assignment operation",
    "AnnAssign": "Annotated assignment",
    "AugAssign": "Augmented assignment (+=, -=, etc)",
    "Name": "Variable or function name",
    "Attribute": "Attribute access (obj.attr)",
    
    # Control Flow
    "If": "If conditional statement",
    "For": "For loop",
    "AsyncFor": "Async for loop",
    "While": "While loop",
    "Break": "Break statement",
    "Continue": "Continue statement",
    "Try": "Try block",
    "TryStar": "Try block with star",
    "ExceptHandler": "Except clause",
    "With": "With statement",
    "AsyncWith": "Async with statement",
    "Match": "Pattern matching (Python 3.10+)",
    
    # Expressions
    "Expr": "Expression statement",
    "Call": "Function call",
    "Constant": "Literal constant",
    "List": "List literal",
    "Tuple": "Tuple literal",
    "Dict": "Dictionary literal",
    "Set": "Set literal",
    "ListComp": "List comprehension",
    "SetComp": "Set comprehension",
    "DictComp": "Dictionary comprehension",
    "GeneratorExp": "Generator expression",
    "Lambda": "Lambda expression",
    
    # Operators
    "BoolOp": "Boolean operation (and, or)",
    "BinOp": "Binary operation (+, -, *, /)",
    "UnaryOp": "Unary operation (not, ~, +, -)",
    "Compare": "Comparison operation",
    
    # Special
    "Delete": "Delete statement",
    "Assert": "Assert statement",
    "Raise": "Raise exception",
    "Pass": "Pass statement",
    "Yield": "Yield expression",
    "YieldFrom": "Yield From expression",
    "Await": "Await expression",
    "Global": "Global declaration",
    "Nonlocal": "Nonlocal declaration",
    
    # Subscripting
    "Subscript": "Subscript operation",
    "Slice": "Slice operation",
    "Starred": "Starred expression (*args)",
    
    # Comprehension parts
    "comprehension": "Comprehension clauses",
    "alias": "Import alias"
}
