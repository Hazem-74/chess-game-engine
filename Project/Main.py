import pygame as p
import Engine 
pieces_images={}
def main():
    p.init()
    screen=p.display.set_mode((512,512))
    clock=p.time.Clock()
    game_icon = p.image.load('Icon.png')
    gs=Engine.Game()
    valid_moves=gs.only_valid_moves()
    move_made=False
    import_pieces()
    running=True
    selected_square=()
    click_pair=[] 
    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False
            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos()
                col=location[0]//64
                row=location[1]//64
                if selected_square==(row,col):
                    selected_square=()
                    click_pair=[]
                else:
                    selected_square=(row,col)
                    click_pair.append(selected_square)
                if len(click_pair)==2:
                    move=Engine.Move(click_pair[0],click_pair[1],gs.board)
                    print(move.from_to_notation())
                    if validate_move(move,valid_moves,gs):
                        if move.piece_moved[1]=='p' and (move.to_row,move.to_col)==gs.en_passant_pos:
                            move.en_passant=True    
                        if move.pawn_promotion:
                            piece=pawn_promotion_menu(gs)
                            gs.make_move(move,piece)
                        else:
                            gs.make_move(move)
                        move_made=True
                        selected_square=()
                        click_pair=[]
                    else:
                        click_pair=[selected_square]
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gs.undo_move()
                    move_made=True
        if move_made:
            valid_moves=gs.only_valid_moves()
            move_made=False
        draw_game(screen,gs,click_pair,valid_moves)
        draw_end(screen,gs)
        p.display.set_caption('Chess_Game')
        p.display.set_icon(game_icon)
        p.display.update()
        p.display.flip()
def import_pieces():
    pieces=["wR","wN","wB","wQ","wK","bR","bN","bB","bQ","bK","wp","bp"]
    for mat in pieces:
        pieces_images[mat]=p.transform.scale(p.image.load("Pieces/"+mat+".png"),(64,64))

def draw_board(screen, click_pair, valid_moves, gs):
    colors = [p.Color("white"),p.Color("Brown")]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * 64, r * 64, 64, 64))
    if len(click_pair)==1:
        p.draw.rect(screen,p.Color("Yellow"),p.Rect(click_pair[0][1]*64,click_pair[0][0]*64,64,64))
        valid_moves=castling_check(gs,valid_moves,click_pair[0])
        draw_moves(screen,click_pair,valid_moves)
    draw_danger(screen,gs.white_king_pos,gs.black_king_pos,gs)
    
def draw_pieces(screen,board):
    for r in range(8):
        for c in range(8):
            piece=board[r][c]
            if piece!="--":
                screen.blit(pieces_images[piece],p.Rect(c*64,r*64,64,64))

def draw_game(screen,gs,click_pair,valid_moves):
    draw_board(screen,click_pair,valid_moves,gs)
    draw_pieces(screen,gs.board)

def validate_move(move,valid_moves,gs):
    for v in valid_moves.values():
        if move in v:
            return True
    if castling(gs,move,valid_moves):
        return True
    return False


def draw_moves(screen,click_pair,valid_moves):
    if click_pair[0] in valid_moves.keys():
        for v in valid_moves[click_pair[0]]:
            p.draw.circle(screen,p.Color("Yellow"),[v.to_col*64+32,v.to_row*64+32],16,0)
    
        
def draw_danger(screen,wk,bk,gs):
    if gs.in_check():
        if gs.white_to_move:
            p.draw.rect(screen,p.Color("Red"),p.Rect(wk[1]*64,wk[0]*64,64,64))
        else:
            p.draw.rect(screen,p.Color("Red"),p.Rect(bk[1]*64,bk[0]*64,64,64))

def draw_end(screen,gs):
    if gs.checkmate:
        font=p.font.Font('comic-sans-ms/COMIC.ttf',32)
        text=font.render('CHECKMATE!!',True,p.Color("Blue"),p.Color("Green"))
        screen.blit(text,p.Rect(152,64,128,128)) 
    if gs.stalemate:
        font=p.font.Font('comic-sans-ms/COMIC.ttf',32)
        text=font.render('STALEMATE!!',True,p.Color("Blue"),p.Color("Green"))
        screen.blit(text,p.Rect(152,64,128,128))

def pawn_promotion_menu(gs):
    menu=p.display.set_mode((512,512))
    menu.fill(p.Color("Grey"))
    runner=True
    options={0:'R',1:'N',2:'B',3:'Q'}
    y=0
    while runner:
        for e in p.event.get():
            if e.type==p.QUIT:
                runner=False
            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos()
                x=location[0]//150
                y=location[1]
            if 160>y>76:
                piece=options[x]
                runner=False
        p.display.flip()
        font=p.font.Font('comic-sans-ms/COMIC.ttf',32)
        text=font.render('Choose piece:',True,p.Color("Blue"),p.Color("Green"))
        menu.blit(text,p.Rect(152,12,64,64))
        if gs.white_to_move:
            pieces=["wR","wN","wB","wQ"]
        else:
            pieces=["bR","bN","bB","bQ"]
        for i in range(len(pieces)):
            menu.blit(pieces_images[pieces[i]],p.Rect(i*150,100,200,200))
    return piece

def castling(gs,move,valid_moves):
    for v in gs.moveLog:
        a=0; d=0; e=0; f=0; g=0; h=0; j=0; k=0; l=0; m=0
        if gs.white_to_move:
            if v.piece_moved[0]=='w':
                if v.piece_moved[1]=='K':
                    a+=1
                elif v.from_row==7 and v.from_col==0:
                    d+=1
                elif v.from_row==7 and v.from_col==7:
                    e+=1
                if a+d==0:
                    for i in range(1,4):
                        if gs.board[7][i]=='--':
                            f+=1
                    if f==3:
                        if not gs.in_check():
                            if move==Engine.Move((move.from_row,move.from_col),(move.from_row,move.from_col-2),gs.board):
                                move.qside_castle=True
                                return True
                if a+e==0:
                    for i in range(5,7):
                        if gs.board[7][i]=='--':
                            m+=1
                    if m==2:
                        if not gs.in_check():
                            if move==Engine.Move((move.from_row,move.from_col),(move.from_row,move.from_col+2),gs.board):
                                move.kside_castle=True
                                return True
        else:
            if v.piece_moved[0]=='b':
                if v.piece_moved[1]=='K':
                    g+=1
                elif v.from_row==0 and v.from_col==0:
                    h+=1
                elif v.from_row==0 and v.from_col==7:
                    j+=1
                if g+h==0:
                    for i in range(1,4):
                        if gs.board[0][i]=='--':
                            l+=1
                    if l==3:
                        if not gs.in_check():
                            if move==Engine.Move((move.from_row,move.from_col),(move.from_row,move.from_col-2),gs.board):
                                move.qside_castle=True
                                return True
                if g+j==0:
                    for i in range(5,7):
                        if gs.board[0][i]=='--':
                            k+=1
                    if k==2:
                        if not gs.in_check():
                            if move==Engine.Move((move.from_row,move.from_col),(move.from_row,move.from_col+2),gs.board):
                                move.kside_castle=True
                                return True

def castling_check(gs,valid_moves,tuple):
    for v in gs.moveLog:
        a=0; d=0; e=0; f=0; g=0; h=0; j=0; k=0; l=0; m=0
        if gs.white_to_move:
            if v.piece_moved[0]=='w':
                if v.piece_moved[1]=='K':
                    a+=1
                elif v.from_row==7 and v.from_col==0:
                    d+=1
                elif v.from_row==7 and v.from_col==7:
                    e+=1
                if a+d==0 and (v.from_row,v.from_col)==(7,0):
                    for i in range(1,4):
                        if gs.board[7][i]=='--':
                            f+=1
                    if f==3:
                        if not gs.in_check():
                                move=Engine.Move(tuple,(tuple[0],tuple[1]-2),gs.board)
                                valid_moves[tuple]=valid_moves[tuple]+[move]
                                move.qside_castle=True
                if a+e==0 and (v.from_row,v.from_col)==(7,7):
                    for i in range(5,7):
                        if gs.board[7][i]=='--':
                            m+=1
                    if m==2:
                        if not gs.in_check():
                                move=Engine.Move(tuple,(tuple[0],tuple[1]+2),gs.board)
                                valid_moves[tuple]=valid_moves[tuple]+[move]
                                move.kside_castle=True
        else:
            if v.piece_moved[0]=='b':
                if v.piece_moved[1]=='K':
                    g+=1
                elif v.from_row==0 and v.from_col==0:
                    h+=1
                elif v.from_row==0 and v.from_col==7:
                    j+=1
                if g+h==0 and (v.from_row,v.from_col)==(0,0):
                    for i in range(1,4):
                        if gs.board[0][i]=='--':
                            l+=1
                    if l==3:
                        if not gs.in_check():
                                move=Engine.Move(tuple,(tuple[0],tuple[1]-2),gs.board)
                                valid_moves[tuple]=valid_moves[tuple]+[move]
                                move.qside_castle=True
                if g+j==0 and (v.from_row,v.from_col)==(0,7):
                    for i in range(5,7):
                        if gs.board[0][i]=='--':
                            k+=1
                    if k==2:
                        if not gs.in_check():
                                move=Engine.Move(tuple,(tuple[0],tuple[1]+2),gs.board)
                                valid_moves[tuple]=valid_moves[tuple]+[move]
                                move.kside_castle=True
    return valid_moves


if __name__=="__main__":
    main()
