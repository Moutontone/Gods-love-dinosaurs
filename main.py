#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random as rdm
import logging as log


#test git hub

def main():
    """Main program"""
    # Code goes over here.
    N = 10
    g = GameGld(N, 3, 100, 33, 15, 15)
    print("game :")
    print(g)
    print(state_to_int(g.cells))
    print(int_to_state_vec(state_to_int(g.cells),N))
    g.rdm_action()
    g.rdm_action()
    g.rdm_action()
    g.rdm_action()
    print("game :")
    print(g)
    print(state_to_int(g.cells))
    print(int_to_state_vec(state_to_int(g.cells),N))
    g.rdm_action()
    g.rdm_action()
    g.rdm_action()
    g.rdm_action()
    print("game :")
    print(g)
    print(state_to_int(g.cells))
    print(int_to_state_vec(state_to_int(g.cells),N))


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

def activate_rabbit(state):
    ind_rabbit = []
    N = len(state)
    for ind, c in enumerate(state):
        if c == 1:
            ind_rabbit.append(ind)
    for ind in ind_rabbit:
        if state[ind - 1] == 0:
            state[ind - 1] = 1
        if state[(ind + 1) % N] == 0:
            state[(ind + 1) % N] = 1

def activate_tiger(state):
    ind_tiger = []
    N = len(state)
    for ind, c in enumerate(state):
        if c == 2:
            ind_tiger.append(ind)
    for ind in ind_tiger:
        state[ind] = 0
        if state[(ind + 1) % N] == 1:
            state[(ind + 1) % N] = 2
        if state[(ind + 2) % N] == 1:
            state[(ind + 2) % N] = 2

def proba_reachable_states(state, action):
    if action == 0:
        # BR
        ind_empty = []
        for ind, c in enumerate(state):
            if c == 0:
                ind_empty.append(ind)
        if not ind_empty:
            return [(state, 1)]
        else:
            res = []
            p = 1/ len(ind_empty)
            for i in ind_empty:
                s = [c for c in state]
                s[i] = 1
                res.append((s, p))
            return res
    if action == 1:
        # BT 
        pass
    if action == 2:
        # AR
        s = [x for x in state]
        s = activate_rabbit(s)
        return [(s, 1)]
    if action == 3:
        # AT
        s = [x for x in state]
        s = activate_tiger(s)
        return [(s, 1)]
    if action == 4:
        log.info(f"action AD")
        # TODO
        # ca fe reflechir
        return 0
    return [(1,2)]
    # tous les etats accessibles et la proba asocie

def reward(state_start, action, state_end, N, K, W, L, CR, CT):
        if action == 0:
            # BR
            return -CR
        if action == 1:
            # BT 
            return -CT
        if action == 2:
            # AR
            return 0
        if action == 3:
            # AR
            return 0
        if action == 4:
            # AD
            # count tiger and rabbit eaten
            tiger_eaten = 0
            rabbit_eaten = 0
            for i,c in enumerate(state_start):
                if c != 0 and state_end[i] == 0:
                    if c == 1:
                        rabbit_eaten += 1
                    if c == 2:
                        tiger_eaten += 1
            if tiger_eaten + rabbit_eaten == 0:
                return -L
            return tiger_eaten * W

def state_to_int(state_vec):
    res = 0
    for i,v in enumerate(state_vec):
        res += 3**i * v 
    return res

def int_to_state_vec(v, N):
    res = [0 for _ in range(N)]
    for i in range(N):
        res[i] = v%3 
        v = (v - v%3)//3
    return res

def Value_iteration(N, K, W, L, CR, CT):
    Etats = range(3**N)
    Actions = [0,1,2,3,4]
    pass
    # init V
    # V0 = [0,0, ..., 0]
    Vn = [0 for _ in range(N)]
    Vn1 = [0 for _ in range(N)]
    d = [0 for _ in range(N)]
    while(True):
        Vn = Vn1 # attention
        for e in Etats:
            vmax = -1
            amax = 0
            for a in Actions:
                v = 0
                for s, ps in proba_reachable_states(e, a):
                    v += ps*Vn[s] + ps*reward(e,a,s, N, K, W, L, CR, CT)
                # v calcule
                if v > vmax:
                    vmax = v
                    amax = a
            # on a trouve le best a et le best v pour notre etat e
            Vn1[e] = vmax
            d[e] = amax
        # on a trouve Vn1

def optimalgaingld(N, K, W, L, CR, CT):
    pass



def play_gld(N, K, W, L, CR, CT):
    pass


if __name__ == "__main__":
    main()
