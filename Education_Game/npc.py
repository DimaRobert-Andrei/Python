
import pygame
import math
import random
import heapq
from settings import TILE_SIZE, FPS



# 1. STAREA ȘI MEMORIA NPC-ULUI

class EnemyNPC:
    # Inițializează poziția, simțurile, starea FSM, memoria și traseul NPC-ului.
    def __init__(self, x, y, game_map):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.exact_x = float(x)
        self.exact_y = float(y)
        self.game_map = game_map

        self.current_round = 1
        self.base_speed = 1.75
        self.speed = self.base_speed

        self.sense_radius = 60
        self.vision_distance = 250
        self.vision_fov = 70

        self.state = "WAITING"
        self.target_pos = None
        self.path = []
        self.search_timer = 0
        self.investigating_chest = None
        self.caught_player = False

        self.priority_targets = []
        self.ai_memory = {}
        self.checked_this_round = set()

        for chest in self.game_map.chests:
            key = (chest['hitbox'].x, chest['hitbox'].y)
            self.ai_memory[key] = 10.0

        self.facing_angle = 0
        self.color = (255, 0, 0)


    # 2. RESETAREA ȘI DIFICULTATEA PE RUNDE
    # Resetează NPC-ul și actualizează memoria ascunzătorilor între runde.
    def reset_round(self, spawn_x, spawn_y):
        for chest in self.game_map.chests:
            if chest.get('player_inside', False):
                key = (chest['hitbox'].x, chest['hitbox'].y)
                self.ai_memory[key] += 40.0
                print(f"\n[ AI POST-MATCH ] Aha! Deci te ascundeai la {key}! Runda viitoare verific acolo prima dată!")

        self.rect.x = int(spawn_x)
        self.rect.y = int(spawn_y)
        self.exact_x = float(spawn_x)
        self.exact_y = float(spawn_y)

        self.state = "WAITING"
        self.target_pos = None
        self.path = []
        self.search_timer = 0
        self.investigating_chest = None
        self.caught_player = False
        self.checked_this_round.clear()
        self.priority_targets = []

    # Mărește viteza, raza vizuală și raza auditivă în funcție de rundă.
    def set_difficulty(self, round_num):
        self.current_round = round_num
        self.speed = self.base_speed + (round_num * 0.25)
        self.sense_radius = 50 + (round_num * 10)
        self.vision_distance = 200 + (round_num * 30)
        self.vision_fov = 60 + (round_num * 5)

        self.checked_this_round.clear()
        self.priority_targets = []

        print("\n" + "=" * 50)
        print(f"[ SYSTEM ] === INIȚIALIZARE RUNDA {self.current_round} ===")
        print(f"[ STATS ] Viteză: {self.speed:.2f} | Văz: {self.vision_distance}px | Auz: {self.sense_radius}px")
        print("[ SYSTEM ] Harta mentală a AI-ului (Q-Table):")

        sorted_memory = sorted(self.ai_memory.items(), key=lambda item: item[1], reverse=True)

        for index, (loc, scor) in enumerate(sorted_memory):
            if scor > 10.0:
                print(f"  {index + 1}. Ascunzătoarea {loc} -> Scor: {scor} (FOARTE SUSPECTĂ!)")
            elif scor < 10.0:
                print(f"  {index + 1}. Ascunzătoarea {loc} -> Scor: {scor} (Probabil goală)")
            else:
                print(f"  {index + 1}. Ascunzătoarea {loc} -> Scor: {scor} (Neutru)")

            #  Dacă scorul e mare, se duce DIRECT acolo runda viitoare

            if scor >= 45.0:
                for chest in self.game_map.chests:
                    if chest['hitbox'].x == loc[0] and chest['hitbox'].y == loc[1]:
                        if chest not in self.priority_targets:
                            self.priority_targets.append(chest)
                            print(f"[ AI ] Am pus locația {loc} pe lista de execuție imediată!")

        print("=" * 50 + "\n")


    # 3. PERCEPȚIA VIZUALĂ ȘI AUDITIVĂ

    # Stabilește dacă NPC-ul poate trece printr-o anumită ușă.
    def can_pass_door(self, door):
        if self.current_round == 1 and door.get('is_quiz_door', False):
            return False
        return True

    # Verifică distanța, unghiul FOV și obstacolele prin raycasting.
    def can_see_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist < self.vision_distance:
            angle_to_player = math.degrees(math.atan2(-dy, dx))
            angle_diff = (angle_to_player - self.facing_angle + 180) % 360 - 180

            if abs(angle_diff) <= self.vision_fov / 2:
                steps = max(int(dist / (TILE_SIZE / 2)), 1)
                for i in range(1, steps):
                    check_x = self.rect.centerx + (dx / steps) * i
                    check_y = self.rect.centery + (dy / steps) * i
                    for wall in self.game_map.wall_hitboxes:
                        if wall.collidepoint(check_x, check_y):
                            return False
                return True
        return False

    # Construiește lista ascunzătorilor apropiate de ultima poziție cunoscută.
    def create_priority_targets(self, center_pos):
        local_chests = []
        for c in self.game_map.chests:
            dist_to_c = math.hypot(c['hitbox'].centerx - center_pos[0], c['hitbox'].centery - center_pos[1])
            if dist_to_c < 12 * TILE_SIZE:
                local_chests.append((dist_to_c, c))
                c_key = (c['hitbox'].x, c['hitbox'].y)
                self.ai_memory[c_key] += 10.0

        local_chests.sort(key=lambda x: x[0])
        self.priority_targets = [item[1] for item in local_chests]


    # 4. MAȘINA CU STĂRI FINITE - FSM

    # Aplică tranzițiile FSM pe baza stimulilor vizuali și auditivi.
    def update(self, player):
        if self.state == "WAITING":
            return

        if self.state == "PATROL":
            self.state = "SEARCH"

        interact_dist = self.game_map.interact_distance
        for door in self.game_map.doors:
            if not door['is_open'] and self.can_pass_door(door):
                dist_to_door = math.hypot(self.rect.centerx - door['hitbox'].centerx,
                                          self.rect.centery - door['hitbox'].centery)
                if dist_to_door < interact_dist:
                    door['is_open'] = True

        is_hidden = False
        if hasattr(self.game_map, 'chests'):
            is_hidden = any(c['player_inside'] for c in self.game_map.chests)

        sees_player = False
        hears_player = False

        if not is_hidden:
            sees_player = self.can_see_player(player)
            dist_to_player = math.hypot(player.rect.centerx - self.rect.centerx,
                                        player.rect.centery - self.rect.centery)
            if dist_to_player < self.sense_radius:
                hears_player = True

        if sees_player or hears_player:
            if self.state != "CHASE":
                motiv = "VĂZUT" if sees_player else "AUZIT"
                print(f"[ AI ] TE-AM {motiv}! Trec la urmărire!")

            self.state = "CHASE"
            self.target_pos = player.rect.center

            if self.investigating_chest and self.investigating_chest.get('is_open', False):
                self.investigating_chest['is_open'] = False
            self.investigating_chest = None
            self.path = []

        elif self.state == "CHASE" and is_hidden:
            print("[ AI ] Te-am văzut ascunzându-te! ")
            self.create_priority_targets(self.target_pos)
            self.state = "SEARCH"
            self.search_timer = 0
            self.path = []

        elif self.state == "CHASE" and not (sees_player or hears_player):
            dist_to_last_known = math.hypot(self.target_pos[0] - self.rect.centerx,
                                            self.target_pos[1] - self.rect.centery)

            if dist_to_last_known < 30:
                print("[ AI ]  Ai dispărut!  Caut  imediat zona in asta!")
                self.create_priority_targets(self.target_pos)
                self.state = "SEARCH"
                self.search_timer = 0
                self.path = []

        if self.state == "SEARCH":
            self.ai_search_logic(player)
            self.follow_path()
        elif self.state == "CHASE":
            self.move_towards_point(self.target_pos)


    # 5. CĂUTAREA ȘI MEMORIA ASCUNZĂTORILOR

    # Controlează investigarea ascunzătorilor în starea SEARCH.
    def ai_search_logic(self, player):
        if not self.path:
            if self.investigating_chest:
                if self.search_timer > 0:
                    self.search_timer -= 1

                    if self.search_timer == int(0.5 * FPS):
                        self.investigating_chest['is_open'] = True

                        dx = self.investigating_chest['hitbox'].centerx - self.rect.centerx
                        dy = self.investigating_chest['hitbox'].centery - self.rect.centery
                        self.facing_angle = math.degrees(math.atan2(-dy, dx))

                        key = (self.investigating_chest['hitbox'].x, self.investigating_chest['hitbox'].y)

                        if self.investigating_chest.get('player_inside', False):
                            self.investigating_chest['player_inside'] = False
                            player.rect.y += TILE_SIZE
                            self.caught_player = True
                            self.ai_memory[key] += 50.0
                            print(f"[ AI ÎNVAȚĂ ] TE-AM GĂSIT!")
                        else:
                            self.ai_memory[key] -= 2.0
                            if self.ai_memory[key] < 1.0:
                                self.ai_memory[key] = 1.0
                            self.checked_this_round.add(key)

                else:
                    if self.investigating_chest['is_open']:
                        self.investigating_chest['is_open'] = False
                    self.investigating_chest = None
                    self.pick_next_ai_target()
                return

            self.pick_next_ai_target()

    # Alege următoarea destinație folosind memoria și prioritățile NPC-ului.
    def pick_next_ai_target(self):
        while self.priority_targets:
            potential_chest = self.priority_targets.pop(0)
            key = (potential_chest['hitbox'].x, potential_chest['hitbox'].y)

            if key not in self.checked_this_round:
                self.investigating_chest = potential_chest
                chest_box = self.investigating_chest['hitbox']
                self.target_pos = (chest_box.centerx, chest_box.bottom + 30)

                self.path = self.calculate_astar_path(self.rect.center, self.target_pos)
                if self.path:
                    self.search_timer = 0
                    return
                else:
                    self.checked_this_round.add(key)

        available_chests = []
        weights = []

        for chest in self.game_map.chests:
            key = (chest['hitbox'].x, chest['hitbox'].y)
            if key not in self.checked_this_round:
                available_chests.append(chest)
                weights.append(self.ai_memory[key])

        if not available_chests:
            self.investigating_chest = None
            self.target_pos = self.get_random_point()
            self.path = self.calculate_astar_path(self.rect.center, self.target_pos)
            return

        chosen_chest = random.choices(available_chests, weights=weights, k=1)[0]
        self.investigating_chest = chosen_chest

        chest_box = self.investigating_chest['hitbox']
        self.target_pos = (chest_box.centerx, chest_box.bottom + 30)

        key = (self.investigating_chest['hitbox'].x, self.investigating_chest['hitbox'].y)
        self.path = self.calculate_astar_path(self.rect.center, self.target_pos)

        if not self.path:
            self.checked_this_round.add(key)
            self.search_timer = 0
            self.investigating_chest = None
        else:
            self.search_timer = 0

    # Generează un punct liber pentru deplasarea de căutare.
    def get_random_point(self):
        while True:
            rx = random.randint(2, self.game_map.width // TILE_SIZE - 2) * TILE_SIZE
            ry = random.randint(2, self.game_map.height // TILE_SIZE - 2) * TILE_SIZE
            test_rect = pygame.Rect(rx, ry, TILE_SIZE, TILE_SIZE)

            if not any(test_rect.colliderect(w) for w in self.game_map.wall_hitboxes):
                if not any(test_rect.colliderect(c['hitbox']) for c in self.game_map.chests):
                    return (rx + TILE_SIZE // 2, ry + TILE_SIZE // 2)


    # 6. MIȘCAREA ȘI URMĂRIREA TRASEULUI

    # Deplasează NPC-ul direct către o țintă și actualizează orientarea.
    def move_towards_point(self, pos):
        dx = pos[0] - self.rect.centerx
        dy = pos[1] - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist > 3:
            vel_x = (dx / dist) * self.speed
            vel_y = (dy / dist) * self.speed

            self.facing_angle = math.degrees(math.atan2(-vel_y, vel_x))

            hitbox_size = 12
            offset = (24 - hitbox_size) // 2

            solid_rects = self.game_map.wall_hitboxes.copy()
            for c in self.game_map.chests:
                solid_rects.append(c['hitbox'])

            self.exact_x += vel_x
            test_rect = pygame.Rect(int(self.exact_x) + offset, int(self.exact_y) + offset, hitbox_size, hitbox_size)
            if any(test_rect.colliderect(w) for w in solid_rects):
                self.exact_x -= vel_x
            self.rect.x = int(self.exact_x)

            self.exact_y += vel_y
            test_rect = pygame.Rect(int(self.exact_x) + offset, int(self.exact_y) + offset, hitbox_size, hitbox_size)
            if any(test_rect.colliderect(w) for w in solid_rects):
                self.exact_y -= vel_y
            self.rect.y = int(self.exact_y)

    # Urmează succesiv nodurile traseului calculat.
    def follow_path(self):
        if not self.path: return
        target_node = self.path[0]
        dist = math.hypot(target_node[0] - self.rect.centerx, target_node[1] - self.rect.centery)

        reach_dist = 10

        if len(self.path) == 1 and self.investigating_chest:
            reach_dist = 15

        if dist < reach_dist:
            self.path.pop(0)
            if not self.path:
                if self.investigating_chest:
                    self.search_timer = int(1.0 * FPS)
        else:
            self.move_towards_point(target_node)


    # 7. PATHFINDING CU ALGORITMUL A*

    # Calculează traseul pe grilă cu algoritmul A* și distanța Manhattan.
    def calculate_astar_path(self, start_pos, target_pos):
        start_grid = (int(start_pos[0] // TILE_SIZE), int(start_pos[1] // TILE_SIZE)) #pozitia din pixeli devine grila
        target_grid = (int(target_pos[0] // TILE_SIZE), int(target_pos[1] // TILE_SIZE))

        open_list = [(0, start_grid)]# Nodurile care urmează să fie analizate.
        came_from = {start_grid: None}    # Reține nodul anterior pentru reconstruirea traseului.
        cost_so_far = {start_grid: 0}

        while open_list:
            current = heapq.heappop(open_list)[1] # Extrage nodul cu cea mai mică prioritate.
            if current == target_grid:
                break

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]: #Pentru fiecare nod sunt verificați cei patru vecini:
                next_node = (current[0] + dx, current[1] + dy)

                if next_node[0] < 0 or next_node[1] < 0 or next_node[0] >= self.game_map.width // TILE_SIZE or \
                        next_node[1] >= self.game_map.height // TILE_SIZE:
                    continue

                test_rect = pygame.Rect(next_node[0] * TILE_SIZE + 2, next_node[1] * TILE_SIZE + 2, TILE_SIZE - 4, # Creează un dreptunghi pentru verificarea coliziunilor.
                                        TILE_SIZE - 4)

                collision = False
                for wall in self.game_map.wall_hitboxes:
                    if test_rect.colliderect(wall):
                        collision = True;
                        break

                if not collision:
                    for door in self.game_map.doors:
                        if test_rect.colliderect(door['hitbox']):
                            if not door['is_open'] and not self.can_pass_door(door):
                                collision = True;
                                break

                if not collision:
                    for chest in self.game_map.chests:
                        if test_rect.colliderect(chest['hitbox']):
                            collision = True;
                            break

                if collision: continue

                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + (abs(target_grid[0] - next_node[0]) + abs(target_grid[1] - next_node[1]))  # Prioritatea = costul parcurs + distanța Manhattan.
                    heapq.heappush(open_list, (priority, next_node))
                    came_from[next_node] = current#traseul este reconstruit

        path = []
        current = target_grid
        if current in came_from:
            while current != start_grid:
                path.append((current[0] * TILE_SIZE + TILE_SIZE // 2, current[1] * TILE_SIZE + TILE_SIZE // 2))
                current = came_from[current]
            path.reverse()     # Inversează traseul pentru a porni de la NPC spre destinație.

        return path


    # 8. RANDAREA NPC-ULUI ȘI A CÂMPULUI VIZUAL

    # Desenează câmpul vizual al NPC-ului.
    def draw_fov(self, screen, camera):
        sw, sh = screen.get_size()
        fov_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        center_screen = camera.apply(self.rect.center)
        points = [center_screen]
        segments = 15

        start_angle = self.facing_angle - self.vision_fov / 2
        end_angle = self.facing_angle + self.vision_fov / 2

        for i in range(segments + 1):
            angle = start_angle + (end_angle - start_angle) * (i / segments)
            rad = math.radians(-angle)
            px = self.rect.centerx + math.cos(rad) * self.vision_distance
            py = self.rect.centery + math.sin(rad) * self.vision_distance
            points.append(camera.apply((px, py)))

        if self.state == "CHASE":
            color = (255, 50, 50, 90)
        else:
            color = (255, 255, 0, 60)

        pygame.draw.polygon(fov_surf, color, points)
        screen.blit(fov_surf, (0, 0))

    # Desenează NPC-ul și elementele vizuale asociate.
    def draw(self, screen, camera):
        self.draw_fov(screen, camera)
        pygame.draw.circle(screen, self.color, camera.apply(self.rect.center), 12)
        eye_x = self.rect.centerx + math.cos(math.radians(-self.facing_angle)) * 10
        eye_y = self.rect.centery + math.sin(math.radians(-self.facing_angle)) * 10
        pygame.draw.circle(screen, (255, 255, 255), camera.apply((eye_x, eye_y)), 4)
