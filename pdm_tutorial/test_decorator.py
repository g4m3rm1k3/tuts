# A simple decorator taht prints before and after
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"BEFORE calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"AFTER calling {func.__name__}")
        return result
    return wrapper

# Using the decorator


@logger
def greet(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"


# Call it
result = greet("Michael")
print(f"Result: {result}")
