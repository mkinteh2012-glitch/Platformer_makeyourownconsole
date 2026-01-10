extends Area2D

@onready var timer: Timer = $Timer

func _on_body_entered(body: Node2D) -> void:
	pass # Replace with function body.
	print("you died")
	timer.start()
	


func _on_timer_timeout() -> void:
	pass # Replace with function body.
	get_tree().reload_current_scene()
