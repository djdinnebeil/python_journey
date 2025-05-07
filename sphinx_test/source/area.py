def calculate_area(radius):
    """
    Calculates the area of a circle given its radius.

    Parameters:
        radius (float): The radius of the circle. Must be non-negative.

    Returns:
        float: The area of the circle.

    Example:
        >>> calculate_area(2)
        12.56636
    """
    pi = 3.14159
    return pi * radius * radius
