def parse_duration(duration: int):
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    duration = []
    if days > 1:
        duration.append(f"{days} days")
    elif days == 1:
        duration.append(f"{days} day")
    if hours > 1:
        duration.append(f"{hours} hours")
    elif hours == 1:
        duration.append(f"{hours} hour")
    if minutes > 1:
        duration.append(f"{minutes} minutes")
    elif minutes == 1:
        duration.append(f"{minutes} minute")
    if seconds > 1:
        duration.append(f"{seconds} seconds")
    elif seconds == 1:
        duration.append(f"{seconds} second")

    return ", ".join(duration)
