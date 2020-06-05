# int('a') Raises a ValueError, which you want to pass by silently.


for item in ['a', 1]:
    try:
        int(item)

    except KeyError:  # This isn't the right error. Move on.
        print('KeyError!')

    else:  # If the previous statements didn't go through
        print('A different error!')

    finally:  # Do this no matter what.
        print('Exception handled!')
