"""Demo for the tree-visualizer package."""
from . import demo
from . import rich_printer_examples
from . import styling_examples


def run_demos():
    demo.run_demo()
    rich_printer_examples.run_demo()
    styling_examples.run_demo()


if __name__ == "__main__":
    run_demos()
