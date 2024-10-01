# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random

class Bullet(turtle.RawTurtle):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.shapesize(0.2, 0.2, 0.2)
        self.shape('circle')
        self.color('yellow')
        self.penup()
        self.speed(0)  # Fastest speed
        self.hideturtle()  # Start hidden

    def fire(self, start_pos, angle):
        self.setposition(start_pos)
        self.setheading(angle)
        self.showturtle()  # Make the bullet visible
        self.move()

    def move(self):
        self.forward(10)  # Move the bullet forward
        
        # Check if bullet goes off-screen and reposition to a random location
        # Check if bullet goes off-screen and reposition
        if self.xcor() > 210:  # Right edge
            self.setx(-200)  # Reappear on the left edge
            self.sety(random.randint(-150, 150))  # Random y position within bounds
        elif self.xcor() < -210:  # Left edge
            self.setx(-200)  # Reappear on the right edge
            self.sety(random.randint(-150, 150))  # Random y position within bounds
        elif self.ycor() > 160:  # Top edge
            self.sety(-150)  # Reappear at the bottom edge
            self.setx(random.randint(-200, 200))  # Random x position within bounds
        elif self.ycor() < -160:  # Bottom edge
            self.sety(150)  # Reappear at the top edge
            self.setx(random.randint(-200, 200))  # Random x position within bounds

        # Keep moving the bullet
        # self.screen.ontimer(self.move, 100)  # Adjust the timer as needed

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner 
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.bullets = []  # List to hold bullets

        # Initialize 'runner' and 'chaser'
        self.runner.color('white')
        self.runner.penup()

        self.chaser.shapesize(0.2, 0.2, 0.2)
        self.chaser.shape('circle')
        self.chaser.color('yellow')
        self.chaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.penup()

        self.create_bullets()  # Create bullets in advance

    def create_bullets(self):
        for _ in range(50):  # Create 50 bullets
            bullet = Bullet(self.canvas)

            # Randomly choose a side to spawn the bullet
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                start_pos = (random.randint(-200, 200), 150)  # Spawn at the top edge
                angle = 270  # Move downwards
            elif side == "bottom":
                start_pos = (random.randint(-200, 200), -150)  # Spawn at the bottom edge
                angle = 90  # Move upwards
            elif side == "left":
                start_pos = (-200, random.randint(-150, 150))  # Spawn at the left edge
                angle = 0  # Move right
            else:  # side == "right"
                start_pos = (200, random.randint(-150, 150))  # Spawn at the right edge
                angle = 180  # Move left

            bullet.fire(start_pos, angle)  # Fire the bullet
            self.bullets.append(bullet)  # Add to bullets list

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=200, ai_timer_msec=10):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(90)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # Update bullets
        for bullet in self.bullets:
            bullet.move()

        is_catched = self.is_catched()
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Is catched? {is_catched}')

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, screen, step_move=5):
        super().__init__(screen)
        self.screen = screen
        self.step_move = step_move
        self.keys = set()

        # Bind key press and release events to track keys
        screen.onkeypress(lambda: self.key_press('Up'), "Up")
        screen.onkeyrelease(lambda: self.key_release('Up'), "Up")
        screen.onkeypress(lambda: self.key_press('Down'), "Down")
        screen.onkeyrelease(lambda: self.key_release('Down'), "Down")
        screen.onkeypress(lambda: self.key_press('Left'), "Left")
        screen.onkeyrelease(lambda: self.key_release('Left'), "Left")
        screen.onkeypress(lambda: self.key_press('Right'), "Right")
        screen.onkeyrelease(lambda: self.key_release('Right'), "Right")
        
        screen.listen()
        self.move()
        
    def key_press(self, key):
        self.keys.add(key)

    def key_release(self, key):
        self.keys.discard(key)

    def move(self):
        # Get current position
        x, y = self.xcor(), self.ycor()
        diagonal_step = self.step_move * 0.7071  # Moving diagonally; multiplying by sin(45°) for smooth diagonal movement

        # Movement combinations for 8 directions
        if 'Up' in self.keys and 'Left' in self.keys:
            x -= self.step_move
            y += self.step_move
        elif 'Up' in self.keys and 'Right' in self.keys:
            x += self.step_move
            y += self.step_move
        elif 'Down' in self.keys and 'Left' in self.keys:
            x -= self.step_move
            y -= self.step_move
        elif 'Down' in self.keys and 'Right' in self.keys:
            x += self.step_move
            y -= self.step_move
        elif 'Up' in self.keys:
            y += self.step_move
        elif 'Down' in self.keys:
            y -= self.step_move
        elif 'Left' in self.keys:
            x -= self.step_move
        elif 'Right' in self.keys:
            x += self.step_move

        # Update turtle's position
        self.setposition(x, y)

        # Keep repeating the move function
        self.screen.ontimer(self.move, 15)

    def run_ai(self, opp_pos, opp_heading):
        pass


class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    root.title("Turtle Runaway")
    canvas = tk.Canvas(root, width=400, height=300)
    canvas.pack()
    mainScreen = turtle.TurtleScreen(canvas)
    mainScreen.bgcolor('black')

    runner = ManualMover(mainScreen)
    chaser = RandomMover(mainScreen)

    game = RunawayGame(mainScreen, runner, chaser)
    game.start()
    mainScreen.mainloop()
