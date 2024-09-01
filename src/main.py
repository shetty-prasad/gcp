def greeting(name):
    msg = f"Hello {name}"
    return msg


def add_numbers(a: int, b: int) -> int:
    c = a+b
    return c


def main_func(request):
    print(greeting("Rahul"))
    print(add_numbers(5, 10))