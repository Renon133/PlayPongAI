import pygame
import pandas as pd

pygame.init()
#Variables
Width = 1200
Height = 800
Border = 20
VELOCITY = 15
FrameRate = 30

#Colors
fgColor = pygame.Color("black")
bgColor = pygame.Color("white")
YELLOW = pygame.Color("yellow")

screen = pygame.display.set_mode((Width,Height))
done = False

#Define my classes
class Ball:
    radius = 10
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        
    def show(self, colour):
        global screen
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def update(self, colour, paddle):
        
        newx = self.x + self.vx
        newy = self.y + self.vy
        paddle_y = paddle.y - paddle.HEIGHT//2
        paddle_x = Width - paddle.WIDTH
        
        if newx < Border+self.radius:
            self.vx = -self.vx
        elif newy > Height-Border-self.radius or newy < Border+Ball.radius:
            self.vy = -self.vy
        elif newx > paddle_x and newy in range(paddle_y, paddle_y+paddle.HEIGHT):
            self.vx = -self.vx
        else:
            self.show(bgColor)
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            self.show(colour)
        
class Paddle:
    WIDTH = 20
    HEIGHT = 100
    
    def __init__(self, y):
        self.y = y
    
    def show(self, colour):
        pygame.draw.rect(screen, colour, pygame.Rect(Width-self.WIDTH,self.y-self.HEIGHT//2, self.WIDTH, self.HEIGHT))
    
    def update(self, newY):
        # newY = pygame.mouse.get_pos()[1]
        if newY-self.HEIGHT//2 > Border and newY+self.HEIGHT//2 < Height-Border:
            self.show(bgColor)
            self.y = newY
            self.show(fgColor)
                                              
#Create objects
ball = Ball(Width-Ball.radius-Border, Height//2, -VELOCITY, -VELOCITY)
paddle = Paddle(Height//2)


#Draw the main Scenario
screen.fill(bgColor)
pygame.draw.rect(screen, fgColor, pygame.Rect(0,0,Width, Border))
pygame.draw.rect(screen, fgColor, pygame.Rect(0,0,Border, Height))
pygame.draw.rect(screen, fgColor, pygame.Rect(0,Height-Border,Width, Border))
ball.show(YELLOW)
paddle.show(bgColor)

# To control Frame rate
clock = pygame.time.Clock()

# Creating Data Samples
# sample = open("game.csv","w")
# print("x,y,vx,vy,Paddle.y", file=sample)
pong = pd.read_csv("game.csv")
pong = pong.drop_duplicates()
X = pong.drop(columns="Paddle.y")
Y = pong['Paddle.y']
#Dataframe to store position of the ball and its velocity
df = pd.DataFrame(columns=['x','y','vx','vy'])

#Automation of Game using ML
from sklearn.neighbors import KNeighborsRegressor 
clf = KNeighborsRegressor(n_neighbors = 3)
clf.fit(X,Y)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    clock.tick(FrameRate)
    #Update the ball and paddle position 
    ball.update(YELLOW, paddle)
    #Predicting Position of Paddle
    forPredict = df.append({'x':ball.x, 'y':ball.y, 'vx':ball.vx, 'vy':ball.vy}, ignore_index=True)
    prediction = clf.predict(forPredict)
    paddle.update(int(prediction[-1]))
    # paddle.update()
    pygame.display.flip()
    # print("{},{},{},{},{}".format(ball.x, ball.y, ball.vx, ball.vy, paddle.y), file = sample)
    

pygame.quit()