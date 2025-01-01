import sys
from inspect import isframe, stack
from textwrap import indent
from types import FrameType
from typing import Any, Optional, Union
import inspect

from .frame_analyzer import FrameAnalyzer


class Future:
    """
    Handles dynamic attribute creation and access in nested object structures.

    This class provides context-aware attribute handling by analyzing
    the call stack and current execution frame to determine whether an
    attribute access is part of a setting operation
    (creating new attributes) or a getting operation (which may
    raise appropriate errors).

    Example:
        class Nested:
            def __getattr__(self, name):
                return Future(name, frame=1, instance=self)

        obj = Nested()
        obj.a.b.c = 42  # Creates nested structure
        print(obj.a.b.c)  # Prints 42
        print(obj.x.y)  # Raises AttributeError with context
    """

    def __new__(
        cls,
        name: str,
        instance: object, 
        frame: Optional[Union[int, FrameType]] = None,
        new_return: Optional[Any] = None,
    ) -> Any:
        import inspect
        
        # Get frame if not provided
        if not isframe(frame):
            frame = stack()[(frame + 1) if isinstance(frame, int) else 2].frame
        
        # Get frame source info
        frame_info = inspect.getframeinfo(frame, context=1)
        code_context = frame_info.code_context[0] if frame_info.code_context else ""
        
        # Parse the line of code
        stripped = code_context.strip()
        
        # Check for assignment operations
        is_assignment = any(op in stripped for op in ['=', '+=', '-=', '*=', '/='])
        
        # If this is an assignment, create attribute
        if is_assignment:
            parts = stripped.split('=')[0].split('.')
            cur_pos = parts.index(name) if name in parts else -1
            
            # Only create if not the last attribute
            if cur_pos >= 0 and cur_pos < len(parts) - 1:
                new = type(instance)() if new_return is None else new_return
                setattr(instance, name, new)
                return new
            
        # Otherwise raise attribute error
        raise AttributeError(f"Object has no attribute '{name}'")