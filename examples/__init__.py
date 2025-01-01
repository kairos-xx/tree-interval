"""Demo for the tree-visualizer package."""
from . import demo, rich_printer_examples, styling_examples


def run_demos():
    try:
        demo.run_demo()
    except Exception as e:
        print(e)
    try:
        rich_printer_examples.run_demo()
    except Exception as e:
        print(e)
    try:
        styling_examples.run_demo()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    run_demos()
