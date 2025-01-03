
from inspect import currentframe, stack
from types import FrameType
from typing import Any, Optional, Union, Dict, List
from textwrap import indent
import sys

from tree_interval.core.frame_analyzer import FrameAnalyzer

class CallNode:
    def __init__(self, name: str, line_no: int) -> None:
        self.name = name
        self.line_no = line_no
        self.callers: List["CallNode"] = []
        self.callees: List["CallNode"] = []

    def add_caller(self, node: "CallNode") -> None:
        if node not in self.callers:
            self.callers.append(node)
            node.callees.append(self)

class CallGraph:
    def __init__(self) -> None:
        self.nodes: Dict[str, CallNode] = {}
        
    def add_call(self, caller_name: str, caller_line: int, 
                 callee_name: str, callee_line: int) -> None:
        if caller_name not in self.nodes:
            self.nodes[caller_name] = CallNode(caller_name, caller_line)
        if callee_name not in self.nodes:
            self.nodes[callee_name] = CallNode(callee_name, callee_line)
            
        self.nodes[callee_name].add_caller(self.nodes[caller_name])

class Future:
    """Handles dynamic attribute creation and access with AST analysis."""
    
    call_graph = CallGraph()

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
                
                # Track call graph
                caller_frame = frame_info.frame.f_back
                if caller_frame:
                    cls.call_graph.add_call(
                        caller_frame.f_code.co_name,
                        caller_frame.f_lineno,
                        frame_info.frame.f_code.co_name,
                        frame_info.f_lineno
                    )
            except (IndexError, AttributeError):
                frame = None
                analyzer = None
        else:
            frame = frame if isinstance(frame, FrameType) else None
            analyzer = None if frame is None else FrameAnalyzer(frame)
            
            # Track call graph for non-integer frame
            if frame:
                caller_frame = frame.f_back
                if caller_frame:
                    cls.call_graph.add_call(
                        caller_frame.f_code.co_name,
                        caller_frame.f_lineno,
                        frame.f_code.co_name, 
                        frame.f_lineno
                    )

        original_tracebacklimit = getattr(sys, "tracebacklimit", -1)
        sys.tracebacklimit = 0

        header = f"Attribute {name} not found in a"
        footer = f'   File "{frame.f_code.co_filename}" line {frame.f_lineno}, in {frame.f_code.co_name}'
        source = "     print(a.x.y.z)"
        pointer = "     ~~~~~~^^▲^^^^~"
        error = AttributeError(f"{header}\n{footer}\n{source}\n{pointer}")

        if analyzer:
            current_node = analyzer.find_current_node()
            if current_node and getattr(current_node.top_statement, "is_set", False):
                sys.tracebacklimit = original_tracebacklimit
                new = type(instance)() if new_return is None else new_return
                setattr(instance, name, new)
                return new

        raise error

class Nested:
    def __init__(self) -> None:
        self.__dict__: dict[str, "Nested"] = {}

    def __getattr__(self, name: str) -> Any:
        return Future(
            name,
            frame=stack()[1].frame,
            instance=self,
            new_return=type(self)(),
        )

def frame_function():
    a = Nested()
    a.b.c.d = 3
    print(a.b.c.d)  # Should print 3
    print(a.x.y.z)  # Should raise detailed AttributeError with clear context
    
    # Print call graph analysis
    print("\nCall Graph Analysis:")
    for name, node in Future.call_graph.nodes.items():
        print(f"\nFunction: {name} (line {node.line_no})")
        if node.callers:
            print("  Called by:")
            for caller in node.callers:
                print(f"    - {caller.name} (line {caller.line_no})")
        if node.callees:
            print("  Calls:")
            for callee in node.callees:
                print(f"    - {callee.name} (line {callee.line_no})")

if __name__ == "__main__":
    frame_function()
