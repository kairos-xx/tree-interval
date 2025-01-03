
from inspect import currentframe, stack
from types import FrameType
from typing import Any, Optional, Union
from textwrap import indent
import sys

class Frame:
    def __init__(self, frame: FrameType):
        self.frame = frame
        self.lineno = frame.f_lineno
        self.filename = frame.f_code.co_filename
        self.name = frame.f_code.co_name

class Future:
    def __new__(
        cls,
        name: str,
        instance: object,
        frame: Optional[Union[int, FrameType]] = None,
        new_return: Optional[Any] = None,
    ) -> Any:
        if isinstance(frame, int):
            try:
                frame_info = stack()[frame]
                frame = frame_info.frame
                analyzer = FrameAnalyzer(frame_info)
            except (IndexError, AttributeError):
                frame = None
                analyzer = None
        else:
            frame = frame if isinstance(frame, FrameType) else None
            analyzer = None if frame is None else FrameAnalyzer(frame)

        original_tracebacklimit = getattr(sys, "tracebacklimit", -1)
        sys.tracebacklimit = 0

        # Generate error message from frame context
        header = f"Attribute {name} not found in a"
        footer = f'   File "{frame.f_code.co_filename}" line {frame.f_lineno}, in {frame.f_code.co_name}'
        
        # Get the source line from the frame
        source_line = None
        if frame and hasattr(frame, 'f_code'):
            try:
                import linecache
                source_line = linecache.getline(frame.f_code.co_filename, frame.f_lineno).strip()
            except:
                source_line = None
                
        source = f"     {source_line}" if source_line else "     print(a.x.y.z)"
        pointer = "     " + "~" * (source.find("." + name) - 5) + "^^▲" + "~" * (len(name) + 4)

        error = AttributeError(f"{header}\n{footer}\n{source}\n{pointer}")

        if analyzer:
            current_node = analyzer.find_current_node()
            if current_node and getattr(current_node.top_statement, "is_set", False):
                sys.tracebacklimit = original_tracebacklimit
                new = type(instance)() if new_return is None else new_return
                setattr(instance, name, new)
                return new

        raise error

class FrameAnalyzer:
    def __init__(self, frame_info):
        self.frame = Frame(frame_info.frame)

    def find_current_node(self):
        return None

class Nested:
    def __init__(self) -> None:
        self.__dict__: dict[str, "Nested"] = {}

    def __getattr__(self, name: str) -> Any:
        return Future(
            name,
            frame=1,
            instance=self,
            new_return=type(self)(),
        )

def frame_function():
    a = Nested()
    a.b.c.d = 3
    print(a.b.c.d)  # Should print 3
    print(a.x.y.z)  # Should raise detailed AttributeError with clear context

if __name__ == "__main__":
    frame_function()
