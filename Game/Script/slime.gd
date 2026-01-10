extends Node2D

const SPEED = 60 #Enemy speed

var direction = 1 #Enemy direction

@onready var ray_cast_right: RayCast2D = $RayCastRight # making raycast variables
@onready var ray_cast_left: RayCast2D = $RayCastLeft

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
	position.x += direction * SPEED * delta
