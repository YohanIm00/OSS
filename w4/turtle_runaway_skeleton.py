# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle
import random
import math

class Bullet(turtle.RawTurtle):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.shapesize(0.2, 0.2, 0.2)
        self.shape('circle')
        self.color('yellow')
        self.penup()
        self.speed(0)  # Fastest speed
        self.hideturtle()  # Start hidden

    def fire(self, start_pos, angle, runner_pos):
        self.setposition(start_pos)
        self.setheading(angle)
        self.showturtle()  # Make the bullet visible
        self.move(runner_pos)  # Pass runner_pos to move

    def move(self, runner_pos):
        self.forward(10)  # Move the bullet forward

        # Check if bullet goes off-screen and reposition to a random location
        if abs(self.xcor()) > 210 or abs(self.ycor()) > 160:
            self.hideturtle()  # Hide bullet before repositioning
            self.respawn(runner_pos)  # Pass runner_pos to respawn method

    def calculate_angle_to_runner(self, runner_pos):
        bullet_pos = self.position()
        dx = runner_pos[0] - bullet_pos[0]
        dy = runner_pos[1] - bullet_pos[1]
        return math.degrees(math.atan2(dy, dx))

    def respawn(self, runner_pos):
        # Randomly choose a side to spawn the bullet
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            start_pos = (random.randint(-200, 200), 150)  # Spawn at the top edge
            angle = self.calculate_angle_to_runner(runner_pos)
        elif side == "bottom":
            start_pos = (random.randint(-200, 200), -150)  # Spawn at the bottom edge
            angle = self.calculate_angle_to_runner(runner_pos)
        elif side == "left":
            start_pos = (-200, random.randint(-150, 150))  # Spawn at the left edge
            angle = self.calculate_angle_to_runner(runner_pos)
        else:  # side == "right"
            start_pos = (200, random.randint(-150, 150))  # Spawn at the right edge
            angle = self.calculate_angle_to_runner(runner_pos)

        # Fire the bullet with the updated runner position
        self.fire(start_pos, angle, runner_pos)


class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner 
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.bullets = []  # List to hold bullets

        # Initialize 'runner' and 'chaser'
        self.runner.setheading(90)
        self.runner.color('white')
        self.runner.penup()

        self.chaser.shapesize(0.2, 0.2, 0.2)
        self.chaser.shape('circle')
        self.chaser.color('yellow')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.penup()

        self.create_bullets()  # Create bullets in advance

    def create_bullets(self):
        runner_pos = self.runner.position()  # Get the runner's current position

        for _ in range(50):  # Create 50 bullets
            bullet = Bullet(self.canvas)

            # Randomly choose a side to spawn the bullet
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                start_pos = (random.randint(-200, 200), 150)  # Spawn at the top edge
            elif side == "bottom":
                start_pos = (random.randint(-200, 200), -150)  # Spawn at the bottom edge
            elif side == "left":
                start_pos = (-200, random.randint(-150, 150))  # Spawn at the left edge
            else:  # side == "right"
                start_pos = (200, random.randint(-150, 150))  # Spawn at the right edge

            # Calculate angle towards runner's position
            x_bullet, y_bullet = start_pos
            x_runner, y_runner = runner_pos
            angle = math.degrees(math.atan2(y_runner - y_bullet, x_runner - x_bullet))

            bullet.fire(start_pos, angle, runner_pos)  # Fire the bullet towards the runner
            self.bullets.append(bullet)  # Add to bullets list

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=200, ai_timer_msec=10):
        self.runner.setpos(0, 0)
        self.chaser.setpos((+init_dist / 2, 0))

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # Update bullets
        runner_pos = self.runner.position()  # Get the runner's current position
        for bullet in self.bullets:
            bullet.move(runner_pos)  # Pass the runner's position to bullet move

        is_catched = self.is_catched()
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Is catched? {is_catched}')

        # Note: The following line should be the last of this function to keep the game playing
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