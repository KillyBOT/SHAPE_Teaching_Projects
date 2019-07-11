#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMS W4701 Artificial Intelligence - Programming Homework 2

This module contains a simple graphical user interface for Othello. 

@author: Daniel Bauer 
"""
from tkinter import *
from tkinter import scrolledtext

from othello_game import OthelloGameManager, Player, InvalidMoveError, AiTimeoutError
from othello_shared import get_possible_moves, get_score

import sys, os, time, random

import subprocess
from threading import Timer

class AiPlayerInterface(Player):

    TIMEOUT = 10

    def __init__(self, filename, color):
        self.color = color
        self.process = subprocess.Popen(['python3',filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        name = self.process.stdout.readline().decode("ASCII").strip()
        self.name = name
        self.process.stdin.write((str(color)+"\n").encode("ASCII"))
        self.process.stdin.flush()

    def timeout(self): 
        sys.stderr.write("{} timed out.".format(self.name))
        self.process.kill() 
        self.timed_out = True

    def get_move(self, manager):
        white_score, dark_score = get_score(manager.board)
        self.process.stdin.write("SCORE {} {}\n".format(white_score, dark_score).encode("ASCII"))
        self.process.stdin.flush()
        self.process.stdin.write("{}\n".format(str(manager.board)).encode("ASCII"))
        self.process.stdin.flush()

        timer = Timer(AiPlayerInterface.TIMEOUT, lambda: self.timeout())
        self.timed_out = False
        timer.start()

        # Wait for the AI call
        move_s = self.process.stdout.readline().decode("ASCII") 

        if self.timed_out:  
            raise AiTimeoutError
        timer.cancel()
        i_s, j_s = move_s.strip().split()
        i = int(i_s)
        j = int(j_s)
        return i,j 
    
    def kill(self):
        #white_score, dark_score = get_score(manager.board)
        #self.process.stdin.write("FINAL {} {}\n".format(white_score, dark_score).encode("ASCII"))
        self.process.kill() 

class OthelloGui(object):

    def __init__(self, game_manager, player1, player2):

        self.game = game_manager
        self.players = [None, player1, player2]
        self.height = self.game.dimension
        self.width = self.game.dimension 
        
        self.offset = 20
        self.cell_size = 50

        self.isOver = False

        root = Tk()
        root.wm_title("Othello")
        root.lift()
        root.attributes("-topmost", True)
        self.root = root
        self.canvas = Canvas(root,height = self.cell_size * self.height + self.offset*2,width = self.cell_size * self.width + self.offset*2, bg="black")
        self.move_label = Label(root)
        self.score_label = Label(root)
        self.game_label = Label(root)
        self.author_label = Label(root)
        self.restart_button = Button(root)
        self.current_player_canvas = Canvas(root, height = self.cell_size + self.offset*2, width = self.cell_size + self.offset*2, bg="black")
        self.text = scrolledtext.ScrolledText(root, width=70, height=10)
        self.game_label.pack(side="top")
        self.author_label.pack(side="top")
        self.score_label.pack(side="top")
        self.move_label.pack(side="top")
        self.current_player_canvas.pack()
        self.canvas.pack()
        self.text.pack()
        self.restart_button.pack()
        self.draw_board()

    def get_position(self,x,y):
        i = (x -self.offset) // self.cell_size
        j = (y -self.offset) // self.cell_size
        return i,j

    def mouse_pressed(self,event):
        i,j = self.get_position(event.x, event.y)

        try:
            player = "Dark" if self.game.current_player == 1 else "Light"
            self.log("{}: {},{}".format(player, i,j))
            self.game.play(i, j)
            self.draw_board()
            if not get_possible_moves(self.game.board, self.game.current_player):
                self.shutdown("Game Over")
            elif isinstance(self.players[self.game.current_player], AiPlayerInterface):
                self.root.unbind("<Button-1>")
                self.root.after(100,lambda: self.ai_move())
        except InvalidMoveError:
            self.log("Invalid move. {},{}".format(i,j))

    def shutdown(self, text):
        self.move_label["text"] = text 
        self.root.unbind("<Button-1>")
        if isinstance(self.players[1], AiPlayerInterface): 
            self.players[1].kill()
        if isinstance(self.players[2], AiPlayerInterface): 
            self.players[2].kill()
        self.isOver = True
 
    def ai_move(self):
        player_obj = self.players[self.game.current_player]
        try:
            i,j = player_obj.get_move(self.game)
            player = "Dark" if self.game.current_player == 1 else "Light"
            player = "{} {}".format(player_obj.name, player)
            self.log("{}: {},{}".format(player, i,j))
            self.game.play(i,j)
            self.draw_board()
            if not get_possible_moves(self.game.board, self.game.current_player):
                if get_score(self.game.board)[0] > get_score(self.game.board)[1]:
                    self.shutdown("Dark wins!")
                elif get_score(self.game.board)[0] < get_score(self.game.board)[1]:
                    self.shutdown("White wins!")
                else:
                    self.shutdown("Tie!")
            elif isinstance(self.players[self.game.current_player], AiPlayerInterface):
                self.root.after(1, lambda: self.ai_move())
            else: 
                self.root.bind("<Button-1>",lambda e: self.mouse_pressed(e))        
        except AiTimeoutError:
            self.log("{} timed out!".format(player_obj.name))
            print(self.game.board)

            for x in range(len(self.game.board)):
                for y in range(len(self.game.board)):
                    self.game.board[x][y] = 1 if self.game.current_player == 2 else 2

            self.isOver = True

    def run(self):
        if isinstance(self.players[1], AiPlayerInterface):
            self.root.after(10, lambda: self.ai_move())
        else: 
            self.root.bind("<Button-1>",lambda e: self.mouse_pressed(e))

        while self.isOver == False: 
            self.draw_board()
            self.canvas.update()

        self.isOver = True
        #self.shutdown("Game Over")
        time.sleep(4)
        self.root.destroy()
        return get_score(self.game.board)

    def draw_board(self):
        self.game_label["text"] = "Othello"
        self.game_label["fg"] = "white"
        self.game_label["bg"] = "black"
        self.game_label["font"] = "Helvetica 72 bold"

        self.draw_current_player()
        player = "Player 1: Dark" if self.game.current_player == 1 else "Player 2: Light"
        self.move_label["text"]= player
        self.score_label["text"]= "Dark {} : {} Light".format(*get_score(self.game.board)) 
        self.draw_grid()
        self.draw_disks()

        self.restart_button["text"] = "Restart Game"
        self.restart_button["command"] = self.restart_game

    def log(self, msg, newline = True): 
        self.text.insert("end","{}{}".format(msg, "\n" if newline else ""))
        self.text.see("end")
 
    def draw_grid(self):
        fillColor = "green"
        for i in range(self.height):
            for j in range(self.width):
                self.canvas.create_rectangle(i*self.cell_size + self.offset, j*self.cell_size + self.offset, (i+1)*self.cell_size + self.offset, (j+1)*self.cell_size + self.offset, fill=fillColor)
       
    def draw_disk(self, i,j, color):
        x = i * self.cell_size + self.offset
        y = j * self.cell_size + self.offset
        padding =2 
        self.canvas.create_oval(x+padding, y+padding, x+self.cell_size-padding, y+self.cell_size-padding, fill=color)
        
    def draw_disks(self):
        for i in range(self.height): 
            for j  in range(self.width): 
                if self.game.board[i][j] == 1:
                    self.draw_disk(j, i, "black")
                elif self.game.board[i][j] == 2:
                    self.draw_disk(j, i, "white")

    def draw_current_player(self):
        player = "black" if self.game.current_player == 1 else "white"
        padding = 3
        self.current_player_canvas.create_rectangle(self.offset, self.offset, self.cell_size+self.offset, self.cell_size+self.offset, fill="dark green")
        self.current_player_canvas.create_oval(self.offset+padding, self.offset+padding, self.cell_size + self.offset-padding, self.cell_size + self.offset -padding, fill="black" if self.game.current_player == 1 else "white")

    def restart_game(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

def main():

    players = []
    playerRanking = []
    gameSize = int(sys.argv[1])
    currentRound = 0
    
    for arg in sys.argv[2:]:
        players.append(arg)

    while len(players) > 1:
        nextPlayers = []

        print(" === Round {} : Current Contenders === ".format(str(currentRound)))
        currentAI = None
        for elem in players:
            currentAI = AiPlayerInterface(elem, 1)
            print(currentAI.name)
            currentAI.kill()

        print()
        while len(players) > 0:
            if len(players) == 1:
                nextPlayers.append(players.pop())
                break

            print("████████████████████████████████████████████████████████████████████████████████")

            random.shuffle(players)

            player1= players.pop()
            player2 = players.pop()

            player1Interface = AiPlayerInterface(player1,1)
            player1Name = player1Interface.name
            player1Interface.kill()

            player2Interface = AiPlayerInterface(player2,2)
            player2Name = player2Interface.name
            player2Interface.kill()

            print("Now: {} vs. {}!".format(player1Name,player2Name))

            time.sleep(5)

            game1 = OthelloGui(OthelloGameManager(dimension=gameSize), AiPlayerInterface(player1,1), AiPlayerInterface(player2,2))
            scores1 = game1.run()

            print("Current Score: {} : {} ; {} : {}".format(game1.players[1].name,scores1[0],game1.players[2].name,scores1[1]))

            time.sleep(5)

            game2 = OthelloGui(OthelloGameManager(dimension=gameSize), AiPlayerInterface(player2,1), AiPlayerInterface(player1,2))
            scores2 = game2.run()

            player1Score = scores1[0] + scores2[1]
            player2Score = scores1[1] + scores2[0]

            print("Final Score: {} : {} ; {} : {}".format(game1.players[1].name,player1Score,game1.players[2].name,player2Score))

            winner = None
            winnerName = None
            loserName = None

            if player1Score > player2Score:
                winner = player1
                winnerName = player1Name
                loserName = player2Name
            elif player2Score > player1Score:
                winner = player2
                winnerName = player2Name
                loserName = player1Name
            
            if winner == None:
                print("Tie! Both go to next round...")
                nextPlayer.append(player1)
                nextPlayer.append(player2)
            else:
                print("{} wins! {} goes to the next round.".format(winnerName,winnerName))
                nextPlayers.append(winner)
                playerRanking.insert(0, loserName)

            time.sleep(5)

        players = nextPlayers
        currentRound+=1

    currentAI = AiPlayerInterface(players[0],1)
    playerRanking.insert(0, currentAI.name)
    currentAI.kill()
    print("{} is the champion! Congratulations!!!".format(playerRanking[0]))
    print(" === Final rankings === ")
    for x in range(0, len(playerRanking)):
        print("{} : {}".format(x+1,playerRanking[x]))

if __name__ == "__main__":
    main()