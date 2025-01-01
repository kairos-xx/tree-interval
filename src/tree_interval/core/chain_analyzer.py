
import ast
from typing import Tuple, List, Optional
from dataclasses import dataclass

@dataclass
class ChainInfo:
    """Information about an attribute chain"""
    is_assignment: bool
    chain: List[str]
    assignment_type: Optional[str]

class ChainAnalyzer:
    """Analyzes attribute chains and their assignment status"""
    
    @staticmethod
    def parse_expression(code: str) -> ChainInfo:
        """Parse code and analyze the attribute chain"""
        try:
            tree = ast.parse(code)
            node = tree.body[0].value if isinstance(tree.body[0], ast.Expr) else tree.body[0]
            
            # Handle augmented assignments (+=, -=, etc)
            if isinstance(node, ast.AugAssign):
                target = node.target
                op_type = type(node.op).__name__
                chain = []
                while isinstance(target, ast.Attribute):
                    chain.append(target.attr)
                    target = target.value
                if isinstance(target, ast.Name):
                    chain.append(target.id)
                chain.reverse()
                return ChainInfo(True, chain, op_type)
            
            # Handle normal assignments
            elif isinstance(node, ast.Assign):
                target = node.targets[0]
                chain = []
                while isinstance(target, ast.Attribute):
                    chain.append(target.attr)
                    target = target.value
                if isinstance(target, ast.Name):
                    chain.append(target.id)
                chain.reverse()
                return ChainInfo(True, chain, 'Assign')
                
            # Handle attribute access without assignment
            elif isinstance(node, ast.Attribute):
                chain = []
                current = node
                while isinstance(current, ast.Attribute):
                    chain.append(current.attr)
                    current = current.value
                if isinstance(current, ast.Name):
                    chain.append(current.id)
                chain.reverse()
                return ChainInfo(False, chain, None)
                
        except:
            # Catch all exceptions silently and return a default ChainInfo
            pass
            
        return ChainInfo(False, [], None)
    
    @staticmethod
    def should_create_attr(code: str, name: str) -> bool:
        """Determine if an attribute should be created"""
        info = ChainAnalyzer.parse_expression(code)
        
        # If this is an assignment and the attribute appears in the chain
        # before the final position, create it
        if info.is_assignment and name in info.chain[:-1]:
            return True
            
        return False
