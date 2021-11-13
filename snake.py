import pygame
import time
import random

# Window size
winx = 250
winy = 250

segment_size = 10
direction = [-1,0]

def add_segment(segs):
  final_item_x = segs[-1][0]
  final_item_y = segs[-1][1]

  segs.append([final_item_x,final_item_y])

  return segs

def update_segment_pos(segs):
  global direction

  prevs = [[x,y] for x,y in segs]

  if direction[0] == -1:
    segments[0][0] -= segment_size
  elif direction[0] == 1:
    segments[0][0] += segment_size
  elif direction[1] == -1:
    segments[0][1] -= segment_size
  elif direction[1] == 1:
    segments[0][1] += segment_size

  for s in range(1,len(segs)):
    segs[s][0] = prevs[s-1][0]
    segs[s][1] = prevs[s-1][1]

  return segs

def change_direction(dir):
  global direction

  if direction == [-1,0] and dir != [1,0]:
    direction = dir
  elif direction == [1,0] and dir != [-1,0]:
    direction = dir
  elif direction == [0,1] and dir != [0,-1]:
    direction = dir
  elif direction == [0,-1] and dir != [0,1]:
    direction = dir

pygame.display.init()

screen = pygame.display.set_mode((winx,winy))

done = False

start_length = 1

segments = [[(winx//2)+(i*segment_size),(winy//2)] for i in range(start_length)]

foodX,foodY = [random.randrange(segment_size,(winx-segment_size)),random.randrange(segment_size,(winy-segment_size))]

update_interval = 0.5
game_pace = 0.05

# Main Game Loop
while not done:
  # Update section
  tailx = segments[-1][0]
  taily = segments[-1][1]

  segments = update_segment_pos(segments)
  
  # Body collision
  for s in range(2,len(segments)):
    if segments[0][0] == segments[s][0] and segments[0][1] == segments[s][1]:
      print("body_hit - dying now")
      done = True
  if segments[0][0] == tailx and segments[0][1] == taily:
    print("body_hit_tail - dying now")
    done = True

  # Wall collision
  if segments[0][0] >= (winx - segment_size) or\
    segments[0][0] <= (0) or\
	segments[0][1] >= (winy - segment_size) or\
	segments[0][1] <= (0):
    print("Hit Wall - dying now")
    done = True

  # Food collision
  if ((segments[0][0] - foodX)**2 + (segments[0][1] - foodY)**2)**0.5 <= segment_size:
    foodX,foodY = [random.randrange(segment_size,(winx-segment_size)),random.randrange(segment_size,(winy-segment_size))]
    segments = add_segment(segments)
    if update_interval > game_pace:
      update_interval -= game_pace
      update_interval = round(update_interval,2)

  events = pygame.event.get()

  # Input section
  # Use arrow keys to move the snake - press ESC or click the red 'X' to quit.
  for e in events:
    if e.type == pygame.QUIT:
     done = True
    elif e.type == pygame.KEYDOWN:
      if e.key == pygame.K_ESCAPE:
        done = True
      elif e.key == pygame.K_UP:
        change_direction([0,-1])
      elif e.key == pygame.K_DOWN:
        change_direction([0,1])
      elif e.key == pygame.K_LEFT:
        change_direction([-1,0])
      elif e.key == pygame.K_RIGHT:
        change_direction([1,0])

  # Draw section
  screen.fill((0,0,0))
  for s in segments:
    pygame.draw.rect(screen, (255,255,255), (s[0], s[1], segment_size, segment_size))
  pygame.draw.rect(screen, (255,0,0), (foodX, foodY, segment_size, segment_size))
  pygame.display.flip()

  time.sleep(update_interval)

print("Total Length:", len(segments))
pygame.display.quit()
