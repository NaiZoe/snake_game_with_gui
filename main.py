from tkinter import *
import random

# Game constants
GAME_WIDTH = 700  # Width of the game window
GAME_HEIGHT = 700  # Height of the game window
GAME_SPEED = 200  # Initial speed in milliseconds
GRID_SIZE = 50  # Size of each grid cell
BODY_PARTS = 3  # Initial snake body parts
SNAKE_COLOR = "#C2FFC7"  # Color of the snake
FOOD_COLOR = "#FF2929"  # Color of the food
BACKGROUND_COLOR = "#000000"  # Background color of the canvas

# Snake class to manage the snake's behavior
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS  # Initial number of body parts
        self.coordinates = []  # List to store the coordinates of the snake
        self.squares = []  # List to store the square objects representing the snake

        # Initialize the snake's body at the starting position
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])  # Each part starts at (0, 0)

        # Create the snake's body parts on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, 
                                             fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Food class to manage food placement
class Food:
    def __init__(self):
        # Generate random coordinates for the food
        x = random.randint(0, int(GAME_WIDTH / GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, int(GAME_HEIGHT / GRID_SIZE) - 1) * GRID_SIZE

        self.coordinates = [x, y]  # Store the coordinates of the food

        # Create the food on the canvas
        canvas.create_oval(x, y, x + GRID_SIZE, y + GRID_SIZE, 
                           fill=FOOD_COLOR, tag="snake_food")

# Function to start or restart the game
def start_game():
    global snake, food, score, direction, level, GAME_SPEED, play_again_button

    # Reset game state
    score = 0  # Reset score to 0
    level = 0  # Reset level to 0
    GAME_SPEED = 200  # Reset the speed
    direction = "down"  # Reset the initial direction
    label.config(text="Score: {}".format(score))  # Update score label
    level_label.config(text="Level: {}".format(level))  # Update level label

    # Clear the canvas and initialize a new snake and food
    canvas.delete("all")
    snake = Snake()
    food = Food()

    # Hide the start button and play again button if they exist
    start_button.pack_forget()
    if play_again_button:
        play_again_button.place_forget()
        play_again_button = None

    # Start the game loop
    next_turn(snake, food)

# Function to handle the game loop
def next_turn(snake, food):
    global direction, GAME_SPEED, level

    # Get the current position of the snake's head
    x, y = snake.coordinates[0]

    # Update the position of the snake's head based on the direction
    if direction == "up":
        y -= GRID_SIZE
    elif direction == "down":
        y += GRID_SIZE
    elif direction == "left":
        x -= GRID_SIZE
    elif direction == "right":
        x += GRID_SIZE

    # Add the new head position to the snake's coordinates
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, 
                                     fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if the snake eats the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1  # Increase the score
        label.config(text="Score: {}".format(score))  # Update score label
        canvas.delete("snake_food")  # Remove the old food
        food = Food()  # Spawn new food

        # Update the level every 5 points
        new_level = min(score // 5, 5)  # Cap level at 5
        if new_level > level:
            level = new_level
            level_label.config(text="Level: {}".format(level))  # Update level label
            GAME_SPEED = max(75, 200 - (level * 30))  # Increase speed
            display_level_up_message(level)  # Display level-up message
    else:
        # Remove the last part of the snake (tail) if no food is eaten
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake):
        game_over()  # End the game if a collision occurs
    else:
        # Continue the game loop
        window.after(GAME_SPEED, next_turn, snake, food)

# Function to display a level-up message
def display_level_up_message(level):
    level_up_text = canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("Arial", 30),
        text=f"Level {level}!",
        fill="yellow",
        tag="LEVEL_UP_MESSAGE"
    )
    # Remove the message after 1 second
    window.after(1000, lambda: canvas.delete(level_up_text))

# Function to change the direction of the snake
def change_direction(new_direction):
    global direction

    # Ensure the snake cannot move in the opposite direction
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

# Function to check for collisions
def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Check if the snake collides with the walls
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Check if the snake collides with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

# Function to handle game over
def game_over():
    global play_again_button, highest_score

    # Update the highest score if the current score is higher
    if score > highest_score:
        highest_score = score

    # Display "Game Over" message
    canvas.delete("all")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,
                       font=("Arial", 70), text="GAME OVER",
                       fill="red", tag="GAME_OVER")

    # Display the highest score
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 20,
                       font=("Arial", 30), text=f"Highest Score: {highest_score}",
                       fill="white", tag="HIGHEST_SCORE")

    # Show "Play Again" button
    play_again_button = Button(window, text="Play Again", font=("Arial", 24), command=start_game)
    play_again_button.pack()

# Main Window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Initialize variables
score = 0  # Current score
direction = "down"  # Initial direction
level = 0  # Initial level
highest_score = 0  # Highest score so far
GAME_SPEED = 200  # Initial speed
play_again_button = None  # Button to restart the game

# UI Elements
label = Label(window, text="Score: {}".format(score), font=("Arial", 20))
label.pack()

level_label = Label(window, text="Level: {}".format(level), font=("Arial", 20))
level_label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

start_button = Button(window, text="Start Game", font=("Arial", 24), command=start_game)
start_button.pack()

# Update the window to calculate dimensions
window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.attributes("-topmost", True)
window.focus_force()

# Key Bindings for movement
window.bind('<Left>', lambda event: change_direction("left"))
window.bind('<Right>', lambda event: change_direction("right"))
window.bind('<Up>', lambda event: change_direction("up"))
window.bind('<Down>', lambda event: change_direction("down"))
window.bind('<w>', lambda event: change_direction("up"))
window.bind('<a>', lambda event: change_direction("left"))
window.bind('<s>', lambda event: change_direction("down"))
window.bind('<d>', lambda event: change_direction("right"))

# Start the Tkinter event loop
window.mainloop()
