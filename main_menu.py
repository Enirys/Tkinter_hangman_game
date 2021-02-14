from tkinter import *
from PIL import ImageTk,Image
import random
from words import word_list

# Variables pour créer les fenêtres
main_menu_root = Tk()
game_root = None
players_root = None
credits_root = None
replay_root = None
choose_word_root = None

# Variables du jeu
hangman_status = 0
word = "PYTHON"
guessed = []
stages = []
letters = []
input_box = None

# Variables pour positionner la fenêtre du jeu au milieu de l'écran
screen_x = int(main_menu_root.winfo_screenwidth())
screen_y = int(main_menu_root.winfo_screenheight())
win_x = 800
win_y = 500
pos_x = (screen_x // 2) - (win_x // 2)
pos_y = (screen_y // 2) - (win_y // 2)
geo = "{}x{}+{}+{}".format(win_x,win_y,pos_x,pos_y)

# Fonction pour quitter le jeu
def quit_game():
    replay_root.destroy()

# Création de la fenêtre de fin de jeu et afficher si le joueur a gagné ou a perdu
def end_game(message):
    # Fermer la fenêtre du jeu
    game_root.destroy()
    global replay_root
    # Création et initialisation de la fenêtre de fin de jeu
    replay_root = Tk()
    replay_root.geometry(geo)
    replay_root.resizable(False, False)

    # Chargement et affichage de l'image de fond pour la fenêtre
    background_image = ImageTk.PhotoImage(Image.open("bgs/end.png"))
    background_label = Label(replay_root, image = background_image)
    background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    # Affichage du message de fin (Vous avez gangé ou vous avez perdu)
    display_word_label = Label(replay_root,text = message,bg = "#002333",fg = "white")
    display_word_label.config(font=("Helvetica", 20))
    display_word_label.place(x = 250, y = 100)

    # Chargement de l'image de fond du bouton quitter
    quit_btn_img = ImageTk.PhotoImage(Image.open("buttons/quit_btn.png"))

    # Création et affichage du bouton quitter
    quit_btn = Button(replay_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = quit_game)
    quit_btn.config(image=quit_btn_img)
    quit_btn.place(x = 270, y = 320)

    replay_root.mainloop()

# Fonction pour vérifier si l'utilisateur a gagné ou a perdu
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

# Fonction pour détecter quel bouton à été choisi par l'utilisateur pour l'afficher s'il est correct ou pour afficher
# Le stade suivant du pendu
# Si l'utilisateur utilise le clavier pour jouer
def key_pressed(event):
    global hangman_status
    ltr = event.char.upper()
    guessed.append(ltr)
    if ltr not in word:
        hangman_status += 1
    # Mise a jour de l'image du pendu
    display_hangman()

    # Affichage des lettres devinées par l'utilisateur
    display_wordtxt = display_word()
    display_word_label = Label(game_root,text = display_wordtxt,bg = "#002333",fg = "white")
    display_word_label.config(font=("Helvetica", 20))
    display_word_label.place(x = 400, y = 200)

    # Vérifier si l'utilisateur a deviné le mot ou s'il a été pendu
    check_win()

# Fonction pour détecter quel bouton à été choisi par l'utilisateur pour l'afficher s'il est correct ou pour afficher
# Le stade suivant du pendu
# Si l'utilisateur utilise les boutons affichés à l'écran
def check_btn(m):
    global hangman_status
    ltr = chr(m + 97).upper()
    guessed.append(ltr)
    if ltr not in word:
        hangman_status += 1
        
    # Mise a jour de l'image du pendu
    display_hangman()

    # Affichage des lettres devinées par l'utilisateur
    display_wordtxt = display_word()
    display_word_label = Label(game_root,text = display_wordtxt,bg = "#002333",fg = "white")
    display_word_label.config(font=("Helvetica", 20))
    display_word_label.place(x = 400, y = 200)

    # Vérifier si l'utilisateur a deviné le mot ou s'il a été pendu
    check_win()

# Fonction pour afficher le pendu
def display_hangman():
    hangman_label = Label(game_root,image = stages[hangman_status],bg = "#002333")
    hangman_label.place(x = 100, y = 170)

# Fonction pour afficher les lettres devinées par l'utilisateur
def display_word():
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    return display_word

def play_game():
    global word
    word = input_box.get()
    choose_word_root.destroy()
    game()

# Fonction principale du jeu
def game():
    global game_root
    # Création et initialisation de la fenêtre du jeu
    game_root = Tk()
    game_root.geometry(geo)
    game_root.resizable(False, False)

    # Création d'une image de fond pour la fenêtre
    background_image = ImageTk.PhotoImage(Image.open("bgs/game.png"))
    background_label = Label(game_root, image = background_image)
    background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    # Chargement des images pour le personnage du pendu
    for i in range(12):
        stages.append(ImageTk.PhotoImage(Image.open("hangmanstages/hangman" + str(i) + ".png")))

    # Affichage du personnage du pendu
    display_hangman()

    # Chargement des images de fond pour les boutons pour créer des lettres
    for i in range(26):
        letters.append(ImageTk.PhotoImage(Image.open("letters/" + chr (i + 97) + ".png")))

    # Création et affichage des 26 lettres de l'alphabet avec leurs images de fond
    # Associer à chaque lettre une fonction lambda qui permet de savoir quelle lettre à été choisie par l'utilisateur pour l'utiliser
    for i in range(26):
        btn = Button(game_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = lambda m=i: check_btn(m))
        btn.config(image=letters[i])
        btn.place(x = (i % 13) * 50 + 80, y = 400 + 50 * (i // 13))

    # Affichage des lettres devinées par l'utilisateur
    display_wordtxt = display_word()
    display_word_label = Label(game_root,text = display_wordtxt,bg = "#002333",fg = "white")
    display_word_label.config(font=("Helvetica", 20))
    display_word_label.place(x = 400, y = 200)

    # Si l'utilisateur veut joueur au clavier
    game_root.bind("<Key>",key_pressed)

    game_root.mainloop()

# Fonction pour générer un mot aléatoire de la liste
def random_word():
    global word
    word = random.choice(word_list)

# Mode de jeu Computer vs Player
def player_vs_computer():
    random_word()
    players_root.destroy()
    game()

def choose_word():
    global input_box
    global choose_word_root
    players_root.destroy()
    # Création et initialisation de la fenêtre de choix
    choose_word_root = Tk()
    choose_word_root.geometry(geo)
    choose_word_root.resizable(False, False)

    # Création d'une image de fond pour la fenêtre
    background_image = ImageTk.PhotoImage(Image.open("bgs/word.png"))
    background_label = Label(choose_word_root, image = background_image)
    background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    # Chargement des images pour les boutons
    submit_btn_img = ImageTk.PhotoImage(Image.open("buttons/submit_btn.png"))

    # Création de l'input box
    input_box = Entry(choose_word_root,bg = "white")
    input_box.place(x = 200, y = 200)

    # Création du bouton players et ajout de l'image de fond
    submit_btn = Button(choose_word_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = play_game)
    submit_btn.config(image=submit_btn_img)
    submit_btn.place(x = 260, y = 300)

    choose_word_root.mainloop()


# Mode de jeu Player vs Player
def player_vs_player():
    global word
    choose_word()

# Fenêtre pour choisir le mode de jeu
def choose_players():
    global players_root
    # Fermer la fenêtre du menu start
    main_menu_root.destroy()
    # Création et initialisation de la fenêtre de choix
    players_root = Tk()
    players_root.geometry(geo)
    players_root.resizable(False, False)

    # Création d'une image de fond pour la fenêtre
    background_image = ImageTk.PhotoImage(Image.open("bgs/players.png"))
    background_label = Label(players_root, image = background_image)
    background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    # Chargement des images pour les boutons
    players_btn_img = ImageTk.PhotoImage(Image.open("buttons/players_btn.png"))
    computer_btn_img = ImageTk.PhotoImage(Image.open("buttons/computer_btn.png"))

    # Création du bouton players et ajout de l'image de fond
    players_btn = Button(players_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = player_vs_player)
    players_btn.config(image=players_btn_img)
    players_btn.place(x = 200, y = 150)

    # Création du bouton computer et ajout de l'image de fond
    computer_btn = Button(players_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = player_vs_computer)
    computer_btn.config(image=computer_btn_img)
    computer_btn.place(x = 450, y = 150)

    players_root.mainloop()

# Fonction pour lancer le jeu à partir du bouton Start Game
def start_game():
    # Choisir le mode du jeu: Player Vs Player ou Player vs Computer
    choose_players()

# Création du menu Credits
def credits_menu():
    # Fermer la fenêtre du menu start
    main_menu_root.destroy()

    # Création et initialisation de la fenêtre credits
    credits_root = Tk()
    credits_root.geometry(geo)
    credits_root.resizable(False, False)

    # Création d'une image de fond pour la fenêtre
    background_image = ImageTk.PhotoImage(Image.open("bgs/creditsmenu.png"))
    background_label = Label(credits_root, image = background_image)
    background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    credits_root.mainloop()

# Création du menu start du jeu
def main_menu():

    # Création et initialisation de la fenêtre start
    main_menu_root.geometry(geo)
    main_menu_root.resizable(False, False)

    # Création d'une image de fond pour la fenêtre
    background_image = ImageTk.PhotoImage(Image.open("bgs/startmenu.png"))
    background_label = Label(main_menu_root, image = background_image)
    background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    # Création d'images pour les boutons Start Game et Credits
    start_btn_img = ImageTk.PhotoImage(Image.open("buttons/start_btn.png"))
    credits_btn_img = ImageTk.PhotoImage(Image.open("buttons/credits_btn.png"))

    # Création du bouton Start Game et ajout de l'image de fond
    start_btn = Button(main_menu_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = start_game)
    start_btn.config(image=start_btn_img)
    start_btn.place(x = 270, y = 200)

    # Création du bouton Credits et ajout de l'image de fond
    credits_btn = Button(main_menu_root,bd = 0,relief = "groove",compound = CENTER,bg = "#002333",fg = "white",activeforeground = "white",activebackground = "#002333", pady = 0,command = credits_menu)
    credits_btn.config(image=credits_btn_img)
    credits_btn.place(x = 270, y = 300)

    main_menu_root.mainloop()

# Programme principal
if __name__ == "__main__":
    main_menu()
    