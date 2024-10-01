# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        # self.runner.shape()
        self.runner.color('#F3F3F3')
        self.runner.penup()

        self.chaser.shapesize(0.2, 0.2, 0.2)
        self.chaser.shape('circle')
        self.chaser.color('yellow')
        self.chaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        # self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=200, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(90)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
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
        # How about revising this part, too?
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
