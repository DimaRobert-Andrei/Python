import pygame
import os


class Player:
    def __init__(self, start_x, start_y):
        self.scale_factor = 2
        self.frame_width = 16
        self.frame_height = 32
        self.scaled_width = self.frame_width * self.scale_factor
        self.scaled_height = self.frame_height * self.scale_factor

        self.rect = pygame.Rect(start_x, start_y, 20, 15)

        self.walk_speed = 2
        self.run_speed = 4
        self.speed = self.walk_speed
        self.is_hidden = False

        # --- SISTEM DE STAMINA ---
        self.max_stamina = 100
        self.current_stamina = self.max_stamina
        self.stamina_drain_rate = 1
        self.stamina_regen_rate = 0.3
        self.stamina_cooldown = 1000
        self.last_run_time = 0
        self.jump_stamina_cost = 30  # Costul unei sărituri (30%)

        # --- SISTEM DE SĂRITURĂ (Z-Axis Fals) ---
        self.is_jumping = False
        self.z = 0
        self.z_velocity = 0

        # AM MODIFICAT GRAVITAȚIA ȘI PUTEREA SĂRITURII PENTRU A SĂRI MAI MULT
        self.gravity = 0.9  # Redusă de la 1.2 pentru a pluti mai mult
        self.jump_power = 14  # Crescută de la 10 pentru a se înălța mai mult

        self.safe_pos = None

        player_path = os.path.join("assets", "player")
        idle_path = os.path.join(player_path, "16x32 Idle-Sheet.png")
        walk_path = os.path.join(player_path, "16x32 Walk-Sheet.png")
        run_path = os.path.join(player_path, "16x32 Run-Sheet.png")
        jump_path = os.path.join(player_path, "16x32 Jump-Sheet.png")

        try:
            self.idle_sheet = pygame.image.load(idle_path).convert_alpha()
            self.walk_sheet = pygame.image.load(walk_path).convert_alpha()
            self.run_sheet = pygame.image.load(run_path).convert_alpha()
            self.jump_sheet = pygame.image.load(jump_path).convert_alpha()
        except pygame.error as e:
            print(f"Eroare la incarcarea imaginilor jucatorului: {e}")
            self.idle_sheet = pygame.Surface((32, 32), pygame.SRCALPHA)
            self.idle_sheet.fill((0, 255, 0))
            self.walk_sheet = self.idle_sheet
            self.run_sheet = self.idle_sheet
            self.jump_sheet = self.idle_sheet

        self.animations = {
            'idle_down': self.get_frames(self.idle_sheet, 0),
            'idle_right': self.get_frames(self.idle_sheet, 2),
            'idle_left': self.get_frames(self.idle_sheet, 2, flip=True),
            'idle_up': self.get_frames(self.idle_sheet, 4),

            'walk_down': self.get_frames(self.walk_sheet, 0),
            'walk_right': self.get_frames(self.walk_sheet, 2),
            'walk_left': self.get_frames(self.walk_sheet, 2, flip=True),
            'walk_up': self.get_frames(self.walk_sheet, 4),

            'run_down': self.get_frames(self.run_sheet, 0),
            'run_right': self.get_frames(self.run_sheet, 2),
            'run_left': self.get_frames(self.run_sheet, 2, flip=True),
            'run_up': self.get_frames(self.run_sheet, 4),

            'jump_down': self.get_frames(self.jump_sheet, 0),
            'jump_right': self.get_frames(self.jump_sheet, 2),
            'jump_left': self.get_frames(self.jump_sheet, 2, flip=True),
            'jump_up': self.get_frames(self.jump_sheet, 4),
        }

        self.state = 'idle'
        self.direction = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[f'{self.state}_{self.direction}'][self.frame_index]

    def get_frames(self, sheet, row, flip=False):
        frames = []
        num_frames = sheet.get_width() // self.frame_width
        if row * self.frame_height >= sheet.get_height(): row = 0
        if num_frames == 0: num_frames = 1

        for i in range(num_frames):
            x = i * self.frame_width
            y = row * self.frame_height
            frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame_surface.blit(sheet, (0, 0), (x, y, self.frame_width, self.frame_height))
            if flip:
                frame_surface = pygame.transform.flip(frame_surface, True, False)
            frame_surface = pygame.transform.scale(frame_surface, (self.scaled_width, self.scaled_height))
            frames.append(frame_surface)
        return frames

    def animate(self):
        animation_list = self.animations[f'{self.state}_{self.direction}']
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation_list):
            if self.state == 'jump':
                self.frame_index = len(animation_list) - 1
            else:
                self.frame_index = 0
        self.image = animation_list[int(self.frame_index)]

    def move(self, keys, walls):
        if self.is_hidden: return

        moving = False
        old_pos = self.rect.copy()
        current_time = pygame.time.get_ticks()

        # --- INIȚIEREA SĂRITURII CU COST DE STAMINA ---
        if keys[pygame.K_SPACE] and not self.is_jumping:
            if self.current_stamina >= self.jump_stamina_cost:
                self.is_jumping = True
                self.z_velocity = self.jump_power
                self.safe_pos = self.rect.copy()
                self.frame_index = 0
                self.current_stamina -= self.jump_stamina_cost
                self.last_run_time = current_time

        # --- LOGICA STAMINEI PENTRU ALERGARE ---
        wants_to_run = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        is_moving_keys = keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]

        is_running = False
        # Permitem consumul de stamina pentru alergare doar cand NU sărim
        if wants_to_run and is_moving_keys and not self.is_jumping:
            if self.current_stamina > 0:
                is_running = True
                self.speed = self.run_speed
            else:
                self.speed = self.walk_speed
        else:
            # Dacă sărim, păstrăm viteza pe care o aveam înainte de săritură
            # (dacă alergai, sari mai repede/departe; dacă mergeai, sari mai încet)
            if not self.is_jumping:
                self.speed = self.walk_speed

        if is_running:
            self.current_stamina -= self.stamina_drain_rate
            self.last_run_time = current_time
            if self.current_stamina < 0:
                self.current_stamina = 0
                is_running = False
                self.speed = self.walk_speed
        elif not self.is_jumping:  # Regenerăm doar dacă stăm pe pământ
            if current_time - self.last_run_time > self.stamina_cooldown:
                self.current_stamina += self.stamina_regen_rate
                if self.current_stamina > self.max_stamina:
                    self.current_stamina = self.max_stamina

        # --- MIȘCAREA PE AXELE X/Y (Permisă și în timpul săriturii) ---
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = 'left'
            moving = True
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = 'right'
            moving = True

        if not self.is_jumping:
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.x = old_pos.x

        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = 'up'
            moving = True
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = 'down'
            moving = True

        # Coliziunile pe Y funcționează doar când NU sărim
        if not self.is_jumping:
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.y = old_pos.y

        # --- UPDATE AXA Z (SĂRITURA) ---
        if self.is_jumping:
            self.z += self.z_velocity
            self.z_velocity -= self.gravity

            if self.z <= 0:
                self.z = 0
                self.is_jumping = False

                # La aterizare: dacă suntem "înfipți" într-un obstacol, ne întoarcem
                for wall in walls:
                    if self.rect.colliderect(wall):
                        self.rect.x = self.safe_pos.x
                        self.rect.y = self.safe_pos.y
                        break
                # Actualizăm timpul ca să înceapă cooldown-ul de regenerare DUPĂ ce am aterizat
                self.last_run_time = current_time

        # --- SETĂRI ANIMAȚIE ---
        if self.is_jumping:
            self.state = 'jump'
            self.animation_speed = 0.20
        elif moving:
            self.state = 'run' if is_running else 'walk'
            self.animation_speed = 0.25 if is_running else 0.15
        else:
            self.state = 'idle'
            self.animation_speed = 0.15

        self.animate()

    def get_render_data(self):
        if self.is_hidden: return None

        image_draw_x = self.rect.centerx - (self.scaled_width // 2)
        image_draw_y = self.rect.bottom - self.scaled_height - self.z

        return {
            'img': self.image,
            'pos': (image_draw_x, image_draw_y),
            'y_sort': self.rect.bottom
        }