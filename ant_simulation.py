
## Ant Colony Simulation 
## Summer 2020 


# Import Useful Libraries
import random 
import pygame
import sys



# The code
class Ant: 
    def __init__(self, x ,y): 
        self.x = x
        self.y = y 
        self.hasFood = False
    
    
    def move(self, environment, food):
        #up down left right
        neighbors = [ 
                     (-1, 0),
                     (1,  0),
                     (0, -1),
                     (0,  1),
                     (-1,-1),
                     (-1, 1),
                     (1, -1),
                     (1,  1)
                     ]
        # need to calculate the pheromones for the different neighboars
        neighboring_pheromones = [environment.pheromones[(self.y + neighbor[0]) % environment.height][(self.x + neighbor[1]) % environment.width] for neighbor in neighbors]
        total_pheromones = sum(neighboring_pheromones)
        
        #give a probabilistc direction using normalized pheromone levels
        if total_pheromones > 0:
            probabilities = [pheromone / total_pheromones for pheromone in neighboring_pheromones]
        else:
            # If no pheromones are present, distribute probabilities equally
            probabilities = [1 / len(neighbors)] * len(neighbors)
        
        direction = random.choices(neighbors, weights = probabilities)[0]
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        
        self.x, self.y = new_x % environment.width , new_y % environment.height
         
    # getting food
    def get_food(self, food):
        if (self.x-food.x)**2 +(self.y-food.y)**2 <=5 and not self.has_food and food.amount>0:
            self.has_food  = True
            food.amount -= 1 
            if food.amount%10==0: print(food.amount)
    
    
    # Leaving pheromones on the envrionement 
    def pheromone_trail(self, pheromones):
        if self.hasFood: 
            pheromones[self.y][self.x] += 0.25

    
    
class Environment: 
    def __init__(self, height, width): 
        self.height = height
        self.width = width 
        
        self.pheromones = [[0 for _ in range(width)] for _ in range(height)]
    
    def pheromone_decay(self, pheromones):
        decay_rate = 0.995
        for y in range(len(pheromones)):
            for x in range(len(pheromones[y])):
                pheromones[y][x] *= decay_rate
    
    
class Food:
    def __init__(self, x, y, amount):
        self.x = x
        self.y = y
        self.amount = amount

def setup():
    environment = Environment(400, 400)
    ants = [Ant(random.randint(0,environment.height), random.randint(0,environment.width)) for _ in range(50)]
    food = Food(100, 200, 1000)
    

    pygame.init()
    screen = pygame.display.set_mode((environment.width, environment.height))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulation Steps
        for ant in ants:
            ant.move(environment, food)
            ant.get_food(food)
            ant.pheromone_trail(environment.pheromones)
        
        if food.amount ==0: running = False

        environment.pheromone_decay(environment.pheromones)

        # Visualization (Example)
        screen.fill((0, 0, 0))  # Clear the screen
        for ant in ants:
            pygame.draw.circle(screen, (255, 0, 0), (ant.x, ant.y), 2)  # Draw ants as red circles
        pygame.draw.circle(screen, (0, 255, 0), (food.x, food.y), food.amount/100)  # Draw food as green circle

        # Update Display and Control Framerate
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    # sys.exit()


if __name__ == "__main__":
    setup()


# if __name__=="__main__":
#     main()