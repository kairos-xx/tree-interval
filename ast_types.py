
# S - Creates a new statement
# E - Part of an expression
AST_TYPES = {
    # Module level
    "Module": "Root node for entire file [S]",
    "Import": "Import statement [S]",
    "ImportFrom": "From import statement [S]",
    
    # Function and Class
    "FunctionDef": "Function definition [S]",
    "AsyncFunctionDef": "Async function definition [S]", 
    "ClassDef": "Class definition [S]",
    "Return": "Return statement [S]",
    "Args": "Function arguments [E]",
    "arguments": "Function argument definitions [E]",
    
    # Variables and Assignments
    "Assign": "Assignment operation [S]",
    "AnnAssign": "Annotated assignment [S]",
    "AugAssign": "Augmented assignment (+=, -=, etc) [S]",
    "Name": "Variable or function name [E]",
    "Attribute": "Attribute access (obj.attr) [E]",
    
    # Control Flow
    "If": "If conditional statement [S]",
    "For": "For loop [S]",
    "AsyncFor": "Async for loop [S]",
    "While": "While loop [S]",
    "Break": "Break statement [S]",
    "Continue": "Continue statement [S]",
    "Try": "Try block [S]",
    "TryStar": "Try block with star [S]",
    "ExceptHandler": "Except clause [S]",
    "With": "With statement [S]",
    "AsyncWith": "Async with statement [S]",
    "Match": "Pattern matching (Python 3.10+) [S]",
    
    # Expressions
    "Expr": "Expression statement [S]",
    "Call": "Function call [E]",
    "Constant": "Literal constant [E]",
    "List": "List literal [E]",
    "Tuple": "Tuple literal [E]",
    "Dict": "Dictionary literal [E]",
    "Set": "Set literal [E]",
    "ListComp": "List comprehension [E]",
    "SetComp": "Set comprehension [E]",
    "DictComp": "Dictionary comprehension [E]",
    "GeneratorExp": "Generator expression [E]",
    "Lambda": "Lambda expression [E]",
    
    # Operators
    "BoolOp": "Boolean operation (and, or) [E]",
    "BinOp": "Binary operation (+, -, *, /) [E]",
    "UnaryOp": "Unary operation (not, ~, +, -) [E]",
    "Compare": "Comparison operation [E]",
    
    # Special
    "Delete": "Delete statement [S]",
    "Assert": "Assert statement [S]",
    "Raise": "Raise exception [S]",
    "Pass": "Pass statement [S]",
    "Yield": "Yield expression [E]",
    "YieldFrom": "Yield From expression [E]",
    "Await": "Await expression [E]",
    "Global": "Global declaration [S]",
    "Nonlocal": "Nonlocal declaration [S]",
    
    # Subscripting
    "Subscript": "Subscript operation [E]",
    "Slice": "Slice operation [E]",
    "Starred": "Starred expression (*args) [E]",
    
    # Comprehension parts
    "comprehension": "Comprehension clauses [E]",
    "alias": "Import alias [E]"
}
