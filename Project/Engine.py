import pygame as p
class Game():
    def __init__(self):
        self.board=[]
        file = open('Board_Initial.txt','r')
        for line in file:
            self.board.append(line.split())
        file.close()        
        self.move_functions={'p':self.pawn_moves, 'R':self.rook_moves, 'N':self.knight_moves, 'B':self.bishop_moves, 'Q':self.queen_moves, 'K':self.king_moves}
        self.white_to_move=True
        self.moveLog=[]
        self.white_king_pos=(7,4)
        self.black_king_pos=(0,4)
        self.checkmate=False
        self.stalemate=False
        self.en_passant_pos=()

    def make_move(self,move,piece=''):
        self.board[move.from_row][move.from_col]="--"
        self.board[move.to_row][move.to_col]=move.piece_moved   
        self.moveLog.append(move)
        self.white_to_move=not self.white_to_move
        if move.piece_moved=="wK":
           self.white_king_pos=(move.to_row,move.to_col)
        elif move.piece_moved=="bK":
           self.black_king_pos=(move.to_row,move.to_col)
        file=open('Board.txt','w')
        for x in self.board:
            for i in x:
                file.write(i+" ")
            file.write("\n")
        file.close()
        if move.en_passant==True:
            self.board[move.from_row][move.to_col]='--'
        if move.pawn_promotion:
            self.board[move.to_row][move.to_col]=move.piece_moved[0]+piece
        if move.piece_moved[1]=='p'and abs(move.from_row-move.to_row)==2:
            self.en_passant_pos=((move.from_row+move.to_row)//2,move.from_col)
        else:
            self.en_passant_pos=()
        if move.qside_castle==True:
            self.board[move.from_row][move.from_col-1]=move.piece_moved[0]+'R'
            self.board[move.from_row][move.to_col-2]='--'
        if move.kside_castle==True:
            self.board[move.from_row][move.to_col-1]=move.piece_moved[0]+'R'
            self.board[move.from_row][move.to_col+1]='--'

    def undo_move(self):
        if len(self.moveLog)!=0:
            move=self.moveLog.pop()
            self.board[move.from_row][move.from_col]=move.piece_moved
            self.board[move.to_row][move.to_col]=move.piece_captured
            self.white_to_move=not self.white_to_move
            if move.piece_moved=="wK":
                self.white_king_pos=(move.from_row,move.from_col)
            elif move.piece_moved=="bK":
                self.black_king_pos=(move.from_row,move.from_col)
            file=open('Board.txt','w')
            for x in self.board:
                for i in x:
                    file.write(i+" ")
                file.write("\n")
            file.close()

    def all_possible_moves(self):
        moves_dict={}
        for r in range(8):
            for c in range(8):
                piece=self.board[r][c]
                if (piece[0]=='w' and self.white_to_move) or (piece[0]=='b' and not self.white_to_move):
                    self.move_functions[piece[1]](r,c,moves_dict)                         
        return moves_dict
    
    def only_valid_moves(self):
        temp_en_passant=self.en_passant_pos
        c=0
        moves_dict=self.all_possible_moves()
        for k,v in moves_dict.items():
            for i in range(len(v)-1,-1,-1):
                self.make_move(v[i])
                self.white_to_move=not self.white_to_move
                if self.in_check():
                    v.remove(v[i])
                self.white_to_move=not self.white_to_move
                self.undo_move()
            moves_dict[k]=v
            
            if len(v)>0:
                c+=1
        if c==0:
            if self.in_check():
                self.checkmate=True
            else:
                self.stalemate=True
        else:
            self.checkmate=False
            self.stalemate=False
        self.en_passant_pos=temp_en_passant
        return moves_dict

    def in_check(self):
        if self.white_to_move:
            return self.square_threatened(self.white_king_pos[0],self.white_king_pos[1])
        else:
            return self.square_threatened(self.black_king_pos[0],self.black_king_pos[1])

    def square_threatened(self,r,c):
        self.white_to_move=not self.white_to_move
        against_moves=self.all_possible_moves()
        self.white_to_move=not self.white_to_move
        for v in against_moves.values():
            for move in v:
                if move.to_row==r and move.to_col==c:
                    return True
        return False

    def pawn_moves(self,r,c,moves_dict):
        moves=[]
        if self.white_to_move:
            if self.board[r-1][c]=='--':
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=='--':
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c>0 and self.board[r-1][c-1][0]=='b':
                moves.append(Move((r,c),(r-1,c-1),self.board))
            elif c>0 and (r-1,c-1)==self.en_passant_pos:
                moves.append(Move((r,c),(r-1,c-1),self.board))
            if c<7 and self.board[r-1][c+1][0]=='b':
                moves.append(Move((r,c),(r-1,c+1),self.board))
            elif c<7 and (r-1,c+1)==self.en_passant_pos:
                moves.append(Move((r,c),(r-1,c+1),self.board))    
        else:
            if self.board[r+1][c]=='--':
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=='--':
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c>0 and self.board[r+1][c-1][0]=='w':
                moves.append(Move((r,c),(r+1,c-1),self.board))
            elif c>0 and (r+1,c-1)==self.en_passant_pos:
                moves.append(Move((r,c),(r+1,c-1),self.board))
            if c<7 and self.board[r+1][c+1][0]=='w':
                moves.append(Move((r,c),(r+1,c+1),self.board))
            elif c<7 and (r+1,c+1)==self.en_passant_pos:
                moves.append(Move((r,c),(r+1,c+1),self.board))
        moves_dict[(r,c)]=moves

    def rook_moves(self,r,c,moves_dict):
        moves=[]
        for i in range(1,8):
            if r+i<=7:
                if self.board[r+i][c]=='--':
                    moves.append(Move((r,c),(r+i,c),self.board))
                elif self.white_to_move==('w'==self.board[r+i][c][0]):
                    break
                else:
                    moves.append(Move((r,c),(r+i,c),self.board))
                    break
        for i in range(1,8):
            if r-i>=0:
                if self.board[r-i][c]=='--':
                    moves.append(Move((r,c),(r-i,c),self.board))
                elif self.white_to_move==('w'==self.board[r-i][c][0]):
                    break
                else:
                    moves.append(Move((r,c),(r-i,c),self.board))
                    break
        for i in range(1,8):
            if c+i<=7:
                if self.board[r][c+i]=='--':
                    moves.append(Move((r,c),(r,c+i),self.board))
                elif self.white_to_move==('w'==self.board[r][c+i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r,c+i),self.board))
                    break
        for i in range(1,8):
            if c-i>=0:
                if self.board[r][c-i]=='--':
                    moves.append(Move((r,c),(r,c-i),self.board))
                elif self.white_to_move==('w'==self.board[r][c-i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r,c-i),self.board))
                    break
        moves_dict[(r,c)]=moves

    def knight_moves(self,r,c,moves_dict):
        moves=[]
        if r+2<=7 and c+1<=7:
            if self.board[r+2][c+1]=='--':
                moves.append(Move((r,c),(r+2,c+1),self.board))
            elif (self.board[r+2][c+1][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r+2,c+1),self.board))
        if r+2<=7 and c-1>=0:
            if self.board[r+2][c-1]=='--':
                moves.append(Move((r,c),(r+2,c-1),self.board))
            elif (self.board[r+2][c-1][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r+2,c-1),self.board))        
        if r-2>=0 and c+1<=7:
            if self.board[r-2][c+1]=='--':
                moves.append(Move((r,c),(r-2,c+1),self.board))
            elif (self.board[r-2][c+1][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r-2,c+1),self.board))
        if r-2>=0 and c-1>=0:
            if self.board[r-2][c-1]=='--':
                moves.append(Move((r,c),(r-2,c-1),self.board))
            elif (self.board[r-2][c-1][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r-2,c-1),self.board))
        if r+1<=7 and c+2<=7:
            if self.board[r+1][c+2]=='--':
                moves.append(Move((r,c),(r+1,c+2),self.board))
            elif (self.board[r+1][c+2][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r+1,c+2),self.board))
        if r+1<=7 and c-2>=0:
            if self.board[r+1][c-2]=='--':
                moves.append(Move((r,c),(r+1,c-2),self.board))
            elif (self.board[r+1][c-2][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r+1,c-2),self.board))
        if r-1>=0 and c+2<=7:
            if self.board[r-1][c+2]=='--':
                moves.append(Move((r,c),(r-1,c+2),self.board))
            elif (self.board[r-1][c+2][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r-1,c+2),self.board))
        if r-1>=0 and c-2>=0:
            if self.board[r-1][c-2]=='--':
                moves.append(Move((r,c),(r-1,c-2),self.board))
            elif (self.board[r-1][c-2][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r-1,c-2),self.board))
        moves_dict[(r,c)]=moves

    def bishop_moves(self,r,c,moves_dict):
        moves=[]
        for i in range(1,8):
            if r+i<=7 and c+i<=7:
                if self.board[r+i][c+i]=='--':
                    moves.append(Move((r,c),(r+i,c+i),self.board))
                elif self.white_to_move==('w'==self.board[r+i][c+i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r+i,c+i),self.board))
                    break
        for i in range(1,8):
            if r-i>=0 and c+i<=7:
                if self.board[r-i][c+i]=='--':
                    moves.append(Move((r,c),(r-i,c+i),self.board))
                elif self.white_to_move==('w'==self.board[r-i][c+i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r-i,c+i),self.board))
                    break
        for i in range(1,8):
            if r+i<=7 and c-i>=0:
                if self.board[r+i][c-i]=='--':
                    moves.append(Move((r,c),(r+i,c-i),self.board))
                elif self.white_to_move==('w'==self.board[r+i][c-i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r+i,c-i),self.board))
                    break
        for i in range(1,8):
            if r-i>=0 and c-i>=0:
                if self.board[r-i][c-i]=='--':
                    moves.append(Move((r,c),(r-i,c-i),self.board))
                elif self.white_to_move==('w'==self.board[r-i][c-i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r-i,c-i),self.board))
                    break
        moves_dict[(r,c)]=moves

    def queen_moves(self,r,c,moves_dict):
        moves=[]
        for i in range(1,8):
            if r+i<=7 and c+i<=7:
                if self.board[r+i][c+i]=='--':
                    moves.append(Move((r,c),(r+i,c+i),self.board))
                elif self.white_to_move==('w'==self.board[r+i][c+i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r+i,c+i),self.board))
                    break
        for i in range(1,8):
            if r-i>=0 and c+i<=7:
                if self.board[r-i][c+i]=='--':
                    moves.append(Move((r,c),(r-i,c+i),self.board))
                elif self.white_to_move==('w'==self.board[r-i][c+i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r-i,c+i),self.board))
                    break
        for i in range(1,8):
            if r+i<=7 and c-i>=0:
                if self.board[r+i][c-i]=='--':
                    moves.append(Move((r,c),(r+i,c-i),self.board))
                elif self.white_to_move==('w'==self.board[r+i][c-i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r+i,c-i),self.board))
                    break
        for i in range(1,8):
            if r-i>=0 and c-i>=0:
                if self.board[r-i][c-i]=='--':
                    moves.append(Move((r,c),(r-i,c-i),self.board))
                elif self.white_to_move==('w'==self.board[r-i][c-i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r-i,c-i),self.board))
                    break
        for i in range(1,8):
            if r+i<=7:
                if self.board[r+i][c]=='--':
                    moves.append(Move((r,c),(r+i,c),self.board))
                elif self.white_to_move==('w'==self.board[r+i][c][0]):
                    break
                else:
                    moves.append(Move((r,c),(r+i,c),self.board))
                    break
        for i in range(1,8):
            if r-i>=0:
                if self.board[r-i][c]=='--':
                    moves.append(Move((r,c),(r-i,c),self.board))
                elif self.white_to_move==('w'==self.board[r-i][c][0]):
                    break
                else:
                    moves.append(Move((r,c),(r-i,c),self.board))
                    break
        for i in range(1,8):
            if c+i<=7:
                if self.board[r][c+i]=='--':
                    moves.append(Move((r,c),(r,c+i),self.board))
                elif self.white_to_move==('w'==self.board[r][c+i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r,c+i),self.board))
                    break
        for i in range(1,8):
            if c-i>=0:
                if self.board[r][c-i]=='--':
                    moves.append(Move((r,c),(r,c-i),self.board))
                elif self.white_to_move==('w'==self.board[r][c-i][0]):
                    break
                else:
                    moves.append(Move((r,c),(r,c-i),self.board))
                    break
        moves_dict[(r,c)]=moves

    def king_moves(self,r,c,moves_dict):
        moves=[]
        if r+1<=7 and c+1<=7:
            if self.board[r+1][c+1]=='--':
                moves.append(Move((r,c),(r+1,c+1),self.board))
            elif (self.board[r+1][c+1][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r+1,c+1),self.board))
        if r+1<=7 and c-1>=0:
            if self.board[r+1][c-1]=='--':
                moves.append(Move((r,c),(r+1,c-1),self.board))
            elif (self.board[r+1][c-1][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r+1,c-1),self.board))
        if r+1<=7:
            if self.board[r+1][c]=='--':
                moves.append(Move((r,c),(r+1,c),self.board))
            elif (self.board[r+1][c][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r+1,c),self.board))
        if c+1<=7:
            if self.board[r][c+1]=='--':
                moves.append(Move((r,c),(r,c+1),self.board))
            elif (self.board[r][c+1][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r,c+1),self.board))
        if c-1>=0:
            if self.board[r][c-1]=='--':
                moves.append(Move((r,c),(r,c-1),self.board))
            elif (self.board[r][c-1][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r,c-1),self.board))
        if r-1>=0 and c+1<=7:
            if self.board[r-1][c+1]=='--':
                moves.append(Move((r,c),(r-1,c+1),self.board))
            elif (self.board[r-1][c+1][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r-1,c+1),self.board))
        if r-1>=0 and c-1>=0:
            if self.board[r-1][c-1]=='--':
                moves.append(Move((r,c),(r-1,c-1),self.board))
            elif (self.board[r-1][c-1][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r-1,c-1),self.board))
        if r-1>=0:
            if self.board[r-1][c]=='--':
                moves.append(Move((r,c),(r-1,c),self.board))
            elif (self.board[r-1][c][0]=='w')!=self.white_to_move:
                moves.append(Move((r,c),(r-1,c),self.board))
        moves_dict[(r,c)]=moves    
        

class Move():
    def __init__(self, from_pos, to_pos, board):
        self.from_row=from_pos[0]
        self.from_col=from_pos[1]
        self.to_row=to_pos[0]
        self.to_col=to_pos[1]
        self.piece_moved=board[self.from_row][self.from_col]
        self.piece_captured=board[self.to_row][self.to_col]
        self.moveID=self.from_row*1000+self.from_col*100+self.to_row*10+self.to_col
        self.pawn_promotion=False
        if (self.piece_moved=='wp'and self.to_row==0) or (self.piece_moved=='bp'and self.to_row==7):
            self.pawn_promotion=True
        self.en_passant=False
        self.qside_castle=False
        self.kside_castle=False

    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID==other.moveID
        return False

    rank_row = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    row_rank = {v: k for k, v in rank_row.items()}
    file_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    col_file = {v: k for k, v in file_col.items()}

    def rank_file(self, r, c):
        return self.col_file[c] + self.row_rank[r]

    def from_to_notation(self):
        return self.rank_file(self.from_row, self.from_col) + self.rank_file(self.to_row, self.to_col)
