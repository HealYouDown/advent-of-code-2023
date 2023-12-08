from utils import get_input
from typing import Literal, Union
import re
from dataclasses import dataclass

INSTRUCTIONS = tuple[Literal["L"] | Literal["R"]]


@dataclass
class Node:
    name: str
    parent: Union["Node", None] = None
    left: Union["Node", None] = None
    right: Union["Node", None] = None

    def __repr__(self) -> str:
        return f"Node(name={self.name!r}, left={self.left.name!r}, right={self.right.name!r})"


def puzzle_1(start_node: Node, instructions: INSTRUCTIONS) -> int:
    steps = 0
    i = 0
    current_node = start_node
    while current_node.name != "ZZZ":
        instr = instructions[i % len(instructions)]
        current_node = current_node.left if instr == "L" else current_node.right
        steps += 1
        i += 1

    return steps


def puzzle_2(start_nodes: list[Node], instructions: INSTRUCTIONS) -> int:
    # FIXME: runs too long x)
    # Assumption:
    # Nodes probably start running in a circle after x instructions, so we could
    # calculate that point and do some fancy math to find the required steps so that they
    # all align at a Z node.
    steps = 0
    i = 0
    current_nodes = start_nodes
    while not all(node.name.endswith("Z") for node in current_nodes):
        instr = instructions[i % len(instructions)]
        for idx, node in enumerate(current_nodes):
            current_nodes[idx] = node.left if instr == "L" else node.right
        steps += 1
        i += 1

    return steps


if __name__ == "__main__":
    instructions_inp, nodes_inp = get_input(8).split("\n\n")
    instructions: INSTRUCTIONS = tuple(char for char in instructions_inp)

    pattern = re.compile(r"[A-Z|1-9]{3}")
    nodes_lookup: dict[str, Node] = {}
    for line in nodes_inp.splitlines():
        parent, left, right = pattern.findall(line)

        if parent in nodes_lookup:
            parent_node = nodes_lookup[parent]
        else:
            parent_node = Node(name=parent)
            nodes_lookup[parent_node.name] = parent_node

        if left in nodes_lookup:
            left_node = nodes_lookup[left]
        else:
            left_node = Node(name=left, parent=parent_node)
            nodes_lookup[left_node.name] = left_node
        parent_node.left = left_node

        if right in nodes_lookup:
            right_node = nodes_lookup[right]
        else:
            right_node = Node(name=right, parent=parent_node)
            nodes_lookup[right_node.name] = right_node
        parent_node.right = right_node

    print(puzzle_1(nodes_lookup["AAA"], instructions))
    print(
        puzzle_2(
            [node for name, node in nodes_lookup.items() if name.endswith("A")],
            instructions,
        )
    )
