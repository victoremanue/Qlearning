#Aqui vocês irão colocar seu algoritmo de aprendizado
import connection as cn
import random

alpha = 0.1
gama = 0.3

Qtable= []

def init():
    f=open("resultado.txt","r")
    txt = f.read()
    f.close()

    for row in txt.split('\n'):
        l=[]
        for colum in row.split():
            l.append(float(colum))
        Qtable.append(l)

def PrintTable():
    txt=""
    for i in range (0, 96):
        for j in range (0, 3):
            txt+=str(Qtable[i][j]) + " "
        txt+='\n'

    f=open("resultado.txt","w")
    f.write(txt)
    f.close()

def get_max(state):
    return max(Qtable[state][0], Qtable[state][1], Qtable[state][2])

def to_int(txt):
    return int(txt,2)

def updateTable(cur_state, action, new_state, reward):
    Qtable[cur_state][action]+= alpha*(reward + (gama *(get_max(new_state) - Qtable[cur_state][action])))
    

def getCmd(action):
    if action == 0:
        return "left"
    elif action == 1:
        return "right"
    else: 
        return "jump"

def get_next_action(state):
    if (Qtable[state][0] >= Qtable[state][1]) and (Qtable[state][0] >=Qtable[state][2]):
        return 0
    if (Qtable[state][1] >= Qtable[state][0]) and (Qtable[state][1] >=Qtable[state][2]):
        return 1
    return 2 


def aprendizado():
    cont = 0
    s = cn.connect(2037)
    cur_state, reward = cn.get_state_reward(s, "jump")

    while 1:
        action = get_next_action(to_int(cur_state))
        cmd = getCmd(action)
        new_state, reward = cn.get_state_reward(s, cmd)
        updateTable(to_int(cur_state), action, to_int(new_state), reward)
        cur_state = new_state
        cont+=1
        print("cont = {}".format(cont),end = "\r")
        if cont%100 == 0:
            PrintTable()
            print("atualizei")

def main():
    init()      #Inicializa a tabela de aprendizado "Qtable"
    aprendizado()

if __name__ == "__main__":
    main()