#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random as rdm
import logging as log


#test git hub

def main():
    """Main program"""
    # Code goes over here.
    log.basicConfig(level=log.WARNING)
    log.info(f"info")
    log.warning(f"warning")
    N = 5
    g = GameGld(N, 1, 100, 33, 15, 15)
    Game = Value_iteration(N, 2, 100, 33, 15, 15)
    V = Game[0]     #affichage de la value iteration finale
    d = Game[1]     #affichage de la policy iteration finale
    # print(f"end of Value_iteration V = {V}")
    # print(f"end of Value_iteration d = {d}")

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
    return state

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
    return state
            
def combinliste(seq, k): #Renvoie les k-uplets possibles des éléments d'une liste d'éléments 'seq'
    p = []
    i, imax = 0, 2**len(seq)-1
    while i<=imax:
        s = []
        j, jmax = 0, len(seq)-1
        while j<=jmax:
            if (i>>j)&1==1:
                s.append(seq[j])
            j += 1
        if len(s)==k:
            p.append(s)
        i += 1 
    return p            
            


def proba_reachable_states(state, action, K):
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
            return res    # On retourne une liste de tous les states atteignables avec BR avec leur proba associéee
    if action == 1:
        # BT
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
                s[i] = 2
                res.append((s, p))
            return res   # On retourne une liste de tous les states atteignables avec BR avec leur proba associéee
    if action == 2:
        # AR
        # s = [x for x in state]
        s = activate_rabbit(state)
        return [(s, 1)]
    if action == 3:
        # AT
        # s = [x for x in state]
        s = activate_tiger(state)
        return [(s, 1)]
    if action == 4:
        log.info(f"AD")
        dino_summon_possibles=combinliste(range(len(state)), K)      #On liste tous les K-uplets de cases qui peuvent être bouffés
        res=[]
        p=1/len(dino_summon_possibles)
        for i in range(len(dino_summon_possibles)):                      #On construit chaque nouveau state
            s = [c for c in state]
            for j in dino_summon_possibles[i]:
                s[j] = 0
            res.append((s,p))                                       #On ajoute le state créé et la proba associée
        log.info(f"res : {res}")
        return res
    # should not be acces
    print("OLALA GROS PB")
    return [(state, 1)]

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
        return -99999

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
    Vn = [0. for _ in range(len(Etats))]
    Vn1 = [0. for _ in range(len(Etats))]
    d = [0 for _ in range(len(Etats))]
    iter = 0
    d_diff = 0
    while(iter < 200):
        log.warning(f"-------------------")
        log.warning(f"loop iter: {iter}")
        # log.warning(f"Vn1 - Vn: {diff}")
        Vdif = [v1 - v for v1,v in  zip(Vn1, Vn)]
        log.warning(f"span(Vn1): {max(Vdif) - min(Vdif)}")
        iter += 1
        Vn = [x for x in Vn1]
        log.info(f"Vn: {Vn}")
        for e in Etats:
            log.info(f"for loop e: {e}")
            log.info(f"-> {int_to_state_vec(e, N)}")
            vmax = -1
            amax = 0
            for a in Actions:
                log.info(f"for loop a: {a}")
                v = 0
                for s, ps in proba_reachable_states(int_to_state_vec(e, N), a, K):
                    log.info(f"for loop s: {s}, ps: {ps}")
                    v += ps*reward(int_to_state_vec(e, N),a,s, N, K, W, L, CR, CT)
                    v += .5 * ps*Vn[state_to_int(s)] 
                v += .5 * Vn[e]
                # v calcule
                log.info(f"v: {v}")
                if v > vmax:
                    vmax = v
                    amax = a
            log.info(f"vmax: {vmax}")
            # on a trouve le best a et le best v pour notre etat e
            Vn1[e] = vmax
            if d[e] !=amax:
                d_diff += 1
            d[e] = amax
        log.warning(f"d_diff: {d_diff}")
        log.warning(f"g in loop : {Vn1[0] - Vn[0]}")

        # on a trouve Vn1
    return Vn1, d

def optimalgaingld(N, K, W, L, CR, CT):
    pass



def play_gld(N, K, W, L, CR, CT):
    pass


if __name__ == "__main__":
    main()
