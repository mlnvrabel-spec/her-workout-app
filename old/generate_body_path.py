
def generate_body_path():
    # Points for the left side of the body (x < 50)
    # Start from top of head center
    points_left = [
        (50, 5),    # Top Head
        (42, 8),    # Head Left Top
        (40, 18),   # Ear area
        (42, 26),   # Jaw/Neck join
        (35, 28),   # Traps slope
        (20, 30),   # Shoulder top
        (10, 38),   # Deltoid outer
        (8, 55),    # Arm outer (tricep bulge)
        (8, 75),    # Forearm
        (6, 85),    # Wrist
        (4, 90),    # Hand outer
        (8, 95),    # Fingers
        (12, 90),   # Hand inner
        (14, 85),   # Wrist inner
        (16, 60),   # Arm inner
        (20, 50),   # Armpit
        (25, 60),   # Lat spread/Torso
        (28, 80),   # Waist
        (26, 90),   # Hip outer
        (24, 110),  # Thigh outer
        (24, 140),  # Knee outer
        (26, 160),  # Calf outer
        (28, 172),  # Ankle outer
        (26, 178),  # Foot outer
        (35, 178),  # Toe
        (40, 175),  # Foot inner
        (40, 160),  # Calf inner
        (42, 140),  # Knee inner
        (44, 110),  # Thigh inner
        (48, 95),   # Crotch
    ]
    
    # Mirror for right side
    points_right = []
    for x, y in reversed(points_left):
        if x == 50 and y == 5: continue # Don't duplicate start point if we loop back
        points_right.append((100 - x, y))
        
    all_points = points_left + points_right
    
    # Construct path string
    # Using simple Line To (L) for now, can perform slight smoothing if needed but L might be stylistically fine or we can use Q for curves.
    # Let's create a Catmull-Rom spline or just Q curves manually? 
    # For simplicity and "mannequin" look, rounded simple points are good.
    
    d = "M 50 5"
    
    # Helper to smooth?
    # Simple strategy: just connect points.
    for x, y in all_points[1:]:
        d += f" L {x} {y}"
    
    d += " Z"
    return d

print(generate_body_path())
