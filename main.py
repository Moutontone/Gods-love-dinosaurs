#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random as rdm
import logging as log


def main():
    """Main program"""
    # Code goes over here.
    # g = GameGld(10, 3, 100, -33, 15, 15)
    games = [GameGld(10, 3, 100, -33, 15, 15) for _ in range(50)]
    log.basicConfig(level=log.DEBUG)
    for _ in range(100):
        for g in games:
            g.rdm_action()
    scores = [g.score for g in games]
    log.info(f"scores: {scores}")
    log.info(f"moy scores: {sum(scores)/len(scores)}")


    return 0


class GameGld:
    # 0: empty cell
    # 1: rabbit cell
    # 2: tiger cell
    score = 0

    def __init__(self, N, K, W, L, CR, CT) -> None:
        # set attributs
        self.N = N
        self.K = K
        self.W = W
        self.L = L
        self.CR = CR
        self.CT = CT
        self.cells = [0 for _ in range(N)]

    def __str__(self) -> str:
        return f"cells: {self.cells}\nscore: {self.score}"

    def rdm_action(self):
        a = rdm.choice([i for i in range(5)])
        if a == 0:
            log.info(f"action BR")
            self.birth_rabbit()
        if a == 1:
            log.info(f"action BT")
            self.birth_tiger()
        if a == 2:
            log.info(f"action AR")
            self.activate_rabbit()
        if a == 3:
            log.info(f"action AT")
            self.activate_tiger()
        if a == 4:
            log.info(f"action AD")
            self.activate_dinosaur()

    def birth_rabbit(self):
        self.score -= self.CR
        ind_empty = []
        for ind, c in enumerate(self.cells):
            if c == 0:
                ind_empty.append(ind)
        if not ind_empty:
            log.warning("birth_rabbit with no empty cell")
            return
        self.cells[rdm.choice(ind_empty)] = 1

    def birth_tiger(self):
        self.score -= self.CT
        ind_empty = []
        for ind, c in enumerate(self.cells):
            if c == 0:
                ind_empty.append(ind)
        if not ind_empty:
            log.warning("birth_tiger with no empty cell")
            return
        self.cells[rdm.choice(ind_empty)] = 2

    def activate_rabbit(self):
        ind_rabbit = []
        for ind, c in enumerate(self.cells):
            if c == 1:
                ind_rabbit.append(ind)
        for ind in ind_rabbit:
            if self.cells[ind - 1] == 0:
                self.cells[ind - 1] = 1
            if self.cells[(ind + 1) % self.N] == 0:
                self.cells[(ind + 1) % self.N] = 1

    def activate_tiger(self):
        ind_tiger = []
        for ind, c in enumerate(self.cells):
            if c == 2:
                ind_tiger.append(ind)
        for ind in ind_tiger:
            self.cells[ind] = 0
            if self.cells[(ind + 1) % self.N] == 1:
                self.cells[(ind + 1) % self.N] = 2
            if self.cells[(ind + 2) % self.N] == 1:
                self.cells[(ind + 2) % self.N] = 2

    def activate_dinosaur(self):
        tiger_ate = 0
        rabbit_ate = 0
        for i in rdm.choices([i for i in range(self.N)], k=self.K):
            if self.cells[i] == 1:
                rabbit_ate += 1
            if self.cells[i] == 2:
                tiger_ate += 1
            self.cells[i] = 0


        if tiger_ate + rabbit_ate == 0:
            self.score += self.L
        else :
            self.score += tiger_ate * self.W


def optimalgaingld(N, K, W, L, CR, CT):
    pass
    # V0 = 


def play_gld(N, K, W, L, CR, CT):
    pass


if __name__ == "__main__":
    main()
