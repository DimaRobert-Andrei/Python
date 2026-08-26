
TILE_SIZE = 40 

MAP_COLUMNS = 36
MAP_ROWS = 16

# Calculăm automat dimensiunea ferestrei ca să încapă toată harta!
SCREEN_WIDTH = MAP_COLUMNS * TILE_SIZE
SCREEN_HEIGHT = (MAP_ROWS * TILE_SIZE) + 40 # pentru textul cu instrucțiuni

FPS = 60