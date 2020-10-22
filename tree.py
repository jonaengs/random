from dataclasses import dataclass
from typing import Union
from enum import Enum

NodeType = Enum('NodeType', "BRANCH LEAF")
BRANCH, LEAF = NodeType.BRANCH, NodeType.LEAF

@dataclass
class TreeNode:
    type: NodeType
    value: Union[str, list]

def get_value(node):
    return node.value if node.type == LEAF else "".join(map(get_value, node.value))

tree = TreeNode(BRANCH, [
    TreeNode(BRANCH, [
        TreeNode(LEAF, "a")
    ]),
    TreeNode(LEAF, "b"),
    TreeNode(LEAF, "c"),
    TreeNode(LEAF, "d"),
    TreeNode(BRANCH, [
        TreeNode(BRANCH, [
            TreeNode(LEAF, "e"),
            TreeNode(BRANCH, [
                TreeNode(LEAF, "f")
            ])
        ])
    ])
])

print(get_value(tree))



# ALTERNATIVE 2: Use two separate classes. Use OR instead of if-else. Can include type attribute, but not necessary
@dataclass
class TreeBranch:
    # type = BRANCH
    children: list

@dataclass
class TreeLeaf:
    # type = LEAF
    text: str

def get_value(node):
    return getattr(node, "text", None) or "".join(map(get_value, node.children))

# Min løsning på Ardoq-intervjuet. Trærne var skrevet i TypeScript, men så ish slik ut som de over, med type-attributtet
def __get_value(node):
    if node.type == LEAF:
        return node.text
    return map(__get_value, node.children)

tree = TreeBranch([
    TreeBranch([
        TreeLeaf("a")
    ]),
    TreeLeaf("b"),
    TreeBranch([
        TreeBranch([
            TreeLeaf("c")
        ]),
        TreeLeaf("d")
    ])
])

print(get_value(tree))



# ALTERNATIVE 3: Use namedtuple

from collections import namedtuple
Branch = namedtuple("Branch", ("children"))
Leaf = namedtuple("Leaf", ("text"))

def get_value(node):
    return getattr(node, "text", None) or "".join(map(get_value, node.children))

tree = Branch([
    Branch([
        Leaf("a")
    ]),
    Leaf("b"),
    Branch([
        Branch([
            Leaf("c")
        ]),
        Leaf("d")
    ]),
    Leaf("e")
])

print(get_value(tree))




# ALTERNATIVE 4: Subclass namedtuple. Use try/except

from typing import NamedTuple

class Branch(NamedTuple):
    children: list

class Leaf(NamedTuple):
    text: str

def get_value(node):
    return getattr(node, "text", None) or "".join(map(get_value, node.children))
    try: return node.text
    except: "".join(map(get_value, node.children))

tree = Branch([
    Branch([
        Leaf("a")
    ]),
    Leaf("b"),
    Branch([
        Branch([
            Leaf("c")
        ]),
        Leaf("d")
    ]),
    Leaf("g")
])

print(get_value(tree))



# ALTERNATIVE 5: use flag to set branch/leaf

from typing import NamedTuple

class Node(NamedTuple):
    is_leaf: bool
    value: Union[list, str]


def get_value(node):
    return (node.is_leaf and node.value) or "".join(map(get_value, node.value))

tree = Node(False, [
    Node(False, [
        Node(True, "a")
    ]),
    Node(True, "b"),
    Node(False, [
        Node(False, [
            Node(True, "c")
        ]),
        Node(True, "d")
    ]),
    Node(True, "z")
])

print(get_value(tree))



# ALTERNATIVE 6: Use dictionary


def get_value(node):
    return node.get("text") or "".join(map(get_value, node["children"]))

tree = {'children': [
    {'text': 'a'},
    {'children': [
        {'text': 'b'},
        {'text': 'c'},
        {'text': 'd'}
    ]},
    {'children': [
        {'text': 'efg'}
    ]}
]}

print(get_value(tree))


# ALTERNATIVE 7: "Utility class"

class Node:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def get_value(node):
    return node.__dict__.get("text") or "".join(map(get_value, node.children))

tree = Node(children=[
    Node(children=[
        Node(text="a")
    ]),
    Node(text="b"),
    Node(children=[
        Node(children=[
            Node(text="c")
        ]),
        Node(text="abc")
    ])
])

print(get_value(tree))



# ALTERNATIVE 8: Utility class 2

class Node:
    def __init__(self, children=None, text=None):
        # self.__dict__.update({'children': children, 'text': text})
        self.children = children
        self.text = text

def get_value(node):
    return node.text or "".join(map(get_value, node.children))

tree = Node(children=[
    Node(children=[
        Node(text="a")
    ]),
    Node(text="b"),
    Node(children=[
        Node(children=[
            Node(text="c")
        ]),
        Node(text="dcba")
    ])
])

print(get_value(tree))



# ALTERNATIVE 9: namedtuple with defaults

Node = namedtuple("Node", ("text", "children"), defaults=(None, None))

def get_value(node):
    return node.text or "".join(map(get_value, node.children))

tree = Node(children=[
    Node(children=[
        Node(text="a")
    ]),
    Node(text="b"),
    Node(children=[
        Node(children=[
            Node(text="c")
        ]),
        Node(text="namedtuplewithdefaults")
    ])
])

print(get_value(tree))




# ALTERNATIVE 10: dataclass with defaults

@dataclass
class Node:
    children: list = None
    text: str = None

def get_value(node):
    return node.text or "".join(map(get_value, node.children))

tree = Node(children=[
    Node(children=[
        Node(text="a")
    ]),
    Node(text="b"),
    Node(children=[
        Node(children=[
            Node(text="c")
        ]),
        Node(text="dataclasswithdefaults")
    ])
])

print(get_value(tree))


# ALTERNATIVE 11: tuples


def get_value(node):
    return node[0] or "".join(map(get_value, node[1]))

tree = (
    None, [
        (None, [
            ("a", )
        ]),
        ("b", ),
        (None, [
            (None, [
                ("c", )
            ]),
            ("dtuple", ) 
        ])
    ]
)

print(get_value(tree))




# ALTERNATIVE 12: very simple list (could do the exact same with a tuple)


def get_value(node):
    return node if type(node) == str else "".join(map(get_value, node))

tree = [
    "l",
    [
        "i",
        "s",
        [
            "t"
        ]
    ]
]

print(get_value(tree))

tree = ("t", ("u", "p", ("le")))
print(get_value(tree))