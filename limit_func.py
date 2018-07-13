import re
import my_config


def check_the_email(email):
    pattern_all_email = r"[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}"
    pattern_minieye_email = re.compile(r"[a-zA-Z0-9_.-]{0,30}@minieye.cc")
    if my_config.pattern == 'all':
        pattern = pattern_all_email
    else:
        pattern = pattern_minieye_email
    if re.match(pattern, email):
        return True
    else:
        return False


def check_the_password(password):
    if len(password) < 4 or len(password) > 25:
        return False
    pattern1 = r"[0-9]{4,25}"
    if re.match(pattern1, password):
        return False
    return True