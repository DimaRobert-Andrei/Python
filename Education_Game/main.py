
import pygame
from settings import *
from player import Player
from map import GameMap
import ap1_manager
from npc import EnemyNPC

# --- INIȚIALIZARE ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hide & Seek: Hacker Edition")
clock = pygame.time.Clock()

# --- DIMENSIUNI CALCULATE ---
MAP_PIXEL_WIDTH = 59 * TILE_SIZE
MAP_PIXEL_HEIGHT = 15 * TILE_SIZE

game_map = GameMap(MAP_PIXEL_WIDTH, MAP_PIXEL_HEIGHT)
player = Player(MAP_PIXEL_WIDTH // 2, 7 * TILE_SIZE)

# Spawnăm NPC-ul pe coridor
enemy = EnemyNPC((MAP_PIXEL_WIDTH // 2) + 300, 7 * TILE_SIZE + 16, game_map)



# 1. SISTEMUL DE CAMERĂ

class Camera:
    # Inițializează dreptunghiul camerei și dimensiunile hărții.
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width, self.height = width, height

    # Transformă o poziție din coordonate globale în coordonate vizibile pe ecran.
    def apply(self, pos):
        return (pos[0] + self.camera.x, pos[1] + self.camera.y)

    # Centrează camera pe jucător și o limitează la marginile hărții.
    def update(self, target):
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2
        x = min(0, max(-(self.width - SCREEN_WIDTH), x))
        y = min(0, max(-(self.height - SCREEN_HEIGHT), y))
        self.camera = pygame.Rect(x, y, self.width, self.height)


camera = Camera(MAP_PIXEL_WIDTH, MAP_PIXEL_HEIGHT)

# --- LOGICĂ ---
current_round = 1
max_rounds = 5
grace_timer = 5 * FPS
round_duration = 60 * FPS
game_state = "GRACE_PERIOD"
previous_state = None  # Pentru a reține starea înainte de pauză
active_question = None
current_door = None


# --- FUNCȚII UI JOC ---

# 2. INTERFAȚA JOCULUI

# Desenează bara de stamină și schimbă culoarea când nivelul este scăzut.
def draw_stamina_bar(screen, player, x, y):
    bar_width = 150
    bar_height = 10
    fill = (player.current_stamina / player.max_stamina) * bar_width
    pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
    color = (0, 255, 100) if player.current_stamina > 30 else (255, 50, 50)
    pygame.draw.rect(screen, color, (x, y, fill, bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 1)


# Desenează ecranul întrebării, variantele și mesajul de încărcare.
def draw_quiz_ui(screen, question, skill_level, is_loading=False):
    s_width = screen.get_width()
    s_height = screen.get_height()
    margin = 40
    box_width = s_width - (margin * 2)
    box_height = s_height - (margin * 2)
    box_rect = pygame.Rect(margin, margin, box_width, box_height)
    overlay = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    overlay.fill((15, 20, 30, 240))
    screen.blit(overlay, (margin, margin))
    pygame.draw.rect(screen, (0, 255, 200), box_rect, 3)
    font_title = pygame.font.SysFont('courier', 22, bold=True)
    font_text = pygame.font.SysFont('courier', 16)
    title_surf = font_title.render(f"--- TERMINAL: DEBLOCARE USA (Runda {skill_level}) ---", True, (0, 255, 200))
    screen.blit(title_surf, (margin + 20, margin + 20))

    # Împarte textul pe mai multe rânduri ca să încapă în fereastră.
    def draw_wrapped_text(surface, text, font, color, x, y, max_w):
        words = str(text).split(' ')
        lines, current_line = [], []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_w:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        y_offset = y
        for line in lines:
            surf = font.render(line, True, color)
            surface.blit(surf, (x, y_offset))
            y_offset += font.get_linesize() + 2
        return y_offset

    current_y = margin + 80
    max_text_width = box_width - 40
    if is_loading or question is None:
        draw_wrapped_text(screen, "Connecting to local AI... Please wait.", font_title, (0, 255, 0), margin + 20,
                          current_y, max_text_width)
    else:
        current_y = draw_wrapped_text(screen, f"Q: {question['q']}", font_title, (255, 255, 255), margin + 20,
                                      current_y, max_text_width)
        current_y += 30
        options = [(f"[A] {question['A']}", (200, 200, 200)), (f"[B] {question['B']}", (200, 200, 200)),
                   (f"[C] {question['C']}", (200, 200, 200)), (f"[D] {question['D']}", (200, 200, 200))]
        for opt_text, color in options:
            current_y = draw_wrapped_text(screen, opt_text, font_text, color, margin + 20, current_y, max_text_width)
            current_y += 15





# 3. MENIUL PRINCIPAL

# Gestionează meniul principal, ecranul de detalii și butoanele.
def show_main_menu(screen, clock, game_map, player, enemy, camera):
    camera.update(player)

    font_title = pygame.font.SysFont('courier', 50, bold=True)
    font_btn = pygame.font.SysFont('courier', 25, bold=True)
    font_text = pygame.font.SysFont('courier', 18)

    btn_w, btn_h = 220, 60
    btn_play = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, 250, btn_w, btn_h)
    btn_details = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, 340, btn_w, btn_h)
    btn_quit = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, 430, btn_w, btn_h)
    btn_back = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, 500, btn_w, btn_h)

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 15, 20, 180))

    in_menu = True
    show_details = False

    while in_menu:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_details:
                    if btn_back.collidepoint(event.pos):
                        show_details = False
                else:
                    if btn_play.collidepoint(event.pos):
                        return True
                    if btn_details.collidepoint(event.pos):
                        show_details = True
                    if btn_quit.collidepoint(event.pos):
                        return False

        start_x = camera.camera.x % TILE_SIZE - TILE_SIZE
        start_y = camera.camera.y % TILE_SIZE - TILE_SIZE
        for x in range(start_x, SCREEN_WIDTH + TILE_SIZE, TILE_SIZE):
            for y in range(start_y, SCREEN_HEIGHT + TILE_SIZE, TILE_SIZE):
                screen.blit(game_map.floor_img, (x, y))

        game_map.draw_elements_sorted(screen, player, camera)
        enemy.draw(screen, camera)

        screen.blit(overlay, (0, 0))

        if show_details:
            title_surf = font_title.render("DETALII JOC", True, (0, 255, 255))
            screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 80))

            instructions = [
                "OBIECTIV:",
                "- Rezolva puzzle-urile de programare (Python) de la usi.",
                "- Supravietuieste celor 5 runde si fereste-te de AI.",
                "",
                "CONTROALE:",
                "- [W, A, S, D] : Miscare personaj",
                "- [SHIFT]      : Sprint (consuma Stamina)",
                "- [E]          : Interactiunea (Usi / Cufere)",
                "- [H]          : Ascunde-te (in interiorul cuferelor)",
                "- [ESC]        : Meniu Pauza"
            ]

            y_offset = 180
            for line in instructions:
                txt_surf = font_text.render(line, True, (200, 220, 220))
                screen.blit(txt_surf, (SCREEN_WIDTH // 2 - 250, y_offset))
                y_offset += 30

            color_back = (0, 255, 150) if btn_back.collidepoint(mouse_pos) else (0, 150, 100)
            pygame.draw.rect(screen, color_back, btn_back, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), btn_back, 2, border_radius=8)
            back_txt = font_btn.render("INAPOI", True, (255, 255, 255))
            screen.blit(back_txt,
                        (btn_back.centerx - back_txt.get_width() // 2, btn_back.centery - back_txt.get_height() // 2))

        else:
            title_surf = font_title.render("HIDE & SEEK: HACKER", True, (0, 255, 100))
            screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 100))

            for btn, text in [(btn_play, "START JOC"), (btn_details, "DETALII"), (btn_quit, "IESIRE")]:
                color = (0, 200, 100) if btn.collidepoint(mouse_pos) else (0, 100, 50)
                if text == "IESIRE":
                    color = (200, 50, 50) if btn.collidepoint(mouse_pos) else (120, 30, 30)

                pygame.draw.rect(screen, color, btn, border_radius=8)
                pygame.draw.rect(screen, (255, 255, 255), btn, 2, border_radius=8)

                txt_surf = font_btn.render(text, True, (255, 255, 255))
                screen.blit(txt_surf,
                            (btn.centerx - txt_surf.get_width() // 2, btn.centery - txt_surf.get_height() // 2))

        pygame.display.flip()



# STRUCTURAREA ȘI PORNIREA JOCULUI

continue_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 50, 250, 60)

# Butoanele pentru meniul de pauză
pause_btn_w, pause_btn_h = 220, 60
btn_resume = pygame.Rect(SCREEN_WIDTH // 2 - pause_btn_w // 2, SCREEN_HEIGHT // 2 - 40, pause_btn_w, pause_btn_h)
btn_quit_game = pygame.Rect(SCREEN_WIDTH // 2 - pause_btn_w // 2, SCREEN_HEIGHT // 2 + 50, pause_btn_w, pause_btn_h)

start_game = show_main_menu(screen, clock, game_map, player, enemy, camera)
running = start_game

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state in ["ROUND_COMPLETE", "GAME_OVER"] and continue_button_rect.collidepoint(event.pos):
                current_round += 1

                if current_round > max_rounds:
                    game_state = "GAME_FINISHED"
                else:
                    game_state = "GRACE_PERIOD"
                    grace_timer = 5 * FPS
                    round_duration = 60 * FPS

                    player.rect.center = (MAP_PIXEL_WIDTH // 2, 7 * TILE_SIZE)
                    enemy.reset_round((MAP_PIXEL_WIDTH // 2) + 300, 7 * TILE_SIZE + 16)
                    enemy.set_difficulty(current_round)

                    if hasattr(game_map, 'doors'):
                        for door in game_map.doors:
                            door['is_unlocked'], door['is_open'] = False, False
                    if hasattr(game_map, 'chests'):
                        for chest in game_map.chests:
                            chest['player_inside'], chest['is_open'] = False, False

            elif game_state == "GAME_FINISHED" and continue_button_rect.collidepoint(event.pos):
                running = False

            # Logica pentru click în meniul de pauză
            elif game_state == "PAUSED":
                if btn_resume.collidepoint(event.pos):
                    game_state = previous_state  # Revenim la starea de dinainte de pauză
                if btn_quit_game.collidepoint(event.pos):
                    running = False  # Iesim din joc

        if event.type == pygame.KEYDOWN:
            # Apăsare pe ESC pentru a pune pauză sau a ieși din pauză
            if event.key == pygame.K_ESCAPE:
                if game_state in ["EXPLORING", "GRACE_PERIOD"]:
                    previous_state = game_state
                    game_state = "PAUSED"
                elif game_state == "PAUSED":
                    game_state = previous_state

            if game_state in ["EXPLORING", "GRACE_PERIOD"]:
                if event.key == pygame.K_e:
                    door = game_map.interact_door(player)
                    if door:
                        current_door = door
                        game_state = "LOADING_QUIZ"
                        ap1_manager.request_new_question(current_round)
                    game_map.interact_chest(player, 'toggle')
                elif event.key == pygame.K_h:
                    game_map.interact_chest(player, 'hide')

            elif game_state == "QUIZ_DOOR":
                key_map = {pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C', pygame.K_d: 'D'}
                if event.key in key_map:
                    if key_map[event.key] == active_question['correct']:
                        current_door['is_unlocked'], current_door['is_open'] = True, True
                    game_state = "EXPLORING"

    # LOGICĂ TIMP ȘI STARE NPC (Se execută DOAR dacă jocul NU este pe pauză)
    if game_state == "GRACE_PERIOD":
        grace_timer -= 1
        enemy.state = "WAITING"
        if grace_timer <= 0:
            game_state = "EXPLORING"
            round_duration = 60 * FPS
            enemy.set_difficulty(current_round)
            enemy.state = "PATROL"

    elif game_state == "EXPLORING":
        round_duration -= 1
        if round_duration <= 0:
            game_state = "ROUND_COMPLETE"

    # UPDATE MIȘCĂRI
    keys = pygame.key.get_pressed()
    is_hidden = False
    if hasattr(game_map, 'chests'):
        is_hidden = any(c['player_inside'] for c in game_map.chests)

    if not is_hidden:
        if game_state in ["EXPLORING", "GRACE_PERIOD"]:
            player.move(keys, game_map.walls)

    if game_state == "EXPLORING":
        enemy.update(player)

        if hasattr(game_map, 'chests'):
            is_hidden = any(c['player_inside'] for c in game_map.chests)

        if enemy.caught_player or (not is_hidden and enemy.rect.colliderect(player.rect)):
            game_state = "GAME_OVER"

    # FIX ANTI-FREEZE LA GENERAREA INTREBARII
    if game_state == "LOADING_QUIZ":
        pygame.event.pump()
        pygame.time.delay(10)

        if ap1_manager.current_fetched_question:
            active_question = ap1_manager.current_fetched_question
            game_state = "QUIZ_DOOR"

    camera.update(player)

    # --- RENDER JOC ---
    screen.fill((15, 15, 15))

    start_x = camera.camera.x % TILE_SIZE - TILE_SIZE
    start_y = camera.camera.y % TILE_SIZE - TILE_SIZE
    for x in range(start_x, SCREEN_WIDTH + TILE_SIZE, TILE_SIZE):
        for y in range(start_y, SCREEN_HEIGHT + TILE_SIZE, TILE_SIZE):
            screen.blit(game_map.floor_img, (x, y))

    game_map.draw_elements_sorted(screen, player, camera)
    enemy.draw(screen, camera)

    # --- UI HUD JOC ---
    ui_bg = pygame.Surface((280, 70), pygame.SRCALPHA)
    ui_bg.fill((0, 0, 0, 180))
    screen.blit(ui_bg, (15, 15))
    pygame.draw.rect(screen, (255, 215, 0), (15, 15, 280, 70), 2)

    font_ui = pygame.font.SysFont('courier', 18, bold=True)
    display_round = min(current_round, max_rounds)
    screen.blit(font_ui.render(f"RUNDA: {display_round} / {max_rounds}", True, (255, 215, 0)), (25, 25))

    timer_msg = f"INTRUS IN: {grace_timer // FPS}s" if game_state == "GRACE_PERIOD" else f"TIMP RUNDA: {round_duration // FPS}s"
    if game_state in ["ROUND_COMPLETE", "GAME_OVER", "GAME_FINISHED", "PAUSED"]:
        if game_state != "PAUSED":
            timer_msg = "RUNDA TERMINATA"
    screen.blit(font_ui.render(timer_msg, True, (255, 255, 255)), (25, 48))

    font_small = pygame.font.SysFont('courier', 14)
    instr_txt = font_small.render("WASD: Move | E: Interact | H: Hide | SHIFT: Sprint", True, (255, 255, 255))
    screen.blit(instr_txt, (20, SCREEN_HEIGHT - 25))
    if not is_hidden: draw_stamina_bar(screen, player, SCREEN_WIDTH - 175, SCREEN_HEIGHT - 25)

    if game_state == "LOADING_QUIZ":
        draw_quiz_ui(screen, None, current_round, is_loading=True)
    elif game_state == "QUIZ_DOOR":
        draw_quiz_ui(screen, active_question, current_round, is_loading=False)

    # --- ECRANE DE FINAL / PAUZĂ ---
    elif game_state == "PAUSED":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        font_large = pygame.font.SysFont('courier', 60, bold=True)
        pause_text = font_large.render("PAUZA", True, (0, 255, 255))
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 140))

        mouse_pos = pygame.mouse.get_pos()

        # Desenare buton RESUME
        color_res = (0, 200, 100) if btn_resume.collidepoint(mouse_pos) else (0, 100, 50)
        pygame.draw.rect(screen, color_res, btn_resume, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), btn_resume, 3, border_radius=10)
        font_btn = pygame.font.SysFont('courier', 24, bold=True)
        res_txt = font_btn.render("RESUME", True, (255, 255, 255))
        screen.blit(res_txt,
                    (btn_resume.centerx - res_txt.get_width() // 2, btn_resume.centery - res_txt.get_height() // 2))

        # Desenare buton IESIRE
        color_q = (200, 50, 50) if btn_quit_game.collidepoint(mouse_pos) else (120, 30, 30)
        pygame.draw.rect(screen, color_q, btn_quit_game, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), btn_quit_game, 3, border_radius=10)
        q_txt = font_btn.render("IESIRE", True, (255, 255, 255))
        screen.blit(q_txt,
                    (btn_quit_game.centerx - q_txt.get_width() // 2, btn_quit_game.centery - q_txt.get_height() // 2))

    elif game_state == "ROUND_COMPLETE":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        font_large = pygame.font.SysFont('courier', 50, bold=True)
        win_text = font_large.render(f"RUNDA {display_round} COMPLETA!", True, (0, 255, 100))
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        mouse_pos = pygame.mouse.get_pos()
        btn_color = (0, 200, 100) if continue_button_rect.collidepoint(mouse_pos) else (0, 120, 50)
        pygame.draw.rect(screen, btn_color, continue_button_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), continue_button_rect, 3, border_radius=10)
        font_btn = pygame.font.SysFont('courier', 24, bold=True)
        btn_text = font_btn.render("URMATOAREA RUNDA", True, (255, 255, 255))
        screen.blit(btn_text, (continue_button_rect.centerx - btn_text.get_width() // 2,
                               continue_button_rect.centery - btn_text.get_height() // 2))

    elif game_state == "GAME_OVER":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((150, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        font_large = pygame.font.SysFont('courier', 50, bold=True)
        lose_text = font_large.render("AI-UL TE-A PRINS!", True, (255, 50, 50))
        screen.blit(lose_text, (SCREEN_WIDTH // 2 - lose_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        mouse_pos = pygame.mouse.get_pos()
        btn_color = (200, 50, 50) if continue_button_rect.collidepoint(mouse_pos) else (120, 0, 0)
        pygame.draw.rect(screen, btn_color, continue_button_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), continue_button_rect, 3, border_radius=10)
        font_btn = pygame.font.SysFont('courier', 24, bold=True)
        btn_text = font_btn.render("URMATOAREA RUNDA", True, (255, 255, 255))
        screen.blit(btn_text, (continue_button_rect.centerx - btn_text.get_width() // 2,
                               continue_button_rect.centery - btn_text.get_height() // 2))

    elif game_state == "GAME_FINISHED":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 50, 200))
        screen.blit(overlay, (0, 0))
        font_large = pygame.font.SysFont('courier', 50, bold=True)
        win_text = font_large.render("JOC TERMINAT!", True, (0, 255, 255))
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        font_med = pygame.font.SysFont('courier', 20, bold=True)
        sub_text = font_med.render("Ai terminat toate cele 5 runde.", True, (200, 200, 200))
        screen.blit(sub_text, (SCREEN_WIDTH // 2 - sub_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))

        mouse_pos = pygame.mouse.get_pos()
        btn_color = (0, 150, 200) if continue_button_rect.collidepoint(mouse_pos) else (0, 80, 120)
        pygame.draw.rect(screen, btn_color, continue_button_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), continue_button_rect, 3, border_radius=10)
        font_btn = pygame.font.SysFont('courier', 24, bold=True)
        btn_text = font_btn.render("IESIRE", True, (255, 255, 255))
        screen.blit(btn_text, (continue_button_rect.centerx - btn_text.get_width() // 2,
                               continue_button_rect.centery - btn_text.get_height() // 2))

    pygame.display.flip()

pygame.quit()
