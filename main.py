#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random as rdm
import logging as log


#test git hub

def main():
    """Main program"""

    """ log level: 
    - Critical: only shows call to Value_iteration
    - Error: shows span and nb_decision_update per iteration in Value_iteration
    - Warning: shows max_value for every state in V
    - Info: shows value for every action
    - Debug: shows every states reachable and their probability

    -- Be careful when using a log level lower than Error
    This prints a lots of log and slows down the application !!!"""
    log.basicConfig(level=log.CRITICAL, filemode='w', filename="GLD.log")

    # set parameters
    # be sure to set K < N or it will cause errors
    N = 5
    K  = 2
    W  = 25
    L  = 100
    CR = 15
    CT = 100

    print(f"Computing the optimal gain and policy")
    g, d = optimalgaingld(N, K, W, L, CR, CT)
    print(f"The optimal gain is \n\tg = {g}")
    print()

    play_gld(d, N, K, W, L, CR, CT)

    return 0


###################################
#### Function to play the game ####
###################################

def play_gld(decision_helper, N, K, W, L, CR, CT):
    game = GameGld(N, K, W, L, CR, CT)
    asker = AskInput()
    print_action_liste()
    is_going = True
    turn_counter = 0
    while(is_going):
        print()
        print(f"====================")
        print(f"turn: {turn_counter}")
        turn_counter += 1
        print(game)
        if decision_helper is not None:
            state = game.get_state_int()
            best_action = decision_helper[state]
            print(f"the optimal action is {action_to_str(best_action)}")
            asker.set_best(best_action)
        action = asker.ask_input()
        if action == -1:
            is_going = False
        else:
            game.play_action(action)

###################################
#### Value iteration algorithm ####
###################################

def optimalgaingld(N, K, W, L, CR, CT):
    epsilon = .1
    max_iteration = 1000
    g, d = Value_iteration(epsilon, max_iteration, N, K, W, L, CR, CT)
    return g, d

def Value_iteration(epsilon, max_iteration, N, K, W, L, CR, CT):
    log.critical(f"starting Value_iteration epsilon: {epsilon}, max_iteration {max_iteration}")
    Etats = range(3**N)
    Actions = [0, 1, 2, 3, 4]
    # initialize Vn, Vn+1, decision
    Vn = [0. for _ in range(len(Etats))]
    Vn1 = [0. for _ in range(len(Etats))]
    decision = [0 for _ in range(len(Etats))]
    iter = 0
    span = epsilon + 1
    while(iter < max_iteration and span > epsilon):
        log.error(f"\t\t--------------------- loop: {iter} ---------------------")
        iter += 1
        nb_decisions_update = 0
        # Vn <- Vn1
        Vn = [x for x in Vn1]
        for e in Etats:
            log.warning(f"\t--- loop on state e: {e} -> {int_to_state_vec(e, N)}")
            value_max = -1
            action_max = 0
            for a in Actions:
                log.info(f"\t\t--- --- loop on action: {action_to_str(a)}")
                value = 0
                for state, proba_state in proba_reachable_states(int_to_state_vec(e, N), a, K):
                    log.debug(f"\t\t--- --- --- loop on reachable state: {state}, with probability: {proba_state}")
                    value += proba_state*reward(int_to_state_vec(e, N),a,state, W, L, CR, CT)
                    value += .5 * proba_state*Vn[state_to_int(state)] 
                value += .5 * Vn[e]
                log.info(f"\t\t--- --- value: {value}")
                # update max if needed
                if value > value_max:
                    value_max = value
                    action_max = a
            log.warning(f"\t--- value_max: {value_max}")
            # update Vn1 and d with max
            Vn1[e] = value_max
            if decision[e] != action_max:
                nb_decisions_update += 1
                decision[e] = action_max
        log.error(f"\t\tnb_decisions_update: {nb_decisions_update}")
        # update stop condition
        Vdif = [v1 - v for v1,v in  zip(Vn1, Vn)]
        span = max(Vdif) - min(Vdif)
        log.error(f"\t\tspan: {span}")
        # end of while 
    if iter >= max_iteration:
        log.critical(f"max_iteration stop condition reached")
    log.critical(f"end of Value_iteration")
    # compute g
    Vdif = [v1 - v for v1,v in  zip(Vn1, Vn)]
    g = sum(Vdif)/len(Vdif)
    return g, decision

def proba_reachable_states(state, action, K):
    if action == 0:
        # action BR
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
        # action BT
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
            return res
    if action == 2:
        # action AR
        s = activate_rabbit(state)
        return [(s, 1)]
    if action == 3:
        # action AT
        s = activate_tiger(state)
        return [(s, 1)]
    if action == 4:
        # action AD
        dino_summon_possibles=combinliste(range(len(state)), K)      #On liste tous les K-uplets de cases qui peuvent être bouffés
        res=[]
        p=1/len(dino_summon_possibles)
        for i in range(len(dino_summon_possibles)):                      #On construit chaque nouveau state
            s = [c for c in state]
            for j in dino_summon_possibles[i]:
                s[j] = 0
            res.append((s,p))                                       #On ajoute le state créé et la proba associée
        return res
    # should not be acces
    log.critical(f"proba_reachable_state is given an unexpected action: {action}")
    return [(state, 1)]

def reward(state_start, action, state_end, W, L, CR, CT):
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
        log.critical(f"reward is given an unexpected action: {action}")
        return -99999

####################################
#### Utils for Value iteration  ####
####################################

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

# Renvoie les k-uplets possibles des éléments d'une liste d'éléments 'seq'
def combinliste(seq, k):
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

#############################
#### Graphical functions ####
#############################

def action_to_str(a):
        if a == 0:
           return "BR"
        if a == 1:
           return "BT"
        if a == 2:
           return "AR"
        if a == 3:
           return "AT"
        if a == 4:
           return "AD"
        return "unknow"

def print_action_liste():
    print("| To play the game you have acces to the following action:")
    print("| -{br, bt, ar, at, ad} to play the corresponding action")
    print("| -q to quite the game")
    print("| -h to print the action liste")
    print("| -tape <Enter> to play the optimal action (if no helper set it will repeat the last action played)")

class AskInput():
    def __init__(self) -> None:
        self.best_action = -1

    def set_best(self, best):
        self.best_action = best

    def ask_input(self):
        a = self.read_input()
        self.best_action = a
        return a

    def read_input(self):
        print("-- Action selection -- ")
        action = input("Action choice: ")
        action.lower()
        while(True): 
            if action == "q":
                return -1
            if action == "br":
                return 0
            if action == "bt":
                return 1
            if action == "ar":
                return 2
            if action == "at":
                return 3
            if action == "ad":
                return 4
            if action == "" and self.best_action >= 0:
                return self.best_action
            if action == "h":
                print_action_liste()
            action = input("wrong input... Action choice: ")
            action.lower()
  
################################
#### Class to play the game ####
################################

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

    def get_state_int(self):
        return state_to_int(self.cells)

    def __str__(self) -> str:
        return f"cells: {self.cells}\nscore: {self.score}"

    def play_action(self, a):
        if a == 0:
            self.birth_rabbit()
        if a == 1:
            self.birth_tiger()
        if a == 2:
            self.activate_rabbit()
        if a == 3:
            self.activate_tiger()
        if a == 4:
            self.activate_dinosaur()

    def rdm_action(self):
        a = rdm.choice([i for i in range(5)])
        self.play_action(a)

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
            self.score -= self.L
        else :
            self.score += tiger_ate * self.W

if __name__ == "__main__":
    main()
