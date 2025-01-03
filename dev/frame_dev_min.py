from inspect import stack
from typing import Any

from tree_interval.core.future import Future


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
    print(a.b.c.f.g)


frame_function()
