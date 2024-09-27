# Outline
**Turtle Runaway**(tentative title) is kind of bullet hell game. It is kind of endless game and player should survive fromn bunch of bullets as long as they possible. there are two kinds of bullets; one is just moving straight forward, beside another is follow player as an induction bullet. Players need to enhance their quickness for getting better score by surviving from tons of bullet hell.

# Features
* Such an impressive project with using Python turtle library; *I hope so*
* Audio manager: appropriate SFXs and BGMs are really significant for enhancing better gaming experience.
* Leaderboard system: it contains player's record of time and the number of bullets.

# Synopsis
You are an astronaut who belonged to "Moon Starers", where people focus on researching this universe to reveal what we still don't know. For developing human being's scientific acknowledgement, you had decided to take a rocket to explore beyond our current boundary about cosmos. But one day, you suddenly got terrible harzard; tons of asteroid are rapidly comming to your rocket...
Can you, survive from there? 

# Goal
* **Ending** is derived when the player collided by the bullet
* So, **Player's purpose** to play this game is getting better score.
* Pursue them to enlarge their scores of **total surviving time**.

# Rule
Game level is a closed environment where player can move 4 direction and bullets are continuously bounced at the edge of screen. The number of bullets are getting increased as long as the time goes on. if the distance between player and random bullet is shorter than predefined distance, game will regard it as colliding and the game will be finished.

# 3Cs
## Camera
Main camera of this game is offering top-down view to player. It doesn't move anywhere even if the player is moving to the edge of the game.

## Character
### Description
main character is astronaut, and that's why player control a rocket. This game don't have any other transport of some character at this version.
### States
* Wait: if player don't tap any button that can control, rocket just wait there.
* Move: as long as player push some button for moving, it slightly move in that way. 

## Controler
* Arrows: move rocket based on its direction.
* Mouse click: buttons in several menus are available to click

# Game Menu
## Main
Player can access this after starting game.
* Start: load the game.
* Scoreboard: display recently recorded top 10 results.
* Exit: close the game.
## Game Over
Player meet this after the game is done.
* Namebox: player can type arbitrary name before they restore their score.

## Scoreboard
Player can see their records or reset their records.