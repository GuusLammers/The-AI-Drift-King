import pygame as pg
import os
import random
import math

# window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750

# track image
TRACK = pg.transform.scale(pg.image.load(os.path.join('images', 'track.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))

# car images
CAR_BLUE = pg.transform.scale(pg.image.load(os.path.join('images', 'blue_car.png')), (24, 12))
CAR_RED = pg.transform.scale(pg.image.load(os.path.join('images', 'red_car.png')), (24, 12))
CAR_ORANGE = pg.transform.scale(pg.image.load(os.path.join('images', 'orange_car.png')), (24, 12))

# colours
WHITE = (255, 255, 255)

# car class
class Car:
	# global class variables
	CAR_ACCELERATION = 0.4
	CAR_NATURAL_DECELERATION = 0.05
	CAR_MAX_FORWARD_SPEED = 3
	CAR_MAX_BACKWARD_SPEED = 2
	CAR_TURNING_VELOCITY = 3
	CAR_IMAGES = [CAR_BLUE, CAR_RED, CAR_ORANGE]
	#CAR_MASS

	def __init__(self, x_pos, y_pos):
		self.position = (x_pos, y_pos)
		self.speed = 0
		self.angle = 0
		self.time_count = 0
		self.image = pg.transform.rotate(self.random_car(), self.angle)

	# randomizes the cars color	
	def random_car(self):
		return self.CAR_IMAGES[random.randint(0, len(self.CAR_IMAGES) - 1)]

	# calculates cars new speed	
	def speed_change(self, forward, backward):
		# if trying to move forward
		if forward:
			self.speed += self.CAR_ACCELERATION
			# check maximum forward velocity
			if self.speed > self.CAR_MAX_FORWARD_SPEED:
				self.speed = self.CAR_MAX_FORWARD_SPEED

		# if trying to move backward
		if backward:
			self.speed -= self.CAR_ACCELERATION	
			# check maximum backward velocity
			if -self.speed > self.CAR_MAX_BACKWARD_SPEED:
				self.speed = -self.CAR_MAX_BACKWARD_SPEED

		# if not trying to move forward or backward	
		if not forward and not backward:
			# if currently moving forward
			if self.speed > 0.3:
				self.speed -= self.CAR_NATURAL_DECELERATION
			# if currently moving backward	
			elif self.speed < -0.3:
				self.speed += self.CAR_NATURAL_DECELERATION
			# if speed is between 0.3 and -0.3 set speed to zero
			else:
				self.speed = 0 

	# calculates cars new angle if it turned at all			
	def angle_change(self, left, right):
		# if the cars speed is not zero
		if self. speed != 0:
			# if car is moving forward
			if self.speed > 0:
				# if turning left
				if left:
					self.angle -= self.CAR_TURNING_VELOCITY
				# if turning right
				if right:
					self.angle += self.CAR_TURNING_VELOCITY

			# if car is moving backward
			if self.speed < 0:
				# if turning right
				if left:
					self.angle += self.CAR_TURNING_VELOCITY
				# if turning left
				if right:
					self.angle -= self.CAR_TURNING_VELOCITY				
			
		# check if angle is greater than 360
		if self.angle > 360:
			self.angle -= 360	

		# check if angle is less than 0
		if self.angle < 0:
			self.angle += 360	

	# move car		
	def move(self, forward, backward, left, right):
		# update speed and angle
		self.speed_change(forward, backward)
		self.angle_change(left, right)

		# check if car is moving forward
		if self.speed > 0:
			# split up velocity vector into x and y components
			x_velocity = self.speed * math.cos(math.radians(self.angle)) 
			y_velocity = self.speed * math.sin(math.radians(self.angle))	
			# update position
			self.position = (self.position[0] + x_velocity, self.position[1] + y_velocity)


		# check if car is moving backward	
		if self.speed < 0:
			# split up velocity vector into x and y components
			x_velocity = -self.speed * math.cos(math.radians(self.angle - 180)) 
			y_velocity = -self.speed * math.sin(math.radians(self.angle - 180))	
			# update position
			self.position = (self.position[0] + x_velocity, self.position[1] + y_velocity)

	# draw car		
	def draw (self, window):
		# rotate image
		rotated_image = pg.transform.rotate(self.image, -self.angle)
		# draw car
		window.blit(rotated_image, self.position)


# update window
def update_window(window, car):
	# fill background
	window.fill((128, 128, 128))
	# draw track
	window.blit(TRACK, (0, 0))
	# draw car
	car.draw(window)
	# update window
	pg.display.update()

# main funtion
def main():
	# initialize window
	window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pg.display.set_caption('The AI Drift King')

	# initialize car
	car = Car(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

	# initialize clock
	clock = pg.time.Clock()

	# movement control variables
	up = False
	down = False
	left = False
	right = False

	# initialize loop control variables
	run = True

	# main loop
	while run:
		# clock speed
		clock.tick(60)

		# monitors users mouse and keyboard inputs
		for event in pg.event.get():
			# breaks main loop if exit is clicked
			if event.type == pg.QUIT:
				run = False	

			# if keyboard is clicked
			if event.type == pg.KEYDOWN:
				# if up is pressed
				if event.key == pg.K_UP:
					up = True
				# if down is pressed	
				if event.key == pg.K_DOWN:
					down = True
				# if left is pressed
				if event.key == pg.K_LEFT:
					left = True
				# if right is pressed	
				if event.key == pg.K_RIGHT:
					right = True	

			# if keyboard is not clicked
			if event.type == pg.KEYUP:
				# if up is not pressed
				if event.key == pg.K_UP:
					up = False
				# if down is not pressed	
				if event.key == pg.K_DOWN:
					down = False	
				# if left is not pressed
				if event.key == pg.K_LEFT:
					left = False
				# if right is not pressed	
				if event.key == pg.K_RIGHT:
					right = False		
							
		# move car			
		car.move(up, down, left, right)
					
		# update window			
		update_window(window, car)	

	# quit pygame application	
	pg.quit()			

# main function call
main()	
