def fit(source_width: float, source_height: float, target_width: float, target_height: float):
    """Scale source to fit with in target bounds while maintaing the aspect ratio."""
    target_ratio = target_height/target_width
    source_ratio = source_height/source_width
    if target_ratio > source_ratio:
        scale = target_width/source_width
    else:
        scale = target_height/source_height
    x = source_width * scale
    y = source_height * scale
    return x, y
