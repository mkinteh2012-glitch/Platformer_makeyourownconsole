extends Area2D

@onready var timer: Timer = $Timer

func _on_body_entered(body: Node2D) -> void: # if touching kill area
	pass # Replace with function body.
	print("you died") # you died in terminal
	Engine.time_scale = 0.5 #slows down the game to 50%
	body.get_node("CollisionShape2D").queue_free() #Finds collison shape in player and disables it
	timer.start() #Death cooldown
	


func _on_timer_timeout() -> void: #after timer's over
	pass # Replace with function body.
	Engine.time_scale = 1 # sets speed to normal
	get_tree().reload_current_scene() # reset the player
