import pygame
import os
import math
import random
from settings import TILE_SIZE


# ===========================================================================
# 1. INIȚIALIZAREA HĂRȚII ȘI A RESURSELOR
# ===========================================================================
class GameMap:
    # Încarcă texturile, definește layout-ul și construiește harta.
    def __init__(self, width, height):
        self.width = width
        self.height = height

        base_dir = os.path.dirname(__file__)
        assets_path = os.path.join(base_dir, "assets", "map")

        # ==========================================
        # 1. ÎNCĂRCARE PEREȚI ȘI PODEA
        # ==========================================
        try:
            self.tex_h_top = pygame.image.load(os.path.join(assets_path, "perete3.png")).convert_alpha()
            self.tex_h_bottom = pygame.image.load(os.path.join(assets_path, "perete5.png")).convert_alpha()
            self.tex_v_left = pygame.image.load(os.path.join(assets_path, "perete6.png")).convert_alpha()

            self.tex_h_top_m = pygame.transform.flip(self.tex_h_top, True, False)
            self.tex_h_bottom_m = pygame.transform.flip(self.tex_h_bottom, True, False)
            self.tex_v_right = pygame.transform.flip(self.tex_v_left, True, False)

            self.c_tl = pygame.image.load(os.path.join(assets_path, "colt_stanga_sus.png")).convert_alpha()
            self.c_tr = pygame.image.load(os.path.join(assets_path, "colt_dreapta_sus.png")).convert_alpha()
            self.c_bl = pygame.image.load(os.path.join(assets_path, "stanga_jos.png")).convert_alpha()
            self.c_br = pygame.image.load(os.path.join(assets_path, "dreapta_jos.png")).convert_alpha()
        except Exception as e:
            print(f"Eroare asset-uri pereți: {e}")

        try:
            raw_floor = pygame.image.load(os.path.join(assets_path, "podea.png")).convert_alpha()
            self.floor_img = pygame.transform.scale(raw_floor, (TILE_SIZE, TILE_SIZE))
        except:
            self.floor_img = self._make_floor_tile()

        # ==========================================
        # 2. ÎNCĂRCARE TEXTURI OBIECTE
        # ==========================================
        try:
            self.door_closed_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "usa_inchisa2.png")).convert_alpha(),
                (TILE_SIZE, TILE_SIZE))
            self.door_open_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "usa_deschisa.png")).convert_alpha(),
                (TILE_SIZE, TILE_SIZE))
            self.chest_closed_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "cufar.png")).convert_alpha(), (TILE_SIZE, TILE_SIZE))
            self.chest_open_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "cufar_deschis.png")).convert_alpha(),
                (TILE_SIZE, TILE_SIZE))
            self.chest2_closed_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "cufar2_inchis.png")).convert_alpha(),
                (TILE_SIZE, TILE_SIZE))
            self.chest2_open_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "cufar2_deschis.png")).convert_alpha(),
                (TILE_SIZE, TILE_SIZE))

            dulap_w, dulap_h = TILE_SIZE * 2, int(TILE_SIZE * 2.2)
            self.dulap_closed_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "dulap_inchis1.png")).convert_alpha(), (dulap_w, dulap_h))
            self.dulap_open_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "dulap_deschis1.png")).convert_alpha(), (dulap_w, dulap_h))

            fotoliu_sz = int(TILE_SIZE * 1.8)
            self.fotoliu_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "fotoliu.png")).convert_alpha(), (fotoliu_sz, fotoliu_sz))
            self.fotoliu2_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "fotoliu2.png")).convert_alpha(), (fotoliu_sz, fotoliu_sz))
            self.spate_fotoliu_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "spate_fotoliu.png")).convert_alpha(),
                (fotoliu_sz, fotoliu_sz))

            self.bed_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "pat1.png")).convert_alpha(),
                (TILE_SIZE * 2, TILE_SIZE * 2))
            self.noptiera1_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "noptiera1.png")).convert_alpha(), (TILE_SIZE, TILE_SIZE))
            self.noptiera2_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "noptiera2.png")).convert_alpha(), (TILE_SIZE, TILE_SIZE))
            self.tablou_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "tablou.png")).convert_alpha(), (TILE_SIZE * 2, TILE_SIZE))

            self.lampa_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "lampa.png")).convert_alpha(),
                (int(TILE_SIZE * 0.9), int(TILE_SIZE * 0.9)))
            self.ceas_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "ceas.png")).convert_alpha(),
                (int(TILE_SIZE * 0.6), int(TILE_SIZE * 0.6)))
            self.rug1_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "covor1.png")).convert_alpha(),
                (TILE_SIZE * 2, TILE_SIZE * 2))
            self.rug2_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "covor3.png")).convert_alpha(),
                (TILE_SIZE * 2, TILE_SIZE * 2))

            self.semineu_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "semineu.png")).convert_alpha(),
                (TILE_SIZE * 2, TILE_SIZE * 2))
            self.birou_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "birou.png")).convert_alpha(),
                (TILE_SIZE * 2, int(TILE_SIZE * 1.5)))

            scaun_birou_sz = int(TILE_SIZE * 1.1)
            self.scaun_birou_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "scaun_birou.png")).convert_alpha(),
                (scaun_birou_sz, scaun_birou_sz))
            self.bookshelf_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "bookshelf.png")).convert_alpha(),
                (TILE_SIZE * 3, int(TILE_SIZE * 2.4)))

            self.frigider_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "frigider.png")).convert_alpha(),
                (int(TILE_SIZE * 1.3), TILE_SIZE * 2))
            self.mob_bucat_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "mobila_bucatarie.png")).convert_alpha(),
                (TILE_SIZE * 4, int(TILE_SIZE * 1.2)))
            self.mob_perete_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "mobila_perete_bucatarie.png")).convert_alpha(),
                (TILE_SIZE * 4, TILE_SIZE))
            self.masa_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "masa_bucatarie.png")).convert_alpha(),
                (TILE_SIZE * 3, int(TILE_SIZE * 1.5)))

            scaun_sz = int(TILE_SIZE * 0.9)
            self.scaun_spate_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "scaun_bucatarie_cu_spatele.png")).convert_alpha(),
                (scaun_sz, scaun_sz))
            self.scaun_fata_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "scaun_bucatarie_cu_fata.png")).convert_alpha(),
                (scaun_sz, scaun_sz))
            self.covor_bucat_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "covor_bucatarie.png")).convert_alpha(),
                (TILE_SIZE * 2, TILE_SIZE))

            canapea_w, canapea_h = int(TILE_SIZE * 2.8), int(TILE_SIZE * 1.5)
            self.canapea_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "canapea.png")).convert_alpha(), (canapea_w, canapea_h))
            self.spate_canapea_img = pygame.transform.scale(
                pygame.image.load(os.path.join(assets_path, "spate_canapea.png")).convert_alpha(),
                (canapea_w, canapea_h))
            self.tv_img = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "TV.png")).convert_alpha(),
                                                 (TILE_SIZE * 2, TILE_SIZE))

            # Terminale
            self.terminal_img = self.birou_img
        except Exception as e:
            print(f"Eroare încărcare asset-uri: {e}")

        self.walls_render = []
        self.wall_hitboxes = []
        self.doors = []
        self.chests = []
        self.deco_objects = []
        self.rugs_render = []
        self.terminals = []
        self.interact_distance = TILE_SIZE * 1.5

        # Layout
        self.layout = [
            "1WWWWWWWzWWWW2.1WWWWWWWWWWWW2.1WWzWWWWWWWWW2.1WWWWWWWWWWzW2",
            "VX.y....q...XM.VX....fk....XM.V.JP.L.....H.M.V..y..S.y...XM",
            "V.......i....M.V............M.V..c.........M.VY...........M",
            "VY...........M.V......m.....M.V............M.V.....O....T.M",
            "V............M.V............M.V..........X.M.VG.........i.M",
            "3BBBBBDBBBBBB4.3BBBBBDBBBBBB4.3BBBBBDBBBBBB4.3BBBBBDBBBBBB4",
            "...........................................................",
            "...........................................................",
            "1WWWWWDWWzWWW2.1WWWWWDWWzWWW2.1WWvWWDWWWWWW2.1WWWWWDWWWWWW2",
            "VH.F.......H.M.VX..........XM.VH.......LP.JM.VY.......F..XM",
            "V............M.V............M.V.........c..M.V............M",
            "VY...........M.V.....m......M.V............M.VG...........M",
            "V.....c....t.M.V............M.VY...........M.V............M",
            "VG...U.....O.M.VY..........YM.V..........O.M.VY...........M",
            "3BBBBBBBBBBBB4.3BBBBBBBBBBBB4.3BBBBBBBBBBBB4.3BBBBBBBBBBBB4",
        ]
        self.build_map()


    # 2. CONSTRUIREA HĂRȚII

    # Creează o textură simplă de rezervă pentru podea.
    def _make_floor_tile(self):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surf.fill((172, 172, 178))
        return surf

    # Parcurge matricea hărții și construiește pereții, obiectele și hitbox-urile.
    def build_map(self):
        self.wall_hitboxes.clear()
        self.walls_render.clear()
        self.doors.clear()
        self.chests.clear()
        self.deco_objects.clear()
        self.rugs_render.clear()
        self.terminals.clear()

        for r_idx, row in enumerate(self.layout):
            c_idx = 0
            while c_idx < len(row):
                char = row[c_idx]
                px, py = c_idx * TILE_SIZE, r_idx * TILE_SIZE

                wall_char = 'W' if char in ['W', 'z', 'v'] else char

                if wall_char in ['W', 'B', 'E', 'R']:
                    start_c = c_idx
                    while c_idx < len(row) and (
                            row[c_idx] == wall_char or (wall_char == 'W' and row[c_idx] in ['z', 'v'])):
                        c_idx += 1

                    num = c_idx - start_c
                    tex = \
                        {'W': self.tex_h_top, 'B': self.tex_h_bottom, 'E': self.tex_h_top_m, 'R': self.tex_h_bottom_m}[
                            wall_char]
                    img = pygame.transform.scale(tex, (num * TILE_SIZE, TILE_SIZE))

                    for i in range(num):
                        self.wall_hitboxes.append(pygame.Rect((start_c + i) * TILE_SIZE, py, TILE_SIZE, TILE_SIZE))

                    self.walls_render.append({'img': img, 'pos': (start_c * TILE_SIZE, py), 'y_sort': py + TILE_SIZE})
                    continue

                # Colțuri
                elif char in '1234':
                    img = [self.c_tl, self.c_tr, self.c_bl, self.c_br][int(char) - 1]
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
                    self.walls_render.append(
                        {'img': pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)), 'pos': (px, py),
                         'y_sort': py + TILE_SIZE})
                c_idx += 1

        # PASUL 2: GENERĂM OBIECTELE ȘI DECORURILE (Inclusiv z si v peste pereți)
        for r_idx, row in enumerate(self.layout):
            c_idx = 0
            while c_idx < len(row):
                char = row[c_idx]
                px, py = c_idx * TILE_SIZE, r_idx * TILE_SIZE

                if char == 'D':
                    is_quiz = random.random() < 0.60
                    self.doors.append({
                        'hitbox': pygame.Rect(px, py, TILE_SIZE, TILE_SIZE),
                        'is_open': False, 'pos': (px, py), 'y_sort': py + TILE_SIZE,
                        'is_quiz_door': is_quiz, 'is_unlocked': not is_quiz
                    })

                # --- SOLUȚIA PENTRU CUFERE ȘI DULAP ('H') ---
                elif char in ['X', 'Y', 'H']:
                    if char == 'X':
                        img_c, img_o = self.chest_closed_img, self.chest_open_img
                        w, draw_y, step = TILE_SIZE, py, 1
                    elif char == 'Y':
                        img_c, img_o = self.chest2_closed_img, self.chest2_open_img
                        w, draw_y, step = TILE_SIZE, py, 1
                    elif char == 'H':  # DULAP
                        img_c, img_o = self.dulap_closed_img, self.dulap_open_img
                        # Dulapul este mai înalt, îl desenăm mai sus pe Y, dar hitbox-ul rămâne jos la picioare
                        w, draw_y, step = TILE_SIZE * 2, py - int(TILE_SIZE * 1.2), 2

                    self.chests.append({
                        'hitbox': pygame.Rect(px, py, w, TILE_SIZE),
                        'is_open': False, 'player_inside': False, 'pos': (px, draw_y),
                        'y_sort': py + TILE_SIZE, 'img_c': img_c, 'img_o': img_o
                    })
                    c_idx += step;
                    continue

                elif char == 'T':
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE * 2, TILE_SIZE))
                    self.deco_objects.append(
                        {'img': self.terminal_img, 'pos': (px, py - int(TILE_SIZE * 0.3)), 'y_sort': py + TILE_SIZE})
                    self.terminals.append(pygame.Rect(px, py, TILE_SIZE * 2, TILE_SIZE))
                    c_idx += 2;
                    continue

                # --- AICI ADAUGĂM TABLOUL/TV-UL PESTE PERETE ---
                elif char == 'z':
                    self.deco_objects.append(
                        {'img': self.tablou_img, 'pos': (px, py + int(TILE_SIZE * 0.1)), 'y_sort': py + TILE_SIZE + 1})
                    c_idx += 1;
                    continue
                elif char == 'v':
                    self.deco_objects.append(
                        {'img': self.tv_img, 'pos': (px, py + int(TILE_SIZE * 0.1)), 'y_sort': py + TILE_SIZE + 1})
                    c_idx += 1;
                    continue

                elif char == 'q':
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE * 2, TILE_SIZE))
                    self.deco_objects.append(
                        {'img': self.birou_img, 'pos': (px, py - int(TILE_SIZE * 0.3)), 'y_sort': py + TILE_SIZE})
                    c_idx += 2;
                    continue
                elif char == 'i':
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
                    self.deco_objects.append(
                        {'img': self.scaun_birou_img, 'pos': (px, py - int(TILE_SIZE * 0.1)), 'y_sort': py + TILE_SIZE})
                elif char == 'y':
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE * 3, TILE_SIZE))
                    self.deco_objects.append(
                        {'img': self.bookshelf_img, 'pos': (px, py - int(TILE_SIZE * 1.4)), 'y_sort': py + TILE_SIZE})
                    c_idx += 3;
                    continue
                elif char == 'f':
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
                    self.deco_objects.append(
                        {'img': self.frigider_img, 'pos': (px, py - TILE_SIZE), 'y_sort': py + TILE_SIZE})
                elif char == 'k':
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE * 4, int(TILE_SIZE * 1.2)))
                    self.deco_objects.append({'img': self.mob_bucat_img, 'pos': (px, py), 'y_sort': py + TILE_SIZE})
                    self.deco_objects.append(
                        {'img': self.mob_perete_img, 'pos': (px, py - int(TILE_SIZE * 0.9)), 'y_sort': py})
                    c_idx += 4;
                    continue
                elif char == 'm':
                    self.wall_hitboxes.append(
                        pygame.Rect(px, py + int(TILE_SIZE * 0.3), TILE_SIZE * 3, int(TILE_SIZE * 0.8)))
                    self.deco_objects.append(
                        {'img': self.masa_img, 'pos': (px, py), 'y_sort': py + TILE_SIZE + int(TILE_SIZE * 0.5)})
                    ox1, ox2, ox3 = int(TILE_SIZE * 0.2), TILE_SIZE + int(TILE_SIZE * 0.1), TILE_SIZE * 2
                    sy_spate, sy_fata = py - int(TILE_SIZE * 0.4), py + int(TILE_SIZE * 0.8)
                    self.deco_objects.extend(
                        [{'img': self.scaun_spate_img, 'pos': (px + ox1, sy_spate), 'y_sort': py + TILE_SIZE - 10},
                         {'img': self.scaun_spate_img, 'pos': (px + ox2, sy_spate), 'y_sort': py + TILE_SIZE - 10},
                         {'img': self.scaun_spate_img, 'pos': (px + ox3, sy_spate), 'y_sort': py + TILE_SIZE - 10}])
                    self.deco_objects.extend(
                        [{'img': self.scaun_fata_img, 'pos': (px + ox1, sy_fata), 'y_sort': py + TILE_SIZE * 2},
                         {'img': self.scaun_fata_img, 'pos': (px + ox2, sy_fata), 'y_sort': py + TILE_SIZE * 2},
                         {'img': self.scaun_fata_img, 'pos': (px + ox3, sy_fata), 'y_sort': py + TILE_SIZE * 2}])
                    c_idx += 3;
                    continue
                elif char in 'CU':
                    self.wall_hitboxes.append(pygame.Rect(px, py, int(TILE_SIZE * 2.8), TILE_SIZE))
                    img = self.canapea_img if char == 'C' else self.spate_canapea_img
                    self.deco_objects.append(
                        {'img': img, 'pos': (px, py - int(TILE_SIZE * 0.2)), 'y_sort': py + TILE_SIZE})
                    c_idx += 2;
                    continue
                elif char == 'S':
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE * 2, TILE_SIZE))
                    self.deco_objects.append(
                        {'img': self.semineu_img, 'pos': (px, py - TILE_SIZE), 'y_sort': py + TILE_SIZE})
                    c_idx += 2;
                    continue
                elif char in 'FGO':
                    img = self.fotoliu_img if char == 'F' else (
                        self.fotoliu2_img if char == 'G' else self.spate_fotoliu_img)
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
                    f_off_x, f_off_y = (TILE_SIZE - img.get_width()) // 2, (TILE_SIZE - img.get_height())
                    self.deco_objects.append(
                        {'img': img, 'pos': (px + f_off_x, py + f_off_y), 'y_sort': py + TILE_SIZE})
                elif char == 'P':
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE * 2, TILE_SIZE * 2))
                    self.deco_objects.append({'img': self.bed_img, 'pos': (px, py), 'y_sort': py + TILE_SIZE * 2})
                    c_idx += 2;
                    continue
                elif char == 'J':
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
                    self.deco_objects.append({'img': self.noptiera1_img, 'pos': (px, py), 'y_sort': py + TILE_SIZE})
                    self.deco_objects.append({'img': self.lampa_img,
                                              'pos': (px + (TILE_SIZE - self.lampa_img.get_width()) // 2,
                                                      py - self.lampa_img.get_height() + int(TILE_SIZE * 0.3)),
                                              'y_sort': py + TILE_SIZE + 1})
                elif char == 'L':
                    self.wall_hitboxes.append(pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
                    self.deco_objects.append({'img': self.noptiera2_img, 'pos': (px, py), 'y_sort': py + TILE_SIZE})
                    self.deco_objects.append({'img': self.ceas_img,
                                              'pos': (px + (TILE_SIZE - self.ceas_img.get_width()) // 2,
                                                      py - self.ceas_img.get_height() + int(TILE_SIZE * 0.3)),
                                              'y_sort': py + TILE_SIZE + 1})

                # --- SOLUȚIA PENTRU COVOARE ---
                elif char in ['t', 'c']:
                    rug_img = self.rug1_img if char == 't' else self.rug2_img
                    # y_sort = 0 forțează covoarele să fie desenate imediat după podea
                    self.deco_objects.append({'img': rug_img, 'pos': (px, py), 'y_sort': 0})
                    c_idx += 2;
                    continue

                c_idx += 1

        # Pereți verticali
        v_vis = set()
        for c in range(len(self.layout[0])):
            for r in range(len(self.layout)):
                char = self.layout[r][c]
                if char in ['M', 'V'] and (r, c) not in v_vis:
                    start_r = r
                    while r < len(self.layout) and self.layout[r][c] == char:
                        v_vis.add((r, c));
                        r += 1
                    num = r - start_r
                    tex = self.tex_v_left if char == 'M' else self.tex_v_right
                    px, py = c * TILE_SIZE, start_r * TILE_SIZE
                    img = pygame.transform.scale(tex, (TILE_SIZE, num * TILE_SIZE))
                    for i in range(num): self.wall_hitboxes.append(
                        pygame.Rect(px, py + i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    self.walls_render.append({'img': img, 'pos': (px, py), 'y_sort': py + num * TILE_SIZE})

    @property

    # 3. COLIZIUNI ȘI RANDARE

    # Returnează lista hitbox-urilor folosite pentru coliziuni.
    def walls(self):
        collision_list = self.wall_hitboxes.copy()
        for d in self.doors:
            if not d['is_open']: collision_list.append(d['hitbox'])
        for c in self.chests:
            if not c['player_inside']: collision_list.append(c['hitbox'])
        return collision_list

    # Desenează podeaua repetitiv în zona vizibilă a camerei.
    def draw_floor(self, screen, camera=None):
        for r in range(len(self.layout)):
            for c in range(len(self.layout[0])):
                pos = camera.apply((c * TILE_SIZE, r * TILE_SIZE)) if camera else (c * TILE_SIZE, r * TILE_SIZE)
                screen.blit(self.floor_img, pos)
        for r in self.rugs_render:
            pos = camera.apply(r['pos']) if camera else r['pos']
            screen.blit(r['img'], pos)

    # Desenează obiectele și personajele în ordinea coordonatei Y.
    def draw_elements_sorted(self, screen, player, camera=None):
        render_list = list(self.walls_render)
        for d in self.doors: render_list.append(
            {'img': self.door_open_img if d['is_open'] else self.door_closed_img, 'pos': d['pos'],
             'y_sort': d['y_sort']})
        for c in self.chests: render_list.append(
            {'img': c['img_o'] if c['is_open'] else c['img_c'], 'pos': c['pos'], 'y_sort': c['y_sort']})
        for deco in self.deco_objects: render_list.append(deco)
        if not any(c['player_inside'] for c in self.chests):
            p = player.get_render_data()
            if p: render_list.append(p)
        render_list.sort(key=lambda item: item['y_sort'])
        for item in render_list:
            pos = camera.apply(item['pos']) if camera else item['pos']
            screen.blit(item['img'], pos)


    # 4. INTERACȚIUNILE CU OBIECTELE

    # Verifică ușile apropiate și returnează ușa cu care interacționează jucătorul.
    def interact_door(self, player):
        for d in self.doors:
            if math.hypot(player.rect.centerx - d['hitbox'].centerx,
                          player.rect.centery - d['hitbox'].centery) < self.interact_distance:
                if d['is_unlocked']: d['is_open'] = not d['is_open']; return None
                return d
        return None

    # Gestionează intrarea și ieșirea jucătorului din ascunzători.
    def interact_chest(self, player, action):
        for c in self.chests:
            if c['player_inside'] or math.hypot(player.rect.centerx - c['hitbox'].centerx,
                                                player.rect.centery - c['hitbox'].centery) < self.interact_distance:
                if action == 'toggle':
                    c['is_open'] = not c['is_open']
                elif action == 'hide' and (c['is_open'] or c['player_inside']):
                    c['player_inside'] = not c['player_inside']
                    if c['player_inside']:
                        player.rect.center = c['hitbox'].center
                    else:
                        player.rect.y += TILE_SIZE
                break
