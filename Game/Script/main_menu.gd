extends Control

func _ready():
	# This ensures the menu is ready to listen for keys immediately
	set_process_input(true)

func _input(event):
	# "ui_accept" is the default for Space and Enter
	if event.is_action_pressed("ui_accept"):
		start_game()

func start_game():
	# 1. Reset the checkpoint so they don't spawn in the middle of the level
	Global.checkpoint_pos = null
	
	# 2. Change to your level (Make sure this path matches your FileSystem!)
	get_tree().change_scene_to_file("res://Scenes/platformer.tscn")

# If you still want to have a clickable button on the screen:
func _on_button_pressed():
	start_game()
