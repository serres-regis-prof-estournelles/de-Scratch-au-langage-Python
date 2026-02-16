"""
Jeu Pac-Man - Version Python
Converti depuis Scratch
"""

import tkinter as tk
from tkinter import messagebox
import random
import time

class PacManGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man")
        self.root.resizable(False, False)
        
        # Dimensions du jeu
        self.CELL_SIZE = 30
        self.GRID_WIDTH = 19
        self.GRID_HEIGHT = 21
        self.WIDTH = self.GRID_WIDTH * self.CELL_SIZE
        self.HEIGHT = self.GRID_HEIGHT * self.CELL_SIZE
        
        # Variables de jeu
        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.game_over = False
        self.game_won = False
        self.game_started = False
        
        # Créer le canvas
        self.canvas = tk.Canvas(
            root, 
            width=self.WIDTH, 
            height=self.HEIGHT + 50,
            bg='black'
        )
        self.canvas.pack()
        
        # Labyrinthe (1 = mur, 0 = chemin, 2 = point, 3 = super point)
        self.maze = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
            [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,3,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1],
            [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
            [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
            [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
            [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
            [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
            [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
            [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
            [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
            [1,3,2,1,2,2,2,2,2,0,2,2,2,2,2,1,2,3,1],
            [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
            [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
            [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        
        # Compter les points totaux
        self.total_dots = sum(row.count(2) + row.count(3) for row in self.maze)
        self.dots_eaten = 0
        
        # Position Pac-Man
        self.pacman_x = 9
        self.pacman_y = 15
        self.pacman_dir = 0  # 0=droite, 1=bas, 2=gauche, 3=haut
        self.next_dir = 0
        self.pacman_mouth_open = True
        
        # Fantômes (x, y, direction, couleur, comportement)
        # Comportements: 'chase' (poursuit), 'patrol' (patrouille), 'ambush' (embuscade), 'random' (aléatoire)
        self.ghosts = [
            {'x': 9, 'y': 9, 'dir': 0, 'color': 'red', 'scared': False, 'behavior': 'chase', 'speed': 1},
            {'x': 8, 'y': 9, 'dir': 2, 'color': 'cyan', 'scared': False, 'behavior': 'patrol', 'speed': 1},
            {'x': 10, 'y': 9, 'dir': 0, 'color': 'pink', 'scared': False, 'behavior': 'ambush', 'speed': 1},
            {'x': 9, 'y': 10, 'dir': 3, 'color': 'orange', 'scared': False, 'behavior': 'random', 'speed': 1},
            {'x': 7, 'y': 9, 'dir': 1, 'color': 'red', 'scared': False, 'behavior': 'chase', 'speed': 1},
            {'x': 11, 'y': 9, 'dir': 2, 'color': 'cyan', 'scared': False, 'behavior': 'patrol', 'speed': 1},
            {'x': 8, 'y': 10, 'dir': 0, 'color': 'pink', 'scared': False, 'behavior': 'ambush', 'speed': 1},
            {'x': 10, 'y': 10, 'dir': 3, 'color': 'orange', 'scared': False, 'behavior': 'random', 'speed': 1}
        ]
        
        self.move_counter = 0  # Compteur pour la vitesse des fantômes
        
        self.power_mode = False
        self.power_mode_timer = 0
        
        # Frame d'accueil
        self.show_start_screen()
        
        # Contrôles clavier
        self.root.bind('<Left>', lambda e: self.set_direction(2))
        self.root.bind('<Right>', lambda e: self.set_direction(0))
        self.root.bind('<Up>', lambda e: self.set_direction(3))
        self.root.bind('<Down>', lambda e: self.set_direction(1))
        self.root.bind('<space>', lambda e: self.start_game())
        
    def show_start_screen(self):
        """Afficher l'écran de démarrage"""
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT + 50, fill='black')
        
        # Titre
        self.canvas.create_text(
            self.WIDTH // 2, 150,
            text="PAC-MAN",
            fill='yellow',
            font=('Arial', 48, 'bold')
        )
        
        # Instructions
        self.canvas.create_text(
            self.WIDTH // 2, 250,
            text="Appuyez sur ESPACE pour commencer",
            fill='white',
            font=('Arial', 16)
        )
        
        self.canvas.create_text(
            self.WIDTH // 2, 300,
            text="Utilisez les flèches pour vous déplacer",
            fill='white',
            font=('Arial', 14)
        )
        
        self.canvas.create_text(
            self.WIDTH // 2, 350,
            text="Mangez tous les points !",
            fill='white',
            font=('Arial', 14)
        )
        
        self.canvas.create_text(
            self.WIDTH // 2, 400,
            text="Évitez les fantômes !",
            fill='white',
            font=('Arial', 14)
        )
        
        if self.high_score > 0:
            self.canvas.create_text(
                self.WIDTH // 2, 480,
                text=f"Meilleur score: {self.high_score}",
                fill='cyan',
                font=('Arial', 16)
            )
    
    def start_game(self):
        """Démarrer le jeu"""
        if not self.game_started:
            self.game_started = True
            self.game_over = False
            self.game_won = False
            self.score = 0
            self.lives = 3
            self.dots_eaten = 0
            
            # Réinitialiser le labyrinthe
            self.maze = [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
                [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,3,1],
                [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
                [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1],
                [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
                [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
                [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
                [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
                [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
                [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
                [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
                [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
                [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
                [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
                [1,3,2,1,2,2,2,2,2,0,2,2,2,2,2,1,2,3,1],
                [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
                [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
                [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
                [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ]
            
            # Réinitialiser Pac-Man
            self.pacman_x = 9
            self.pacman_y = 15
            self.pacman_dir = 0
            self.next_dir = 0
            
            # Réinitialiser les fantômes
            self.ghosts = [
                {'x': 9, 'y': 9, 'dir': 0, 'color': 'red', 'scared': False, 'behavior': 'chase', 'speed': 1},
                {'x': 8, 'y': 9, 'dir': 2, 'color': 'cyan', 'scared': False, 'behavior': 'patrol', 'speed': 1},
                {'x': 10, 'y': 9, 'dir': 0, 'color': 'pink', 'scared': False, 'behavior': 'ambush', 'speed': 1},
                {'x': 9, 'y': 10, 'dir': 3, 'color': 'orange', 'scared': False, 'behavior': 'random', 'speed': 1},
                {'x': 7, 'y': 9, 'dir': 1, 'color': 'red', 'scared': False, 'behavior': 'chase', 'speed': 1},
                {'x': 11, 'y': 9, 'dir': 2, 'color': 'cyan', 'scared': False, 'behavior': 'patrol', 'speed': 1},
                {'x': 8, 'y': 10, 'dir': 0, 'color': 'pink', 'scared': False, 'behavior': 'ambush', 'speed': 1},
                {'x': 10, 'y': 10, 'dir': 3, 'color': 'orange', 'scared': False, 'behavior': 'random', 'speed': 1}
            ]
            
            self.move_counter = 0
            
            self.power_mode = False
            self.power_mode_timer = 0
            
            self.game_loop()
    
    def set_direction(self, direction):
        """Changer la direction de Pac-Man"""
        self.next_dir = direction
    
    def can_move(self, x, y):
        """Vérifier si une position est valide"""
        if 0 <= y < self.GRID_HEIGHT and 0 <= x < self.GRID_WIDTH:
            return self.maze[y][x] != 1
        return False
    
    def move_pacman(self):
        """Déplacer Pac-Man"""
        # Essayer de changer de direction
        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][self.next_dir]
        new_x = self.pacman_x + dx
        new_y = self.pacman_y + dy
        
        if self.can_move(new_x, new_y):
            self.pacman_dir = self.next_dir
        
        # Déplacer dans la direction actuelle
        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][self.pacman_dir]
        new_x = self.pacman_x + dx
        new_y = self.pacman_y + dy
        
        if self.can_move(new_x, new_y):
            self.pacman_x = new_x
            self.pacman_y = new_y
            
            # Téléportation (tunnels)
            if self.pacman_x < 0:
                self.pacman_x = self.GRID_WIDTH - 1
            elif self.pacman_x >= self.GRID_WIDTH:
                self.pacman_x = 0
            
            # Manger les points
            cell = self.maze[self.pacman_y][self.pacman_x]
            if cell == 2:  # Point normal
                self.maze[self.pacman_y][self.pacman_x] = 0
                self.score += 10
                self.dots_eaten += 1
            elif cell == 3:  # Super point
                self.maze[self.pacman_y][self.pacman_x] = 0
                self.score += 50
                self.dots_eaten += 1
                self.activate_power_mode()
        
        self.pacman_mouth_open = not self.pacman_mouth_open
    
    def activate_power_mode(self):
        """Activer le mode power (fantômes effrayés)"""
        self.power_mode = True
        self.power_mode_timer = 60  # 60 frames
        for ghost in self.ghosts:
            ghost['scared'] = True
    
    def move_ghosts(self):
        """Déplacer les fantômes avec différents comportements"""
        self.move_counter += 1
        
        for ghost in self.ghosts:
            # Ne déplacer que tous les N frames selon la vitesse
            if self.move_counter % ghost['speed'] != 0:
                continue
                
            # Obtenir les directions possibles
            possible_dirs = []
            for direction in range(4):
                dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][direction]
                new_x = ghost['x'] + dx
                new_y = ghost['y'] + dy
                
                # Éviter de faire demi-tour immédiatement
                opposite_dir = (ghost['dir'] + 2) % 4
                if direction == opposite_dir and len(possible_dirs) > 0:
                    continue
                    
                if self.can_move(new_x, new_y):
                    possible_dirs.append(direction)
            
            if not possible_dirs:
                # Si bloqué, autoriser le demi-tour
                for direction in range(4):
                    dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][direction]
                    new_x = ghost['x'] + dx
                    new_y = ghost['y'] + dy
                    if self.can_move(new_x, new_y):
                        possible_dirs.append(direction)
            
            if possible_dirs:
                best_dir = ghost['dir']
                
                if ghost['scared']:
                    # Mode effrayé : s'éloigner de Pac-Man
                    max_dist = -1
                    for direction in possible_dirs:
                        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][direction]
                        new_x = ghost['x'] + dx
                        new_y = ghost['y'] + dy
                        dist = abs(new_x - self.pacman_x) + abs(new_y - self.pacman_y)
                        if dist > max_dist:
                            max_dist = dist
                            best_dir = direction
                
                elif ghost['behavior'] == 'chase':
                    # Poursuivre directement Pac-Man
                    min_dist = float('inf')
                    for direction in possible_dirs:
                        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][direction]
                        new_x = ghost['x'] + dx
                        new_y = ghost['y'] + dy
                        dist = abs(new_x - self.pacman_x) + abs(new_y - self.pacman_y)
                        if dist < min_dist:
                            min_dist = dist
                            best_dir = direction
                
                elif ghost['behavior'] == 'ambush':
                    # Essayer d'anticiper la position de Pac-Man
                    target_x = self.pacman_x
                    target_y = self.pacman_y
                    
                    # Prédire la position future de Pac-Man
                    pdx, pdy = [(1, 0), (0, 1), (-1, 0), (0, -1)][self.pacman_dir]
                    target_x += pdx * 4
                    target_y += pdy * 4
                    
                    min_dist = float('inf')
                    for direction in possible_dirs:
                        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][direction]
                        new_x = ghost['x'] + dx
                        new_y = ghost['y'] + dy
                        dist = abs(new_x - target_x) + abs(new_y - target_y)
                        if dist < min_dist:
                            min_dist = dist
                            best_dir = direction
                
                elif ghost['behavior'] == 'patrol':
                    # Patrouiller : préférer continuer tout droit
                    if ghost['dir'] in possible_dirs:
                        best_dir = ghost['dir']
                    else:
                        # Sinon, tourner à droite si possible
                        right_dir = (ghost['dir'] + 1) % 4
                        if right_dir in possible_dirs:
                            best_dir = right_dir
                        else:
                            best_dir = possible_dirs[0]
                
                elif ghost['behavior'] == 'random':
                    # Mouvement aléatoire
                    best_dir = random.choice(possible_dirs)
                
                ghost['dir'] = best_dir
                
                # Effectuer le déplacement
                dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][ghost['dir']]
                new_x = ghost['x'] + dx
                new_y = ghost['y'] + dy
                
                if self.can_move(new_x, new_y):
                    ghost['x'] = new_x
                    ghost['y'] = new_y
                    
                    # Téléportation pour les fantômes aussi
                    if ghost['x'] < 0:
                        ghost['x'] = self.GRID_WIDTH - 1
                    elif ghost['x'] >= self.GRID_WIDTH:
                        ghost['x'] = 0
    
    def check_collisions(self):
        """Vérifier les collisions avec les fantômes"""
        for ghost in self.ghosts:
            if ghost['x'] == self.pacman_x and ghost['y'] == self.pacman_y:
                if ghost['scared']:
                    # Manger le fantôme
                    self.score += 200
                    ghost['x'] = 9
                    ghost['y'] = 9
                    ghost['scared'] = False
                else:
                    # Perdre une vie
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        # Réinitialiser les positions
                        self.pacman_x = 9
                        self.pacman_y = 15
                        for g in self.ghosts:
                            g['x'] = 9
                            g['y'] = 9
    
    def draw(self):
        """Dessiner le jeu"""
        self.canvas.delete('all')
        
        # Dessiner le labyrinthe
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                cell = self.maze[y][x]
                x1 = x * self.CELL_SIZE
                y1 = y * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                if cell == 1:  # Mur
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill='blue', outline='blue'
                    )
                elif cell == 2:  # Point
                    center_x = x1 + self.CELL_SIZE // 2
                    center_y = y1 + self.CELL_SIZE // 2
                    self.canvas.create_oval(
                        center_x - 3, center_y - 3,
                        center_x + 3, center_y + 3,
                        fill='white'
                    )
                elif cell == 3:  # Super point
                    center_x = x1 + self.CELL_SIZE // 2
                    center_y = y1 + self.CELL_SIZE // 2
                    self.canvas.create_oval(
                        center_x - 6, center_y - 6,
                        center_x + 6, center_y + 6,
                        fill='white'
                    )
        
        # Dessiner Pac-Man
        px = self.pacman_x * self.CELL_SIZE + self.CELL_SIZE // 2
        py = self.pacman_y * self.CELL_SIZE + self.CELL_SIZE // 2
        radius = self.CELL_SIZE // 2 - 2
        
        if self.pacman_mouth_open:
            # Pac-Man avec bouche ouverte
            start_angle = [350, 80, 170, 260][self.pacman_dir]
            self.canvas.create_arc(
                px - radius, py - radius,
                px + radius, py + radius,
                start=start_angle, extent=280,
                fill='yellow', outline='yellow'
            )
        else:
            # Pac-Man avec bouche fermée
            self.canvas.create_oval(
                px - radius, py - radius,
                px + radius, py + radius,
                fill='yellow', outline='yellow'
            )
        
        # Dessiner les fantômes
        for ghost in self.ghosts:
            gx = ghost['x'] * self.CELL_SIZE + self.CELL_SIZE // 2
            gy = ghost['y'] * self.CELL_SIZE + self.CELL_SIZE // 2
            
            color = 'blue' if ghost['scared'] else ghost['color']
            
            # Corps du fantôme (ovale pour le haut)
            self.canvas.create_oval(
                gx - radius, gy - radius - 2,
                gx + radius, gy + radius // 2,
                fill=color, outline=color
            )
            
            # Bas du fantôme avec des ondulations
            points = []
            num_waves = 3
            for i in range(num_waves + 1):
                x_pos = gx - radius + (2 * radius * i / num_waves)
                if i % 2 == 0:
                    y_pos = gy + radius
                else:
                    y_pos = gy + radius - 4
                points.extend([x_pos, y_pos])
            
            # Ajouter les coins pour fermer la forme
            points.extend([gx + radius, gy])
            points.extend([gx - radius, gy])
            
            if len(points) >= 6:
                self.canvas.create_polygon(points, fill=color, outline=color)
            
            # Yeux
            if not ghost['scared']:
                eye_offset = 5
                eye_size = 3
                # Oeil gauche
                self.canvas.create_oval(
                    gx - eye_offset - eye_size, gy - 4 - eye_size,
                    gx - eye_offset + eye_size, gy - 4 + eye_size,
                    fill='white', outline='white'
                )
                # Pupille gauche
                self.canvas.create_oval(
                    gx - eye_offset - 1, gy - 4 - 1,
                    gx - eye_offset + 1, gy - 4 + 1,
                    fill='black'
                )
                # Oeil droit
                self.canvas.create_oval(
                    gx + eye_offset - eye_size, gy - 4 - eye_size,
                    gx + eye_offset + eye_size, gy - 4 + eye_size,
                    fill='white', outline='white'
                )
                # Pupille droite
                self.canvas.create_oval(
                    gx + eye_offset - 1, gy - 4 - 1,
                    gx + eye_offset + 1, gy - 4 + 1,
                    fill='black'
                )
            else:
                # Yeux effrayés
                self.canvas.create_line(
                    gx - 6, gy - 2, gx - 2, gy - 2,
                    fill='white', width=2
                )
                self.canvas.create_line(
                    gx + 2, gy - 2, gx + 6, gy - 2,
                    fill='white', width=2
                )
        
        # Afficher le score et les vies
        self.canvas.create_text(
            10, self.HEIGHT + 10,
            text=f"Score: {self.score}",
            fill='white',
            font=('Arial', 16),
            anchor='nw'
        )
        
        self.canvas.create_text(
            self.WIDTH // 2, self.HEIGHT + 25,
            text=f"Vies: {'❤️ ' * self.lives}",
            fill='red',
            font=('Arial', 16)
        )
        
        self.canvas.create_text(
            self.WIDTH - 10, self.HEIGHT + 10,
            text=f"Record: {self.high_score}",
            fill='cyan',
            font=('Arial', 16),
            anchor='ne'
        )
    
    def game_loop(self):
        """Boucle principale du jeu"""
        if not self.game_over and not self.game_won:
            # Mettre à jour le jeu
            self.move_pacman()
            self.move_ghosts()
            self.check_collisions()
            
            # Gérer le mode power
            if self.power_mode:
                self.power_mode_timer -= 1
                if self.power_mode_timer <= 0:
                    self.power_mode = False
                    for ghost in self.ghosts:
                        ghost['scared'] = False
            
            # Vérifier la victoire
            if self.dots_eaten >= self.total_dots:
                self.game_won = True
            
            # Dessiner
            self.draw()
            
            # Continuer la boucle
            self.root.after(120, self.game_loop)  # Légèrement plus rapide avec plus d'ennemis
        
        elif self.game_over:
            self.draw()
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2,
                text="GAME OVER",
                fill='red',
                font=('Arial', 48, 'bold')
            )
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 + 60,
                text="Appuyez sur ESPACE pour rejouer",
                fill='white',
                font=('Arial', 16)
            )
            if self.score > self.high_score:
                self.high_score = self.score
            self.game_started = False
        
        elif self.game_won:
            self.draw()
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2,
                text="VOUS AVEZ GAGNÉ !",
                fill='yellow',
                font=('Arial', 42, 'bold')
            )
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 + 60,
                text=f"Score final: {self.score}",
                fill='white',
                font=('Arial', 20)
            )
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 + 100,
                text="Appuyez sur ESPACE pour rejouer",
                fill='white',
                font=('Arial', 16)
            )
            if self.score > self.high_score:
                self.high_score = self.score
            self.game_started = False

# Créer et lancer le jeu
if __name__ == "__main__":
    root = tk.Tk()
    game = PacManGame(root)
    root.mainloop()
