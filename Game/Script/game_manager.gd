extends Node
#making the score variable
var score = 0

@onready var score_label: Label = $ScoreLabel

func add_point():#makes a fuction
	score += 1 # increase score by 1 
	score_label.text = "You collected " + str(score) + " coins! "
