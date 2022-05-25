class A:

    def __init__(self, a=29, b=89):
        self.a = a
        self.b = b

    def print_arg(self):
        print(self.a)

    @property
    def sum_values(self):
        return self.a + self.b

    def __str__(self):
        if not (self.a + self.b) > 45:
            return 'str_method'
        else:
            return 'str_method'

    def __repr__(self):
        return 'this is the repre method'

    def __eq__(self, other):
        return isinstance(other, A) \
               and self.a == other.a \
               and self.b == other.b

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __len__(self):
        return int(self.b / 2)

    @staticmethod
    def star(n):
        def decorate(passed_function):
            def wrapper(*args, **kwargs):
                print(n * '*')
                result = passed_function(*args, **kwargs)
                print(result)
                print(n * '*')
                return result

            return wrapper

        return decorate

    @star(10)
    def print_sum(self):
        return self.a + self.b

class up():

    def __init__(self):
        self.param_class = A()

def main():
    a = A()
    print(a.sum_values)
    print(a)
    print(repr(a))
    b = A()
    print(a == b)
    print(len(a))

    print('\n')
    a.print_sum()
    print('\n')
    up_class = up()
    with up_class.param_class as bogoss:
        bogoss.b = 5
        print(bogoss.b)
    print(up_class.param_class.b)

if __name__ == '__main__':
    main()
