#Импорт модулей
import pygame
from pygame.locals import *
#Инициализация пайгейм
pygame.init()

#Глобальные переменные. Размеры окна, создание окна
s_w = 499
s_h = 499
FPS = 30
screen = pygame.display.set_mode([s_w, s_h])


# место клетки
def red_plate():
	surf1 = pygame.Surface((141, 141))
	surf1.set_alpha(70)
	surf1.fill((0, 0, 0))
	return surf1


# маленькая картинка в верхнем левом углу
def small_pic():
	surf = pygame.Surface((141, 141))
	surf.fill((255, 255, 255))
	if start%2==1:
		line1 = pygame.draw.rect(surf, (255, 0, 0), (66, 0, 8, 141), 0, 4, 4, 4, 4)
		line2 = pygame.draw.rect(surf, (255, 0, 0), (0, 66, 141, 8), 0, 4, 4, 4, 4)
		surf = pygame.transform.rotate(surf, 45)
	else:
		cir = pygame.draw.circle(surf, (0, 0, 0), (70, 70), 50, 8)
	surf = pygame.transform.scale(surf, (30, 30))
	return surf


# рисование крестика
def cross_pic():
	surf = pygame.Surface((141, 141), flags=pygame.SRCALPHA)
	surf.fill((255, 255, 255, 0))
	line1 = pygame.draw.rect(surf, (255, 0, 0), (66, 0, 8, 141), 0, 4, 4, 4, 4)
	line2 = pygame.draw.rect(surf, (255, 0, 0), (0, 66, 141, 8), 0, 4, 4, 4, 4)
	surf = pygame.transform.rotate(surf, 45)
	return surf


# рисование нолика
def circle_pic():
	surf = pygame.Surface((141, 141), flags=pygame.SRCALPHA)
	surf.fill((255, 255, 255, 0))
	cir = pygame.draw.circle(surf, (0, 0, 0), (70, 70), 50, 8)
	return surf


# создание класса клетки, на которую нужно нажимать
class Plate(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.rect = red_plate().get_rect()
		self.rect.left = pos[0]
		self.rect.top = pos[1]


	def update(self):
		global start
		if start%2==1:
			if self in clicked_sprites:
				screen.blit(circle_pic(), (self.rect.left, self.rect.top))
				self.kill()
		else:
			if self in clicked_sprites:
				screen.blit(cross_pic(), (self.rect.left-30, self.rect.top-30))
				self.kill()
				



# Функция создает игровое поле
def GameField():
	#Цвет фона/окна
	screen.fill((255, 255, 255))

	line = pygame.draw.rect(screen, (0, 0, 0), (171, 30, 8, 440), 0, 4, 4, 4, 4)
	line = pygame.draw.rect(screen, (0, 0, 0), (320, 30, 8, 440), 0, 4, 4, 4, 4)
	line = pygame.draw.rect(screen, (0, 0, 0), (30, 171, 444, 8), 0, 4, 4, 4, 4)
	line = pygame.draw.rect(screen, (0, 0, 0), (30, 320, 444, 8), 0, 4, 4, 4, 4)


# игровое поле
GameField()


# позиции, куда можно поставить крестик или нолик
plates_pos = ((30, 30), (179, 30), (328, 30), (30, 179), (179, 179), (328, 179), (30, 328), (179, 328), (328, 328))

# позиции, где уже стоят крестик и нолик
cross_pos = []
circle_pos = []

# условия победы
win_cond = [
	plates_pos[:3],
	plates_pos[3:6],
	plates_pos[6:],
	plates_pos[::3],
	plates_pos[1::3],
	plates_pos[2::3],
	(plates_pos[0], plates_pos[4], plates_pos[8]),
	(plates_pos[2], plates_pos[4], plates_pos[6])
]


# название окна, время, группа спрайтов клеточек
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()
plates = pygame.sprite.Group()


# добавление спрайтов в группу
for n in plates_pos:
	pl = Plate((n[0], n[1]))
	plates.add(pl)


# разные переменные
clicked_sprites = [0]
start = 1
won = 0
screen.blit(small_pic(), (10, 10))


#Главный цикл
running = True
while running:
	clock.tick(FPS)
	#Цикл красного крестика
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# нажатие на клеточку
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			clicked_sprites = [s for s in plates if s.rect.collidepoint(pos)]
			if clicked_sprites:
				start+=1
				screen.blit(small_pic(), (10, 10))
				if start%2==0:
					cross_pos.append((clicked_sprites[0].rect.left, clicked_sprites[0].rect.top))
				else:
					circle_pos.append((clicked_sprites[0].rect.left, clicked_sprites[0].rect.top))

	# проверка на 3 в ряд
	for n in win_cond:
		if n[0] in cross_pos and n[1] in cross_pos and n[2] in cross_pos:
			#print("Cross won")
			won = 1
		elif n[0] in circle_pos and n[1] in circle_pos and n[2] in circle_pos:
			#print("Circle won") 
			won = 2
		elif len(circle_pos)+len(cross_pos)==9:
			#print("Draw")
			won = 3


	# обновление экрана
	plates.update()
	pygame.display.flip()


	# финальный экран
	if won != 0:
		plates.empty()
		surf = pygame.Surface((s_w, s_h))
		surf.set_alpha(10)
		surf.fill((255, 178, 102))
		screen.blit(surf, (0, 0))
		font = pygame.font.Font('freesansbold.ttf', 50)
		if won == 1:
			text = font.render('Cross won', True, (0, 0, 0))
		elif won == 2:
			text = font.render('Circle won', True, (0, 0, 0))
		elif won == 3:
			text = font.render('Draw', True, (0, 0, 0))
		screen.blit(text, (s_w/2-125, s_h/2-25))

	
#Выход
pygame.quit()