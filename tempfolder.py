import random

class RandomNumberGenerator:
    def __init__(self):
        self.previous_number = None
        self.count = 0

    def generate_same_number(self):
        if self.count == 0:
            self.previous_number = random.randint(0, 2)
            self.count = 5
        self.count -= 1
        return self.previous_number

# Example usage
rng = RandomNumberGenerator()
for _ in range(10):
    random_num = rng.generate_same_number()
    print(random_num)
