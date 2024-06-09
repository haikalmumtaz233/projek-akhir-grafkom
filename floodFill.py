import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Dimensi layar
WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Flood Fill")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Membuat fungsi untuk melakukan flood fill
def flood_fill(surface, x, y, fill_color, old_color):
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return
    if surface.get_at((x, y)) != old_color:
        return
    surface.set_at((x, y), fill_color)
    flood_fill(surface, x + 1, y, fill_color, old_color)
    flood_fill(surface, x - 1, y, fill_color, old_color)
    flood_fill(surface, x, y + 1, fill_color, old_color)
    flood_fill(surface, x, y - 1, fill_color, old_color)
    
# Fungsi untuk menggambar contoh
def draw_example(surface):
    surface.fill(WHITE)
    pygame.draw.rect(surface, BLACK, (50, 50, 200, 200)) # Kotak hitam
    pygame.draw.circle(surface, BLACK, (500, 200), 100) # Lingkaran hitam
    pygame.draw.rect(surface, RED, (300, 400, 200, 100)) # Kotak merah
    pygame.draw.circle(surface, GREEN, (700, 400), 100) # Lingkaran hijau
    
# Main loop
def main():
    draw_example(SCREEN)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
            # Ambil posisi mouse
                mouse_pos = pygame.mouse.get_pos()
            # Ambil warna pixel di posisi mouse
                pixel_color = SCREEN.get_at(mouse_pos)
            # Flood fill dari posisi mouse dengan warna random
                flood_fill(SCREEN, mouse_pos[0], mouse_pos[1], BLUE, 
                pixel_color)
    
        pygame.display.flip()
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()
