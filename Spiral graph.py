import turtle, random
tina = turtle.Turtle()
tina.shape('turtle')
tina.speed(100)


for turn in range (0,10):
  angle = random.randint (90, 180)
  tina.color(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
  number_list = range(0, 100)

  distance = random.randint (10, 200) # distance is a variable, value we store, which can be changed
  for number in number_list: 
      tina.forward(distance) 
      tina.left(angle)
      tina.penup()
      tina.pendown()
    
