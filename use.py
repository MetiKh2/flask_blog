def allowed_extension(filename):
    ext=filename[-3:]
    extension={'jpg','png'}
    if not ext in extension:
        return False
    return True