mySprite = sprites.create(img("""
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . 2 . . . . . . . . .
        . . . 2 . . 2 . . . . . 2 . . .
        . . . 2 . 2 . . 2 2 2 2 . . . .
        . . . 2 2 2 2 2 . 2 . . . . . .
        . . . 2 . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        """),
    SpriteKind.player)
# Run it multiple times
for index in range(5):
    
    def start_animation_after_random_delay():
        delay = randint(1000, 3000)
        console.log_value("delay_ms", delay)
        # ✅ Logs to Data tab
        pause(delay)
        animation.run_movement_animation(mySprite,
            animation.animation_presets(animation.ease_down),
            2000,
            True)
    control.run_in_background(start_animation_after_random_delay)
    
