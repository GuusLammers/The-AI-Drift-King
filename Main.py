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
RED = (0, 0, 255)

# car class
class Car:
	# global class variables
	CAR_ACCELERATION = 0.4
	CAR_NATURAL_DECELERATION = 0.05
	CAR_MAX_FORWARD_SPEED = 4
	CAR_MAX_BACKWARD_SPEED = 2
	CAR_TURNING_VELOCITY = 3
	CAR_IMAGES = [CAR_BLUE, CAR_RED, CAR_ORANGE]
	
	def __init__(self, x_pos, y_pos):
		self.position = (x_pos, y_pos)
		self.speed = 0
		self.car_angle = 0
		self.speed_angle = self.car_angle
		self.time_count = 0
		self.image = pg.transform.rotate(self.random_car(), self.car_angle)
		self.dead = False

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

	# calculates cars new angle if it turned 		
	def car_angle_change(self, left, right):
		# if the cars speed is not zero
		if self.speed != 0:
			# if car is moving forward
			if self.speed > 0:
				# if turning left
				if left:
					self.car_angle -= self.CAR_TURNING_VELOCITY
				# if turning right
				if right:
					self.car_angle += self.CAR_TURNING_VELOCITY

			# if car is moving backward
			if self.speed < 0:
				# if turning right
				if left:
					self.car_angle += self.CAR_TURNING_VELOCITY
				# if turning left
				if right:
					self.car_angle -= self.CAR_TURNING_VELOCITY					

	# calculates cars new direction of travel (drift function)	
	def speed_angle_change(self):
		# if car is moving forward
		if self.speed > 0:
			# if speed angle is within a degree of car angle
			if abs(self.speed_angle - self.car_angle) <= 1:
				self.speed_angle = self.car_angle

			else:
				# calculate the percent of the maximum speed the car is traveling at
				percent_max_speed = self.speed / self.CAR_MAX_FORWARD_SPEED	
				# calculate change in speed angle
				speed_angle_change = abs(self.speed_angle - self.car_angle) - 0.9 * abs(self.speed_angle - self.car_angle) * percent_max_speed

				# if turning left
				if self.car_angle > self.speed_angle:
					# if the angle difference is greater than 40
					if abs(self.speed_angle - self.car_angle) > 40:
						self.speed_angle = self.car_angle - 40

					else:	
						self.speed_angle += speed_angle_change

				# if turning right	
				if self.car_angle < self.speed_angle:
					# if the angle difference is greater than 40
					if abs(self.speed_angle - self.car_angle) > 40:
						self.speed_angle = self.car_angle + 40

					else:	
						self.speed_angle -= speed_angle_change

	# move car		
	def move(self, forward, backward, left, right):
		# update speed and angle
		self.speed_change(forward, backward)
		self.car_angle_change(left, right)
		self.speed_angle_change()

		# check if car is moving forward
		if self.speed > 0:
			# split up velocity vector into x and y components
			x_velocity = self.speed * math.cos(math.radians(self.speed_angle)) 
			y_velocity = self.speed * math.sin(math.radians(self.speed_angle))	
			# update position
			self.position = (self.position[0] + x_velocity, self.position[1] + y_velocity)


		# check if car is moving backward	
		if self.speed < 0:
			# split up velocity vector into x and y components
			x_velocity = -self.speed * math.cos(math.radians(self.car_angle - 180)) 
			y_velocity = -self.speed * math.sin(math.radians(self.car_angle - 180))	
			# update position
			self.position = (self.position[0] + x_velocity, self.position[1] + y_velocity)

	# draw lines
	def draw_lines(self, window):
		# rotate image
		rotated_image = pg.transform.rotate(self.image, -self.car_angle)
		# determine center point of car
		new_rectangle = rotated_image.get_rect(center=self.image.get_rect(topleft=self.position).center)
		center = pg.Rect(new_rectangle.bottomleft[0], new_rectangle.bottomleft[1], new_rectangle[2], new_rectangle[3]).center

		# draw lines 		
		# parallel
		pg.draw.line(window, RED, center, (center[0] + 300 * math.cos(math.radians(self.car_angle)), center[1] + 300 * math.sin(math.radians(self.car_angle))))
		# perpendicular
		pg.draw.line(window, RED, center, (center[0] + 300 * math.cos(math.radians(self.car_angle - 90)), center[1] + 300 * math.sin(math.radians(self.car_angle - 90))))
		pg.draw.line(window, RED, center, (center[0] + 300 * math.cos(math.radians(self.car_angle + 90)), center[1] + 300 * math.sin(math.radians(self.car_angle + 90))))
		# 45 degrees
		pg.draw.line(window, RED, center, (center[0] + 300 * math.cos(math.radians(self.car_angle - 45)), center[1] + 300 * math.sin(math.radians(self.car_angle - 45))))
		pg.draw.line(window, RED, center, (center[0] + 300 * math.cos(math.radians(self.car_angle + 45)), center[1] + 300 * math.sin(math.radians(self.car_angle + 45))))

	# draw car		
	def draw (self, window):
		# rotate image
		rotated_image = pg.transform.rotate(self.image, -self.car_angle)
		# determine center point of car
		center = rotated_image.get_rect(center=self.image.get_rect(topleft=self.position).center)	
		# draw lines
		self.draw_lines(window)
		# draw car
		window.blit(rotated_image, center.bottomleft)

	# get mask of car
	def get_mask(self):
		return pg.mask.from_surface(self.image)	
	

class Track:

	def __init__(self):
		self.image = TRACK
		self.mask = pg.mask.from_surface(self.image)	

	# draw track
	def draw(self, window):
		window.blit(self.image, (0, 0))	

	# checks if car goes off track	
	def collide(self, car):
		# get car mask
		car_mask = car.get_mask()
		# calculate offset
		#print(self.image.get_rect().topleft)
		offset = (-round(car.position[0]), -round(car.position[1]) - 18)
		# check collision
		collide = car_mask.overlap(self.mask, offset)

		# return True if collision occured, False if not
		if collide:
			return True

		return False


# update window
def update_window(window, car, track):
	# fill background
	window.fill((128, 128, 128))
	# draw track
	track.draw(window)
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
	car = Car(525, 550)

	# initialize track
	track = Track()

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
			if event.type == pg.KEYDOWN and not car.dead:
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
			if event.type == pg.KEYUP and not car.dead:
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
							
		# check if car went off track and kill car if it did\
		"""
		if track.collide(car):
			car.dead = True	
			up = False	
			down = False
			left = False
			right = False
		"""	

		# move car			
		car.move(up, down, left, right)
					
		# update window			
		update_window(window, car, track)	

	# quit pygame application	
	pg.quit()			

# main function call
main()	
