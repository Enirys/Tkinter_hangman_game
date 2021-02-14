from tkinter import *
from PIL import ImageTk,Image
import random

main_menu_root = Tk()
game_root = None
credits_root = None
replay_root = None

hangman_status = 0
word = "SYRINE"
guessed = []
stages = []

screen_x = int(main_menu_root.winfo_screenwidth())
screen_y = int(main_menu_root.winfo_screenheight())
win_x = 800
win_y = 500
pos_x = (screen_x // 2) - (win_x // 2)
pos_y = (screen_y // 2) - (win_y // 2)
geo = "{}x{}+{}+{}".format(win_x,win_y,pos_x,pos_y)

def create_btn(root):
    btn_img = ImageTk.PhotoImage(Image.open("letters/a.png"))
    btn = Button(root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0)
    btn.config(image=btn_img)
    return btn

def replay_game():
    replay_root.destroy()
    guessed.clear()
    hangman_status = 0
    word = "SYRINE"
    game()

def quit_game():
    replay_root.destroy()

def end_game(message):
    game_root.destroy()
    global replay_root
    replay_root = Tk()
    replay_root.geometry(geo)
    replay_root.resizable(False, False)

    background_image = ImageTk.PhotoImage(Image.open("bgs/end.png"))
    background_label = Label(replay_root, image = background_image)
    background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    display_word_label = Label(replay_root,text = message,bg = "#002333",fg = "white")
    display_word_label.config(font=("Helvetica", 20))
    display_word_label.place(x = 250, y = 100)

    replay_btn_img = ImageTk.PhotoImage(Image.open("buttons/replay_btn.png"))
    quit_btn_img = ImageTk.PhotoImage(Image.open("buttons/quit_btn.png"))

    replay_btn = Button(replay_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = replay_game)
    replay_btn.config(image=replay_btn_img)
    replay_btn.place(x = 270, y = 220)

    quit_btn = Button(replay_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = quit_game)
    quit_btn.config(image=quit_btn_img)
    quit_btn.place(x = 270, y = 320)

    replay_root.mainloop()

def check_win():
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break
    if won:
        end_game("You won!")

    if hangman_status == 11:
        end_game("You lost! \nThe word was {}".format(word))

def key_pressed(event):
    global hangman_status
    ltr = event.char.upper()
    guessed.append(ltr)
    if ltr not in word:
        hangman_status += 1
    print(hangman_status)
    print(guessed)
    display_wordtxt = display_word()
    display_word_label = Label(game_root,text = display_wordtxt,bg = "#002333",fg = "white")
    display_word_label.config(font=("Helvetica", 20))
    display_word_label.place(x = 400, y = 200)

    check_win()

def check_btn(m):
    global hangman_status
    ltr = chr(m + 97).upper()
    guessed.append(ltr)
    if ltr not in word:
        hangman_status += 1
    print(guessed)
    print(hangman_status)
    display_hangman()
    display_wordtxt = display_word()
    display_word_label = Label(game_root,text = display_wordtxt,bg = "#002333",fg = "white")
    display_word_label.config(font=("Helvetica", 20))
    display_word_label.place(x = 400, y = 200)

    check_win()

def display_hangman():
    hangman_label = Label(game_root,image = stages[hangman_status],bg = "#002333")
    hangman_label.place(x = 100, y = 170)

def display_word():
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    return display_word

def game():
    global game_root
    game_root = Tk()
    game_root.geometry(geo)
    game_root.resizable(False, False)

    background_image = ImageTk.PhotoImage(Image.open("bgs/game.png"))
    background_label = Label(game_root, image = background_image)
    background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    letters = []

    for i in range(12):
        stages.append(ImageTk.PhotoImage(Image.open("hangmanstages/hangman" + str(i) + ".png")))

    display_hangman()

    for i in range(26):
        letters.append(ImageTk.PhotoImage(Image.open("letters/" + chr (i + 97) + ".png")))

    for i in range(26):
        btn = Button(game_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = lambda m=i: check_btn(m))
        btn.config(image=letters[i])
        btn.place(x = (i % 13) * 50 + 80, y = 400 + 50 * (i // 13))

    display_wordtxt = display_word()
    display_word_label = Label(game_root,text = display_wordtxt,bg = "#002333",fg = "white")
    display_word_label.config(font=("Helvetica", 20))
    display_word_label.place(x = 400, y = 200)

    game_root.bind("<Key>",key_pressed)

    game_root.mainloop()

def start_game():
    main_menu_root.destroy()
    game()
    
def credits_menu():
    main_menu_root.destroy()
    credits_root = Tk()
    credits_root.geometry(geo)
    credits_root.resizable(False, False)

    background_image = ImageTk.PhotoImage(Image.open("bgs/creditsmenu.png"))
    background_label = Label(credits_root, image = background_image)
    background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    credits_root.mainloop()

def main_menu():
    main_menu_root.geometry(geo)
    main_menu_root.resizable(False, False)

    background_image = ImageTk.PhotoImage(Image.open("bgs/startmenu.png"))
    background_label = Label(main_menu_root, image = background_image)
    background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    start_btn_img = ImageTk.PhotoImage(Image.open("buttons/start_btn.png"))
    credits_btn_img = ImageTk.PhotoImage(Image.open("buttons/credits_btn.png"))

    start_btn = Button(main_menu_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = start_game)
    start_btn.config(image=start_btn_img)
    start_btn.place(x = 270, y = 200)

    credits_btn = Button(main_menu_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = credits_menu)
    credits_btn.config(image=credits_btn_img)
    credits_btn.place(x = 270, y = 300)

    main_menu_root.mainloop()
main_menu()
    