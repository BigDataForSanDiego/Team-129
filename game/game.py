import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Slider Example')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# List of points (you can change these to your desired coordinates)
points = [(100, 100), (200, 200), (300, 150), (400, 300)]

# Slider bar parameters
slider_bar_rect = pygame.Rect(50, HEIGHT - 50, WIDTH - 100, 10)

# Slider handle parameters
slider_handle_radius = 10
slider_handle_pos = [slider_bar_rect.left, slider_bar_rect.centery]

# Slider value between 0 and 1
slider_value = 0

# Dragging flag
dragging = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is over the slider handle
            mouse_pos = pygame.mouse.get_pos()
            dx = mouse_pos[0] - slider_handle_pos[0]
            dy = mouse_pos[1] - slider_handle_pos[1]
            if dx * dx + dy * dy <= slider_handle_radius ** 2:
                dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                # Move the slider handle
                mouse_x = pygame.mouse.get_pos()[0]
                # Clamp the handle position to the slider bar
                slider_handle_pos[0] = max(slider_bar_rect.left, min(mouse_x, slider_bar_rect.right))
                # Update slider value
                slider_value = (slider_handle_pos[0] - slider_bar_rect.left) / slider_bar_rect.width
                # Ensure slider_value is between 0 and 1
                slider_value = max(0, min(slider_value, 1))
    
    # Clear screen
    screen.fill(WHITE)

    # Draw the slider bar
    pygame.draw.rect(screen, BLACK, slider_bar_rect)

    # Draw the slider handle
    pygame.draw.circle(screen, RED, (int(slider_handle_pos[0]), int(slider_handle_pos[1])), slider_handle_radius)

    # Draw the points
    for point in points:
        pygame.draw.circle(screen, BLACK, point, 5)

    # Draw lines between the points based on the slider value
    num_points = len(points)
    total_lines = num_points - 1
    num_lines_to_draw = int(slider_value * total_lines + 0.5)  # Round to nearest integer

    for i in range(num_lines_to_draw):
        pygame.draw.line(screen, RED, points[i], points[i + 1], 2)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
