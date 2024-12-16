import pygame
import socket
import time

pygame.init()
pygame.joystick.init()

# Initialisation de l'écran Pygame
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Contrôle Drone avec Manette')

# Configuration de la communication UDP
UDP_IP = "192.168.10.1"  
UDP_PORT = 8889  
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Vérification de la manette
if pygame.joystick.get_count() == 0:
    print("Aucune manette détectée!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initialisation de la police pour afficher les commandes envoyées
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Fonction pour envoyer une commande
def send_command(command):
    try:
        sock.sendto(command.encode(), (UDP_IP, UDP_PORT))
        print(f"Commande envoyée: {command}")
        message, clientAddress = sock.recvfrom(1024)
        print(f"Message reçu : {message}")
        print(f"De : {clientAddress}")
        return command  # Retourne la commande pour l'afficher
    except Exception as e:
        print(f"Erreur lors de l'envoi de la commande: {e}")
        return "Erreur"

# Commande initiale
send_command("command")
time.sleep(2)

previous_axis_x = 0
previous_axis_y = 0
previous_button_a = False
previous_button_b = False
previous_button_x = False
previous_button_y = False

# Variable pour afficher la dernière commande
last_command = ""

# Couleurs personnalisées
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
FRAME_COLOR = (255, 165, 0)
BUTTON_COLOR = (0, 128, 255)
TEXTBOX_COLOR = (50, 50, 50)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        axis_x = joystick.get_axis(0)  
        axis_y = joystick.get_axis(1)  

        # Détection des axes et envoi des commandes correspondantes
        if axis_y < -0.5 and axis_y != previous_axis_y: 
            last_command = send_command("up 50") 
            previous_axis_y = axis_y
        elif axis_y > 0.5 and axis_y != previous_axis_y: 
            last_command = send_command("down 50")  
            previous_axis_y = axis_y 

        if axis_x < -0.5 and axis_x != previous_axis_x: 
            last_command = send_command("left 50")  
            previous_axis_x = axis_x  
        elif axis_x > 0.5 and axis_x != previous_axis_x: 
            last_command = send_command("right 50")  
            previous_axis_x = axis_x  

        # Détection des boutons et envoi des commandes correspondantes
        button_a = joystick.get_button(0) 
        button_b = joystick.get_button(1)  
        button_x = joystick.get_button(2)  
        button_y = joystick.get_button(3)  

        if button_a and not previous_button_a:  
            last_command = send_command("takeoff")
            previous_button_a = True
        elif not button_a and previous_button_a:  
            previous_button_a = False

        if button_b and not previous_button_b:  
            last_command = send_command("land")
            previous_button_b = True
        elif not button_b and previous_button_b:  
            previous_button_b = False

        if button_x and not previous_button_x:  
            last_command = send_command("forward 50")
            previous_button_x = True
        elif not button_x and previous_button_x:  
            previous_button_x = False

        if button_y and not previous_button_y:  
            last_command = send_command("back 50")
            previous_button_y = True
        elif not button_y and previous_button_y: 
            previous_button_y = False

    except Exception as e:
        print(f"Erreur dans la boucle principale: {e}")


    screen.fill(BACKGROUND_COLOR)

   
    pygame.draw.rect(screen, FRAME_COLOR, pygame.Rect(20, 20, 560, 100), 5)

    text = font.render(f"Commande: {last_command}", True, TEXT_COLOR)
    screen.blit(text, (30, 40)) 

    
    text_info = small_font.render("Utilisez la manette pour contrôler le drone", True, BUTTON_COLOR)
    screen.blit(text_info, (30, 160))

   
    pygame.draw.rect(screen, BUTTON_COLOR, pygame.Rect(30, 200, 200, 40))
    button_text = small_font.render("Takeoff (A)", True, TEXT_COLOR)
    screen.blit(button_text, (90, 210))

    pygame.draw.rect(screen, BUTTON_COLOR, pygame.Rect(30, 250, 200, 40))
    button_text = small_font.render("Land (B)", True, TEXT_COLOR)
    screen.blit(button_text, (90, 260))

    pygame.draw.rect(screen, BUTTON_COLOR, pygame.Rect(300, 200, 200, 40))
    button_text = small_font.render("Move Forward (X)", True, TEXT_COLOR)
    screen.blit(button_text, (340, 210))

    pygame.draw.rect(screen, BUTTON_COLOR, pygame.Rect(300, 250, 200, 40))
    button_text = small_font.render("Move Back (Y)", True, TEXT_COLOR)
    screen.blit(button_text, (340, 260))

    pygame.display.flip()

    
    pygame.time.Clock().tick(60)

pygame.quit()
sock.close()
