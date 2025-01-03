
"""Future class for dynamic attribute handling."""

from inspect import Frame
from typing import Any, Optional, Union

from tree_interval.core.frame_analyzer import FrameAnalyzer


class Future:
    """Dynamic attribute handling with context tracking."""

    def __init__(
        self,
        name: str,
        frame: Union[Frame, int, None] = None,
        instance: Optional[Any] = None,
        new_return: Optional[Any] = None,
    ) -> None:
        self.name = name
        self._instance = instance
        self._frame = frame if isinstance(frame, Frame) else None
        self._new_return = new_return
        self._analyzer = None
        
        if isinstance(frame, int):
            try:
                import inspect
                frame_info = inspect.stack()[frame]
                self._frame = frame_info.frame
                self._analyzer = FrameAnalyzer(frame_info)
            except (IndexError, AttributeError):
                pass

    def __getattr__(self, name: str) -> "Future":
        if self._new_return is not None:
            return Future(
                name,
                instance=self._new_return,
                new_return=type(self._new_return)(),
            )
        return Future(name, instance=self)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ("name", "_instance", "_frame", "_analyzer", "_new_return"):
            super().__setattr__(name, value)
            return

        if self._instance is not None:
            if not hasattr(self._instance, "__dict__"):
                self._instance.__dict__ = {}
            
            if not hasattr(self._instance, self.name):
                self._instance.__dict__[self.name] = type(self._instance)()
            
            target = self._instance.__dict__[self.name]
            
            if not hasattr(target, "__dict__"):
                target.__dict__ = {}
            
            target.__dict__[name] = value
