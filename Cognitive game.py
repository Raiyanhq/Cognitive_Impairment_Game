import pygame
import random
import time

pygame.init()


WIDTH, HEIGHT = 800, 600
CARD_SIZE = 100
GRID_SIZE = 4
GRID_DIMENSION = GRID_SIZE * GRID_SIZE


WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cognitive Impairment Memory Game")


card_images = []
for i in range(1, GRID_DIMENSION // 2 + 1):
    image = pygame.image.load(f'card{i}.png')
    card_images.extend([image, image])

# Shuffle the cards
random.shuffle(card_images)

cards = [None] * GRID_DIMENSION
for i in range(GRID_DIMENSION):
    row, col = divmod(i, GRID_SIZE)
    x, y = col * CARD_SIZE, row * CARD_SIZE
    cards[i] = {
        "image": card_images[i],
        "rect": pygame.Rect(x, y, CARD_SIZE, CARD_SIZE),
        "visible": False,
    }

first_card = None
pairs_found = 0
clickable = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if clickable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, card in enumerate(cards):
                    if card["rect"].collidepoint(event.pos) and not card["visible"]:
                        card["visible"] = True
                        if first_card is None:
                            first_card = i
                        else:
                            # Compare the two cards
                            if card_images[i] == card_images[first_card]:
                                pairs_found += 1
                                if pairs_found == GRID_DIMENSION // 2:
                                    print("Congratulations! You've won!")
                                    clickable = False
                            else:
                                time.sleep(1)  # Delay for a moment
                                cards[i]["visible"] = cards[first_card]["visible"] = False
                            first_card = None

    screen.fill(WHITE)
    for card in cards:
        if card["visible"]:
            screen.blit(card["image"], card["rect"].topleft)
        else:
            pygame.draw.rect(screen, GRAY, card["rect"])
    pygame.display.flip()


pygame.quit()
