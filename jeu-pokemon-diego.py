# Arborescence du projet
"""
jeu_pokemon/
│
├── jeu.py                  # Fichier principal du jeu
├── README.md               # Instructions d'installation
├── installer.bat           # Script d'installation Windows
├── installer.sh            # Script d'installation Linux/Mac
│
└── assets/
    ├── images/
    │   ├── personnage.png
    │   ├── pokemon1.png
    │   ├── pokemon2.png
    │   └── fond.png
    │
    └── sons/
        ├── capture.wav
        └── musique_fond.mp3
"""

# jeu.py
import pygame
import random
import sys
import os

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Configuration de l'écran
LARGEUR, HAUTEUR = 800, 600
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Chasse aux Pokémon de Diego")

# Charger les ressources
def charger_image(nom):
    chemin = os.path.join('assets', 'images', nom)
    return pygame.image.load(chemin).convert_alpha()

def charger_son(nom):
    chemin = os.path.join('assets', 'sons', nom)
    return pygame.mixer.Sound(chemin)

# Classes du jeu
class Personnage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = charger_image('personnage.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (LARGEUR // 2, HAUTEUR - 100)
        self.vitesse = 5

    def deplacer(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, LARGEUR - self.rect.width))

class Pokemon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Liste de Pokémon
        pokemons = ['pokemon1.png', 'pokemon2.png']
        self.image = charger_image(random.choice(pokemons))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGEUR - self.rect.width)
        self.rect.y = 0
        self.vitesse = random.randint(1, 3)

    def tomber(self):
        self.rect.y += self.vitesse

class Jeu:
    def __init__(self):
        # Fond
        self.fond = charger_image('fond.png')
        self.fond = pygame.transform.scale(self.fond, (LARGEUR, HAUTEUR))

        self.personnage = Personnage()
        self.tous_sprites = pygame.sprite.Group(self.personnage)
        self.pokemons = pygame.sprite.Group()
        self.score = 0
        self.temps_spawn = 0
        
        # Sons
        try:
            self.son_capture = charger_son('capture.wav')
            pygame.mixer.music.load(os.path.join('assets', 'sons', 'musique_fond.mp3'))
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erreur de sons : {e}")

    def spawn_pokemon(self):
        nouveau_pokemon = Pokemon()
        self.pokemons.add(nouveau_pokemon)
        self.tous_sprites.add(nouveau_pokemon)

    def execution(self):
        horloge = pygame.time.Clock()
        temps_ecoule = 0
        duree_jeu = 60  # 1 minute de jeu

        police = pygame.font.Font(None, 36)

        while temps_ecoule < duree_jeu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            # Contrôles clavier
            touches = pygame.key.get_pressed()
            if touches[pygame.K_LEFT]:
                self.personnage.deplacer(-self.personnage.vitesse)
            if touches[pygame.K_RIGHT]:
                self.personnage.deplacer(self.personnage.vitesse)

            # Spawn de Pokémon
            self.temps_spawn += 1
            if self.temps_spawn > 30:
                self.spawn_pokemon()
                self.temps_spawn = 0

            # Déplacer les Pokémon
            for pokemon in self.pokemons:
                pokemon.tomber()

                # Capture de Pokémon
                if pygame.sprite.collide_rect(self.personnage, pokemon):
                    self.score += 1
                    try:
                        self.son_capture.play()
                    except:
                        pass
                    pokemon.kill()

                # Supprimer les Pokémon hors écran
                if pokemon.rect.top > HAUTEUR:
                    pokemon.kill()

            # Dessiner
            ecran.blit(self.fond, (0, 0))
            self.tous_sprites.draw(ecran)

            # Afficher le score
            texte_score = police.render(f"Pokémon capturés : {self.score}", True, (0,0,0))
            ecran.blit(texte_score, (10, 10))

            # Afficher le temps restant
            temps_restant = max(0, int(duree_jeu - temps_ecoule))
            texte_temps = police.render(f"Temps : {temps_restant} sec", True, (0,0,0))
            ecran.blit(texte_temps, (LARGEUR - 200, 10))

            pygame.display.flip()
            horloge.tick(60)
            temps_ecoule += 1/60

        # Écran de fin
        ecran.fill((0,255,0))
        texte_fin = police.render(f"Bravo ! Tu as capturé {self.score} Pokémon !", True, (0,0,0))
        rect_texte = texte_fin.get_rect(center=(LARGEUR//2, HAUTEUR//2))
        ecran.blit(texte_fin, rect_texte)
        pygame.display.flip()

        # Attendre avant de quitter
        pygame.time.wait(3000)
        return True

def main():
    jeu = Jeu()
    jeu.execution()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

# README.md
"""
# Jeu de Pokémon pour Diego

## Installation

### Windows
1. Installer Python 3.8+ depuis python.org
2. Télécharger le projet complet
3. Double-cliquer sur `installer.bat`

### Linux/Mac
1. Installer Python 3.8+
2. Ouvrir un terminal
3. Exécuter `./installer.sh`

## Comment jouer
- Utilisez les flèches gauche/droite
- Capturez max de Pokémon en 1 minute
- Amusez-vous bien !
"""

# installer.bat (Windows)
"""
@echo off
python -m venv env
env\Scripts\activate
pip install pygame
python jeu.py
"""

# installer.sh (Linux/Mac)
"""
#!/bin/bash
python3 -m venv env
source env/bin/activate
pip install pygame
python3 jeu.py
"""