
"""
Core tree data structures.

This module contains the core Tree and Leaf classes used across the project.
"""

from dataclasses import dataclass, field
from json import dumps, loads
from typing import Any, Dict, Generic, List, NamedTuple, Optional, TypeVar, Union

T = TypeVar('T')
L = TypeVar('L', bound='Leaf')

class Position:
    def __init__(self, 
                 start: Optional[int] = None,
                 end: Optional[int] = None,
                 info: Optional[Any] = None):
        self.start = start
        self.end = end
        self.info = info
        self._lineno: Optional[int] = None
        self._end_lineno: Optional[int] = None
        self._col_offset: Optional[int] = None
        self._end_col_offset: Optional[int] = None

    @property
    def lineno(self) -> Optional[int]:
        return self._lineno

    @lineno.setter
    def lineno(self, value: Optional[int]) -> None:
        self._lineno = value

    @property
    def end_lineno(self) -> Optional[int]:
        return self._end_lineno

    @end_lineno.setter
    def end_lineno(self, value: Optional[int]) -> None:
        self._end_lineno = value

    @property
    def col_offset(self) -> Optional[int]:
        return self._col_offset

    @col_offset.setter
    def col_offset(self, value: Optional[int]) -> None:
        self._col_offset = value

    @property
    def end_col_offset(self) -> Optional[int]:
        return self._end_col_offset

    @end_col_offset.setter
    def end_col_offset(self, value: Optional[int]) -> None:
        self._end_col_offset = value

    @property
    def absolute_start(self) -> Optional[int]:
        return self.start if self.start is not None else None

    @property
    def absolute_end(self) -> Optional[int]:
        return self.end if self.end is not None else None
