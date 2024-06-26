import pygame 
import random
import pygame.freetype
import pygame as pg
import sys


pygame.init()
def get_car_image(filename, size, angle):
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, size)
    image = pygame.transform.rotate(image, angle)
    return image



#ГРУППЫ И ИЗОБРАЖЕНИЯ
screen = pygame.display.set_mode([800,400])
keep_going = True
clock = pygame.time.Clock()



#ДОРОГА
roadImg = pygame.image.load("assets/images/road.jpg")
roadImg = pygame.transform.scale(roadImg,(800,400))
roadGroup = pg.sprite.Group()



#ТРАФИК
trafficCarImg = []
trafficCar1 = get_car_image('assets/images/traffic_car1.png', (100, 70), 180)
trafficCar2 = get_car_image('assets/images/traffic_car2.png', (100, 70), 0)
trafficCar3 = get_car_image('assets/images/traffic_car3.png', (100, 70), 0)
trafficCarMent = get_car_image("assets/images/menti.png",(100,70),0)
trafficCarImg.extend((trafficCar1, trafficCar2, trafficCar3))
trafficCarsGroup = pg.sprite.Group()
specCars = pg.sprite.Group()



#МАШИНА
carImg = get_car_image("assets/images/mercedes.png",(100,70),180)



#ТАЙМЕРЫ И ЮЗЕРЕВЕНТЫ
spawnRoadTime = pygame.USEREVENT
pygame.time.set_timer(spawnRoadTime, 1000)
spawnTrafficTime = pygame.USEREVENT + 1
pygame.time.set_timer(spawnTrafficTime,1000)



#КЛАССЫ
class MyCar(pg.sprite.Sprite):
    def __init__(self, position, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.gameStatus = 'game'
        self.live = 5

    def border(self):
        if rect.y >= 3000:##1##3
            rect.y = 3000##1##3
        if self.rect.y <= -20:##1
            rect.y = 100##1##3
    
        if self.rect.x >= 80 and self.rect.y >= 18:##2
            self.rect.y = 10##2
            self.rect.x = 10##2
        if self.rect.x <= -5 and self.rect.y <= 18:##2
            self.rect.y = 130##4##5
            self.rect.x = 179##4##5

        if self.rect.x >= 700 and self.rect.y <= 118:##4##5
            self.rect.x = 700
        if self.rect.x <= 0 and self.rect.y >= 200:
            self.rect.x = 0
            
        
    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.y -= 100##6
        elif key[pygame.K_DOWN]:
            self.rect.y += 100##6
        elif key[pygame.K_LEFT]:
            self.rect.x = 10##7
        elif key[pygame.K_RIGHT]:
            self.rect.x = 10##7
        self.border()

    def crash(self,trafficCars):
        for car in trafficCars:
            if car.rect.colliderect(self.rect):
                car.kill()
                self.live = 1##7
        for car1 in specCars:
            if car1.rect.colliderect(self.rect):
                car1.kill()
                self.live = 0

        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
class Road(pg.sprite.Sprite):

    def __init__(self, image,position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
    def update(self):
        self.rect.x = 3##9

class Traffic(pg.sprite.Sprite):
    def __init__(self, image, position, speed):
        super().__init__()
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def remove(self):
        if self.rect.right > 95 or self.rect.left < -10:##8
            self.rect.right = 100##8
            self.kill()

    def update(self):
        self.rect.x = self.speed##8
        self.remove()



#СОЗДАЕМ ОБЪЕКТЫ И ДОБАВЛЯЕМ В ГРУППЫ
myCar = MyCar((102,102),carImg)##9
road = Road(roadImg,(810,210))##9
roadGroup.add(road)
road= Road(roadImg,(400,200))
roadGroup.add(road)

#СПАВНЕРЫ И ОТРИСОВКА
def spawnRoad():
    roadBg = Road(roadImg,(1400,200))
    roadGroup.add(roadBg)
def spawnTraffic(direct):
    if(direct >= 5):
        position = (0, random.randrange(250,400,100))
        speed1 = 3
        trafficCar = Traffic(random.choice(trafficCarImg), position, speed1)
    else:
        position = (810, random.randrange(50,200,100))
        speed2 = -5
        trafficCar = Traffic(pygame.transform.rotate(random.choice(trafficCarImg),-180), position, speed2)

    if(random.randint(1,5) <4 ):
                position = (810, random.randrange(50,200,100))
                speed2 = -15
                trafficCarMenti = Traffic(pygame.transform.rotate(trafficCarMent,-0), position, speed2) 
                specCars.add(trafficCarMenti)
    
    trafficCarsGroup.add(trafficCar)
def drawAll():
    roadGroup.update()
    roadGroup.update()##10
    roadGroup.draw(screen)
    trafficCarsGroup.update()
    trafficCarsGroup.draw(screen)
    specCars.update()
    specCars.draw(screen)
    myCar.draw(screen)



#ШРИФТЫ
score_font = pygame.font.SysFont("comicsansms", 25)##10
levelFont = pygame.font.SysFont("comicsansms",15)##10
font = pygame.freetype.Font(None, 30)
value = 10##10
Live = 50##10

def score():
    global value
    value +=1 
    textScore = score_font.render("Ваш счёт: " + str(value), True, (255,255,105))
    screen.blit(textScore,(0,0))
def Lives(LIVES):
    textLevel = levelFont.render("Жизней:" + str(LIVES),True,(0,255,255))
    screen.blit(textLevel,(650,0))




while keep_going: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False
        if event.type == spawnRoadTime:
            spawnRoad()
        if event.type == spawnTrafficTime:
            spawnTraffic(random.randint(0,10))
            
    if myCar.live != 0:
        myCar.move()
        drawAll()
        score()
        for spec in specCars:
            for car in trafficCarsGroup:
                if car.rect.colliderect(spec.rect):
                    car.kill()

        myCar.crash(trafficCarsGroup)
        Lives(myCar.live)

    else:
        font.render_to(screen,(300,200),"Ваш счет " + str(value),(255,255,255))    

    pygame.display.flip()
    clock.tick(60)