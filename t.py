import pygame

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Camera variables
zoom_scale = 1.0
scroll_x = 0
scroll_y = 0

# Create a sample surface to zoom into (a grid)
world_surf = pygame.Surface((2000, 2000))
world_surf.fill((30, 30, 30))
for x in range(0, 2000, 100):
    pygame.draw.line(world_surf, (100, 100, 100), (x, 0), (x, 2000), 2)
for y in range(0, 2000, 100):
    pygame.draw.line(world_surf, (100, 100, 100), (0, y), (2000, y), 2)
pygame.draw.circle(world_surf, (255, 50, 50), (1000, 1000), 50)  # Center marker

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Only trigger on scroll wheel
            if event.button in (4, 5): 
                # 1. Calculate mouse pos in world coordinates before zoom change
                mouse_world_x = (mouse_pos[0] - scroll_x) / zoom_scale
                mouse_world_y = (mouse_pos[1] - scroll_y) / zoom_scale
                
                # 2. Update the zoom factor
                if event.button == 4:    # Scroll Up (Zoom In)
                    zoom_scale *= 1.1
                elif event.button == 5:  # Scroll Down (Zoom Out)
                    zoom_scale /= 1.1
                    
                # Limit zoom features to avoid crashing or extremes
                zoom_scale = max(0.1, min(zoom_scale, 10.0))
                
                # 3. Adjust scroll so the mouse stays over the same world position
                scroll_x = mouse_pos[0] - mouse_world_x * zoom_scale
                scroll_y = mouse_pos[1] - mouse_world_y * zoom_scale

    # Dragging to pan around the map (Optional quality of life feature)
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]: # Left click drag
        rel = pygame.mouse.get_rel()
        scroll_x += rel[0]
        scroll_y += rel[1]
    else:
        pygame.mouse.get_rel() # Reset relative movement when not clicking

    # Drawing
    screen.fill((0, 0, 0))
    
    # Scale the world surface based on current zoom factor
    new_size = (int(world_surf.get_width() * zoom_scale), int(world_surf.get_height() * zoom_scale))
    scaled_surf = pygame.transform.scale(world_surf, new_size)
    
    # Blit the scaled surface at our adjusted scroll coordinates
    screen.blit(scaled_surf, (scroll_x, scroll_y))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
