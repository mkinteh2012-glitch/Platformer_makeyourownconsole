extends Node2D

const SPEED = 60 #Enemy speed

var direction = 1 #Enemy direction

@onready var ray_cast_right: RayCast2D = $RayCastRight # making raycast variables
@onready var ray_cast_left: RayCast2D = $RayCastLeft
@onready var animated_sprite:AnimatedSprite2D = $AnimatedSprite2D #animated sprite node

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
	if ray_cast_right.is_colliding(): # if the raycast right touches a wall
			direction = -1 #turn around
			animated_sprite.flip_h = true #flips the enemy
	if ray_cast_left.is_colliding():# check raycast right touches a walll
			direction = 1 #turn around
			animated_sprite.flip_h = false
	position.x += direction * SPEED * delta
