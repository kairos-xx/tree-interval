from typing import Any

from tree_interval.core.future import Future


def test():

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

        def frame_function_inner():
            nested = Nested()

            (nested.b.c.d) = 3
            _ = (nested.e.f.g)

        frame_function_inner()

    frame_function()


test()
