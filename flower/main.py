import itertools as it
import json

from operator import mul
from collections import deque
from functools import reduce
from pprint import pprint
from typing import *


import tqdm

#
mix_d = {
    (0, 0): [(0, 1.)],
    (1, 0): [(0, 0.5), (1, 0.5)],
    (0, 1): [(0, 0.5), (1, 0.5)],
    (1, 1): [(0, 0.25), (1, 0.5), (2, 0.25)],
    (2, 0): [(1, 1.)],
    (0, 2): [(1, 1.)],
    (2, 1): [(1, 0.5), (2, 0.5)],
    (1, 2): [(1, 0.5), (2, 0.5)],
    (2, 2): [(2, 1.)]
}

def load_colors(file):
    d = {}
    
    def helper(s):
        return sum(1 for c in s if c.isupper())
    with open(file, "r") as fp:
        for line in fp.readlines():
            gene, *_, color = line.strip().split("\t")
            
            gene = (helper(gene[0:2]), helper(gene[2:4]), helper(gene[4:6]), helper(gene[6:8]))
            d[gene] = color
    return d

flower_color = load_colors("roses.csv")


class Flower:
    def __init__(self, genes):
        self.genes = tuple(genes)
        self.color = flower_color[self]
    
    def __add__(self, other) -> List[Tuple["Flower", float]]:
        res_genes = [mix_d[g] for g in zip(self.genes, other.genes)]
        
        res = []
        for p in it.product(*res_genes):
            genes, probs = zip(*p)
            prob = reduce(mul, probs)
            res.append((Flower(genes), prob))
        
        return res
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Flower):
            return self.genes == other.genes
        else:
            return self.genes == other
    def __hash__(self):
        return hash(self.genes)

    def __str__(self) -> str:
        return f"{self.code()} {self.color}"

    def __repr__(self):
        return f"{self.code()} {self.color}"
        return f"Flower({self.genes})"

    def code(self) -> str:
        gene_name = ["rr Rr RR".split(),
                     "yy Yy YY".split(),
                     "WW Ww ww".split(),
                     "ss Ss SS".split()]
        res = []
        for i, g in enumerate(self.genes):
            res.append(gene_name[i][g])
        
        return " ".join(res)

base_red = Flower([2, 0, 2, 1])
base_yellow = Flower([0, 2, 2, 0])
base_white = Flower([0, 0, 1, 0])

tgt_blue = Flower([2, 2, 0, 0])


def explore(base_flowers):
    dp = {}
    for f in base_flowers:
        dp[f] = (None, set(), 1.)
    
    flower_l = base_flowers.copy()
    
    for _ in tqdm.trange(3**4):
        for f1 in flower_l:
            _, pred_f1, prob_f1 = dp[f1]
            for f2 in flower_l:
                _, pred_f2, prob_f2 = dp[f2]

                pred_common = pred_f1 & pred_f2
                prob_common = prob_f1 * prob_f2 / reduce(mul, (dp[fi][2] for fi in pred_common), 1.)
                
                ff = f1 + f2
                
                for f, p in ff:
                    prob_f = prob_common * p
                    if not f in dp:
                        dp[f] = ((f1, f2), pred_f1 | pred_f2 | {f1, f2}, prob_f)
                    
                    elif dp[f][2] < prob_f:
                        dp[f] = ((f1, f2), pred_f1 | pred_f2 | {f1, f2}, prob_f)
        
        flower_l = list(dp)
        
    return dp


def ancestors(tgt, vocab, mem):
    if tgt in mem:
        return mem[tgt]
    
    parents, *_ = vocab[tgt]
    
    if parents is None:
        return {"color": flower_color[tgt]}
    else:
        p1, p2 = parents
        
        a1 = ancestors(p1, vocab, mem)
        mem[p1] = a1
        
        a2 = ancestors(p2, vocab, mem)
        mem[p2] = a2
        
        comb_prob = dict(p1 + p2)[tgt]
        
        return {"A": (str(p1), a1),
                "B": (str(p2), a2),
                "prob": f"{comb_prob:.03}",
                "color": flower_color[tgt]
                }
        




def main():
    flower_vocab = explore([base_red, base_white, base_yellow]) 
    # print(*flower_vocab.items(), sep="\n")
    
    
    
    pprint(ancestors(tgt_blue, flower_vocab, {}))
    
    
if __name__ == "__main__":
    main()