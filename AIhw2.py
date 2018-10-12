import math
import copy
import string



N=None
mode=None
youplay=None
cell_val=None
opponent=None
turn=None
oppo=None
def readtext():
    f=open("input.txt","r")
    r=f.readlines()
    for i in range(0,len(r)):
        r[i]=r[i].replace("\n","")
    global N
    N=int(r[0])
    global mode
    mode=r[1]
    global youplay
    youplay=r[2]
    depth=int(r[3])

    for i in range(4,N+4):
        r[i]=r[i].split(' ')
    for i in range(N+4,N+N+4):
        r[i]=r[i].split()

    global cell_val    
    cell_val=r[4:N+4]
    cell_val=[[int(j) for j in cell_val[i]] for i in range(0,len(cell_val))]
    board_state=r[N+4:N+N+4]
    for i in range(0,len(board_state)):
        board_state[i]=list(board_state[i][0])
    sumX=0
    sumO=0
    score=0
    for i in range (0,len(board_state)):
        for j in range(0,len(board_state[i])):
            if board_state[i][j]=='X':
                sumX+=cell_val[i][j]
            elif board_state[i][j]=='O':
                sumO+=cell_val[i][j]
    global opponent
    if youplay=='X':
        evalnum=sumX-sumO
        opponent='O'
    else:
        evalnum=sumO-sumX
        opponent='X'
    return {'depth':depth,
            'board_state':board_state,
            'eval':evalnum,
            'move':None,
            'position':None}

def board(i,j):
    num=[a for a in range(0,N)]
    #alphabet=[key for key in string.ascii_uppercase]
    d = dict( (a, b) for a,b in zip(num, string.ascii_uppercase))
    return d[i],j+1

def minimax_decision(state):
    global d
    d={}
    a=max_value(state)
    list1=d[a]
    current_state=list1[0]
    move_type=list1[1]
    a,b=board(list1[2][1],list1[2][0])
    #f=open("C:\\Users\\tara\\Desktop\\TC\\OUTPUT\\{0}.output".format(x),"w")
    f=open("output.txt","w")
    write_list=[]
    write_list.append(a+str(b)+" "+move_type+"\n")
    temp=''
    for i in range(0,len(current_state)):
        for j in range(0,len(current_state[i])):
            temp+=current_state[i][j]
        write_list.append(temp+"\n")
        temp=''
    f.writelines(write_list)
    return 

def max_value(state):
    global turn
    turn=youplay
    global oppo
    oppo=opponent
    if cutoff_test(state):
        return state['eval']
         
    v=float("-inf")
    for i in successor(state):
        val=min_value(i)
        global d
        if (val>v):
            
            #d[val]=[i['board_state'],i['move'],i['position']]
            if val in d:
                temp=d[val]
                if i['depth']>=temp[3]:
                    d[val]=[i['board_state'],i['move'],i['position'],i['depth']]
                    
                #print(d)
            else:
                
                d[val]=[i['board_state'],i['move'],i['position'],i['depth']]
        v = max(v, val)    
    return v

def min_value(state):
    global turn
    turn=opponent
    global oppo
    oppo=youplay
    
    if cutoff_test(state):
      return state['eval']

    v=float("inf")
    for i in successor(state):
        v = min(v, max_value(i))
    return v
def alphabeta_decision(state):
    global d
    d={}
    alpha=float('-inf')
    beta=float('inf')
    a=alphabeta_max_value(state, alpha, beta)
    #print(a)
    list1=d[a]
    current_state=list1[0]
    move_type=list1[1]
    a,b=board(list1[2][1],list1[2][0])
    #f=open("C:\\Users\\tara\\Desktop\\TC\\OUTPUT\\{0}.output".format(x),"w")
    f=open("output.txt","w")
    write_list=[]
    write_list.append(a+str(b)+" "+move_type+"\n")
    temp=''
    for i in range(0,len(current_state)):
        for j in range(0,len(current_state[i])):
            temp+=current_state[i][j]
        write_list.append(temp+"\n")
        temp=''
    f.writelines(write_list)
    return
def alphabeta_max_value(state, alpha, beta):
    global turn
    turn=youplay
    global oppo
    oppo=opponent  
    if cutoff_test(state):
        return state['eval']
    
    #v = float('-inf')
    for s in successor(state):
        val=alphabeta_min_value(s, alpha, beta)
        if (val>alpha):
            global d
            if val in d:
                temp=d[val]
                if s['depth']>=temp[3]:
                    d[val]=[s['board_state'],s['move'],s['position'],s['depth']]
                    
                #print(d)
            else:
                
                d[val]=[s['board_state'],s['move'],s['position'],s['depth']]
            #d[val]=[s['board_state'],s['move'],s['position']]
            
        alpha = max(alpha, val)
        if alpha >= beta:
            return beta
    return alpha

def alphabeta_min_value(state, alpha, beta):
    #print("in min")
    global turn
    turn=opponent
    global oppo
    oppo=youplay
    if cutoff_test(state):
        return state['eval']
    
    #v = float('inf')
    for s in successor(state):
        beta = min(beta, alphabeta_max_value(s, alpha, beta))
        if beta <= alpha:
            return alpha
    return beta
    
def cutoff_test(state):
    board=state['board_state']
    depth=state['depth']
    check=False
    for i in range (0,len(board)):
        for j in range(0,len(board[i])):
            if board[i][j]=='.':
                check=True
    if depth==0:
        return True
    if check==False:
        return True
    
    return False





def find_neighbor(state,row,column):
    board=state['board_state']
    #cell=state['cell_val']
    #N=state['N']
    n=['left','right','bottom','up']
    #neighbor_val=[0,0,0,0]
    neighbor=[['n','n'],['n','n'],['n','n'],['n','n']]
    if row==0:
        neighbor[3]=['null','null']
        n[3]='null'
    else:
        neighbor[3]=[row-1,column]
        n[3]=board[row-1][column]
            
    if row==N-1:
        neighbor[2]=['null','null']
        n[2]='null'
    else:
        neighbor[2]=[row+1,column]
        n[2]=board[row+1][column]
            
    if column==0:
        neighbor[0]=['null','null']
        n[0]='null'
    else:
        neighbor[0]=[row,column-1]
        n[0]=board[row][column-1]


            
    if column==N-1:
        neighbor[1]=['null','null']
        n[1]='null'
    else:
        neighbor[1]=[row,column+1]
        n[1]=board[row][column+1]

    return neighbor,n
        
        
            

def successor(state):
    board_state=state['board_state']
    #cell_val=state['cell_val']
    #youplay=state['youplay']
    depth=state['depth']-1
    #N=state['N']
    evalnum=state['eval']
    move=state['move']
    position=state['position']
    #mode=state['mode']

    successor=[]
    
    
    #stake
    no_copy=False
    for i in range (0,len(board_state)):
        for j in range(0,len(board_state[i])):
            if no_copy==False:
                temp=copy.deepcopy(state)
            tempboard=temp['board_state']
            if tempboard[i][j]=='.':
                no_copy=False
                tempboard[i][j]=turn
                position=[i,j]
                move='Stake'
                #evalnum=eval(tempboard,cell_val,x)
                if turn==youplay:
                    evalnum=temp['eval']+cell_val[i][j]
                else:
                    evalnum=temp['eval']-cell_val[i][j]
                temp['board_state']=tempboard
                temp['eval']=evalnum
                temp['depth']=depth
                temp['position']=position
                temp['move']=move
                successor.append(temp)
            else:
                no_copy=True
                
                
        

            
    

    #raid
    no_copy=False
    for i in range (0,len(board_state)):
        for j in range(0,len(board_state[i])):
            if no_copy==False:
                temp=copy.deepcopy(state)
            tempboard=temp['board_state']
            npo,n=find_neighbor(state,i,j)
            evalnum=temp['eval']
            if tempboard[i][j]=='.':
                no_copy=False
                npo,n=find_neighbor(state,i,j)
                for a in range (0,len(n)):
                    check=False
                    if n[a]==turn:
                        found=True
                        no_conquer=True
                        check=True
                        tempboard[i][j]=turn
                        move='Raid'
                        position=[i,j]
                        #evalnum=eval(tempboard,x)
                        if turn==youplay:
                            evalnum=temp['eval']+(cell_val[i][j])
                        else:
                            evalnum=temp['eval']-(cell_val[i][j])
                        
                        
                        
                        for b in range (0,len(n)):
                            
                            if n[b]==oppo:
                                if tempboard[npo[b][0]][npo[b][1]]!=turn:
                                    
                                    no_conquer=False
                                
                                    tempboard[npo[b][0]][npo[b][1]]=turn
                                    
                                
                                    
                        
                                    if turn==youplay:
                                        evalnum+=(2*cell_val[npo[b][0]][npo[b][1]])
                                    else:
                                        evalnum-=(2*cell_val[npo[b][0]][npo[b][1]])
                                
                                    
                           
                                  
                        if no_conquer==False:
                            
                            #evalnum+=(cell_val[i][j])
                            temp['board_state']=tempboard
                            temp['eval']=evalnum 
                            temp['depth']=depth
                            temp['position']=position
                            temp['move']=move
                            successor.append(temp)
                        if check==True:
                            a=len(n)
                
                    
            else:
                no_copy=True

    return successor



                                                
if __name__ == "__main__":

    state=readtext()
    if mode=='MINIMAX':
        minimax_decision(state)
    elif mode=='ALPHABETA':
        alphabeta_decision(state)
      
