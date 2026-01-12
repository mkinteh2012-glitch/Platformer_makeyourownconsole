extends Area2D

func _on_body_entered(body):
	# Check if the thing that touched the flag is the Player
	if body.name == "Player":
		# Save this flag's position to our Global memory
		Global.checkpoint_pos = global_position
		
		# Make the flag disappear (as you requested)
		$AnimatedSprite2D.visible = false
		
		# Disable collision so it doesn't trigger again
		$CollisionShape2D.set_deferred("disabled", true)
		print("Checkpoint Saved!")
