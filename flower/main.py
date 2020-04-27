import itertools as it
import json

from operator import mul
from collections import deque, namedtuple
from functools import reduce
from pprint import pprint
from os import path
from typing import *

# This code uses informations provided by this source: https://docs.google.com/document/d/1ARIQCUc5YVEd01D7jtJT9EEJF45m07NXhAm4fOpNvCs/mobilebasic
# All flowers rules are explained deeply an thoroughly inside.

FlowerType = NewType("FlowerType", str)
FlowerColor = NewType("FlowerColor", str)
ColorSeed = namedtuple("ColorSeed", "color seed")

# Mixing rules for any genesself.
# (gene_flower_1, gene_flower_2): [(gene_hybrid_flower, probability of apparition)]
mix_d = {
    (0, 0): [(0, 1.0)],
    (1, 0): [(0, 0.5), (1, 0.5)],
    (0, 1): [(0, 0.5), (1, 0.5)],
    (1, 1): [(0, 0.25), (1, 0.5), (2, 0.25)],
    (2, 0): [(1, 1.0)],
    (0, 2): [(1, 1.0)],
    (2, 1): [(1, 0.5), (2, 0.5)],
    (1, 2): [(1, 0.5), (2, 0.5)],
    (2, 2): [(2, 1.0)],
}


class Flower:
    COSMOS = FlowerType("__COSMOS__")
    HYACINTHS = FlowerType("__HYACINTHS__")
    LILIES = FlowerType("__LILIES__")
    MUMS = FlowerType("__MUMS__")
    PANSIES = FlowerType("__PANSIES__")
    ROSES = FlowerType("__ROSES__")
    TULIPS = FlowerType("__TULIPS__")
    VIOLETS = FlowerType("__VIOLETS__")
    WINDFLOWERS = FlowerType("__WINDFLOWERS__")

    BLACK = FlowerColor("Black")
    BLUE = FlowerColor("Blue")
    GREEN = FlowerColor("Green")
    PINK = FlowerColor("Pink")
    PURPLE = FlowerColor("Purple")
    ORANGE = FlowerColor("Orange")
    RED = FlowerColor("Red")
    YELLOW = FlowerColor("Yellow")
    WHITE = FlowerColor("White")

    # r y w s
    flower_unused_gene: Dict[FlowerType, List[int]] = {
        COSMOS: [-2],
        HYACINTHS: [-1],
        LILIES: [-2],
        MUMS: [-1],
        PANSIES: [-1],
        ROSES: [],
        TULIPS: [-2],
        VIOLETS: [-1],
        WINDFLOWERS: [-1],
    }

    def __init__(self, flower_type: FlowerType, genes: Sequence[int]):
        """
        Create a Flower based on its genes.
        Genes are represented by a sequence of 3 or 4 integers 0⩽x_i⩽2
        """
        self.type = flower_type
        self.genes = tuple(genes)

    @property
    def color(self) -> FlowerColor:
        return FlowerColor(flower_color[self].color)

    @property
    def is_seed(self) -> bool:
        return bool(flower_color[self].seed)

    @property
    def code(self) -> str:
        gene_name = [
            "rr Rr RR".split(),
            "yy Yy YY".split(),
            "WW Ww ww".split(),  # 0 is dominant over 2 for W gene.
            "ss Ss SS".split(),
        ]

        # Some flowers don't use all genes.
        for i in Flower.flower_unused_gene[self.type]:
            del gene_name[i]

        res = []
        for i, g in enumerate(self.genes):
            res.append(gene_name[i][g])

        return " ".join(res)

    def __add__(self, other) -> List[Tuple["Flower", float]]:
        """
        Compute all possible hybrids (and their probability) generated by self and another Flower.
        """
        if self.type != other.type:
            return []
        res_genes = [mix_d[g] for g in zip(self.genes, other.genes)]

        res = []
        for p in it.product(*res_genes):
            genes, probs = zip(*p)
            prob = reduce(mul, probs)
            res.append((Flower(self.type, genes), prob))

        return res

    def __eq__(self, other) -> bool:
        if isinstance(other, Flower):
            return self.type == other.type and self.genes == other.genes
        elif isinstance(other, Sequence):
            return self.genes == other
        return False

    def __hash__(self):
        return hash((self.type, self.genes))

    def __str__(self) -> str:
        return f"({self.type} {self.code} {self.color} {self.genes} {self.is_seed})"

    def __repr__(self):
        return str(self)
        return f"Flower({self.type}, {self.genes})"


FlowerDB = NewType("FlowerDB", Dict[Flower, ColorSeed])


def load_colors(file_type_couples: List[Tuple[str, FlowerType]]) -> FlowerDB:
    """
    Reads a csv file containing color information about flowers.
    """
    d = FlowerDB({})

    def helper(s, l):
        res = sum(1 for c in s if c.isupper())
        if l == "w":
            return 2 - res
        return res

    for file, flower_type in file_type_couples:
        with open(path.join("data", file), "r") as fp:
            for line in fp.readlines():
                _, gene, *_, color = line.strip().split("\t")

                gene_code = []
                for i in range(0, len(gene), 2):
                    gene_code.append(helper(gene[i : i + 2], gene[i].lower()))

                c = FlowerColor(color.split()[0])
                is_seed = len(color.split()) > 1
                d[Flower(flower_type, tuple(gene_code))] = ColorSeed(c, is_seed)
    return d


flower_color = load_colors(
    [
        ("cosmos.csv", Flower.COSMOS),
        ("hyacinths.csv", Flower.HYACINTHS),
        ("lilies.csv", Flower.LILIES),
        ("mums.csv", Flower.MUMS),
        ("pansies.csv", Flower.PANSIES),
        ("roses.csv", Flower.ROSES),
        ("tulips.csv", Flower.TULIPS),
        ("violets.csv", Flower.VIOLETS),
        ("windflowers.csv", Flower.WINDFLOWERS),
    ]
)


FlowerPedia = NewType(
    "FlowerPedia",
    Dict[Flower, Tuple[Optional[Tuple[Flower, Flower]], Set[Flower], float]],
)


# Roses seeds genes.
rose_base_red = Flower(Flower.ROSES, [2, 0, 0, 1])
rose_base_yellow = Flower(Flower.ROSES, [0, 2, 0, 0])
rose_base_white = Flower(Flower.ROSES, [0, 0, 1, 0])

# Only blue rose gene combination.
rose_tgt_blue = Flower(Flower.ROSES, [2, 2, 2, 0])


# Mums seeds genes.
mum_base_red = Flower(Flower.MUMS, [0, 0, 1])
mum_base_yellow = Flower(Flower.MUMS, [0, 2, 0])
mum_base_white = Flower(Flower.MUMS, [2, 0, 0])

# Only blue mum gene combination.
mum_tgt_green_0 = Flower(Flower.MUMS, [2, 2, 0])
mum_tgt_green_1 = Flower(Flower.MUMS, [2, 2, 1])


def universal_get(
    flower_color: FlowerPedia,
    _type: Optional[FlowerType] = None,
    _color: Optional[FlowerColor] = None,
    _seed: Optional[bool] = None
) -> List[Flower]:
    
    res = []
    
    def test_cond(val, attr):
        def test(x, val=val, attr=attr):
            if val is None:
                return True
            if not isinstance(val, Sequence):
                val = [val]
                
            if getattr(x, attr) in val:
                return True
            return False
        
        return test

    test_type = test_cond(_type, "type")
    test_color = test_cond(_color, "color")
    test_seed = test_cond(_seed, "is_seed")
    
    for flower in flower_color:
        if test_type(flower) and test_color(flower) and test_seed(flower):
            res.append(flower)
    return res


def explore(base_flowers: List[Flower]) -> FlowerPedia:
    """
    Compute best path to obtain each flower using only `base_flowers`
    """
    dp = FlowerPedia({f: (None, set(), 1.0) for f in base_flowers})

    flower_l = base_flowers.copy()

    # Floyd Warshall algorithm with no negative cycles
    # Stop when to modification are made to the FlowerPedia

    modified = True
    while modified:
        modified = False
        for f1 in flower_l:
            _, pred_f1, prob_f1 = dp[f1]
            for f2 in flower_l:
                _, pred_f2, prob_f2 = dp[f2]

                # Compute unique flowers needed to produce f1 and f2
                pred_common = pred_f1 & pred_f2
                prob_common = (
                    prob_f1
                    * prob_f2
                    / reduce(
                        mul, (dp[fi][2] for fi in pred_common), 1.0
                    )  # All flower in pred_common are counter twice in `prob_f1 * prob_f2`
                    # We must divide by `product(prob(i) for i in pred_common)`
                )

                ff = f1 + f2

                for f, p in ff:
                    prob_f = prob_common * p
                    if not f in dp:
                        dp[f] = ((f1, f2), pred_f1 | pred_f2 | {f1, f2}, prob_f)
                        modified = True

                    # We wanr to maximize overall probability of obtaining flower f.
                    elif dp[f][2] < prob_f:
                        dp[f] = ((f1, f2), pred_f1 | pred_f2 | {f1, f2}, prob_f)
                        modified = True

        # All flowers obtained so far will be mixed during next iteration of algortihm.
        flower_l = list(dp)

    return dp


def ancestors(
    tgt: Flower, flowerpedia: FlowerPedia, mem: Dict[Flower, Dict]
) -> Dict[str, Any]:
    """
    Determines best way to obtain Flower `tgt` given a `flowerpedia`
    Recursively get ancestors of `tgt`in the FlowerPedia and aggregate results.
    """
    # Memoization for speedup
    if tgt in mem:
        return mem[tgt]

    parents, *_ = flowerpedia[tgt]

    if parents is None:
        return {"color": tgt.color, "code": tgt.code}
    else:
        p1, p2 = parents

        a1 = ancestors(p1, flowerpedia, mem)
        mem[p1] = a1

        a2 = ancestors(p2, flowerpedia, mem)
        mem[p2] = a2

        comb_prob = dict(p1 + p2)[tgt]
        return {
            "code": tgt.code,
            "A": a1,
            "B": a2,
            "prob": f"{comb_prob:.03}",
            "color": tgt.color,
        }


def main():
    flowerpedia = explore(universal_get(flower_color, _type=None, _color=None, _seed=True))
    # print(*flower_vocab.items(), sep="\n")

    pprint(flowerpedia[rose_tgt_blue])
    pprint(ancestors(rose_tgt_blue, flowerpedia, {}))
    # pprint(flowerpedia[mum_tgt_green_1])
    # pprint(ancestors(mum_tgt_green_1, flowerpedia, {}))

    print([(f, flowerpedia[f]) for f in universal_get(flower_color, _type=Flower.MUMS, _color=Flower.GREEN, _seed=None)])


if __name__ == "__main__":
    main()
