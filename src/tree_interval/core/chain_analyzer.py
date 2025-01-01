
import ast
from inspect import currentframe, getframeinfo
from types import FrameType
from typing import Optional, Tuple

class ChainAnalyzer:
    """Analyzes attribute chains to determine if they end in assignment."""
    
    @staticmethod
    def get_source_segment(frame: FrameType) -> Optional[str]:
        """Get the source code segment for the current frame."""
        info = getframeinfo(frame, 1)
        if info.code_context:
            return info.code_context[0].strip()
        return None
        
    @staticmethod
    def parse_chain(source: str) -> Tuple[bool, list[str]]:
        """Parse the attribute chain and determine if it ends in assignment."""
        try:
            tree = ast.parse(source)
            if isinstance(tree.body[0], ast.Assign):
                # This is an assignment
                target = tree.body[0].targets[0]
                chain = []
                while isinstance(target, ast.Attribute):
                    chain.append(target.attr)
                    target = target.value
                if isinstance(target, ast.Name):
                    chain.append(target.id)
                chain.reverse()
                return True, chain
            elif isinstance(tree.body[0], ast.Expr):
                # This is an expression (like a.b.c)
                value = tree.body[0].value
                chain = []
                while isinstance(value, ast.Attribute):
                    chain.append(value.attr)
                    value = value.value
                if isinstance(value, ast.Name):
                    chain.append(value.id)
                chain.reverse()
                return False, chain
        except:
            pass
        return False, []

    @classmethod
    def should_create_attr(cls, name: str, frame_offset: int = 0) -> bool:
        """
        Determine if an attribute should be created based on the chain analysis.
        
        Args:
            name: The attribute name being accessed
            frame_offset: Number of frames to skip
            
        Returns:
            bool: True if the attribute should be created
        """
        frame = currentframe()
        for _ in range(frame_offset + 1):
            if frame is None:
                return False
            frame = frame.f_back
            
        if frame is None:
            return False
            
        source = cls.get_source_segment(frame)
        if not source:
            return False
            
        is_assignment, chain = cls.parse_chain(source)
        
        # If it's an assignment and this attribute appears in the chain
        # before the final position, we should create it
        if is_assignment and name in chain[:-1]:
            return True
            
        return False
