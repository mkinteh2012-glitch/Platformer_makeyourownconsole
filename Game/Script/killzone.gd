extends Area2D

@onready var timer: Timer = $Timer

func _on_body_entered(body: Node2D) -> void: # if touching kill area
	pass # Replace with function body.
	print("you died") # you died in terminal
	timer.start() #Death cooldown
	


func _on_timer_timeout() -> void: #after timer's over
	pass # Replace with function body.
	get_tree().reload_current_scene() # reset the player
