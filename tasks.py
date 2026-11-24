# Simulated suggestions. Tasks 3, 6 and 8 are wrong on purpose.
# Each task: (title, buggy code, issue line, explanation, suggested fix, suggestion correct?)

TASKS = [
    ("Average", "def average(nums):\n    return sum(nums) / (len(nums) - 1)", 2,
     "It divides by one less than the number of items.",
     "def average(nums):\n    return sum(nums) / len(nums)", True),

    ("Even numbers", "def is_even(n):\n    return n % 2 == 1", 2,
     "This says odd numbers are even.",
     "def is_even(n):\n    return n % 2 == 0", True),

    ("Largest number", "def find_max(nums):\n    max_val = 0\n    for n in nums:\n        if n > max_val:\n            max_val = n\n    return max_val", 2,
     "Starting at 0 won't work for negative lists. Use a lower starting value.",
     "def find_max(nums):\n    max_val = -1\n    for n in nums:\n        if n > max_val:\n            max_val = n\n    return max_val", False),

    ("Counting vowels", "def count_vowels(s):\n    return sum(ch in 'aeiou' for ch in s)", 2,
     "Capital vowels get missed out.",
     "def count_vowels(s):\n    return sum(ch in 'aeiou' for ch in s.lower())", True),

    ("Reverse a string", "def reverse(s):\n    return s[::1]", 2,
     "The slice step should be -1.",
     "def reverse(s):\n    return s[::-1]", True),

    ("Last item", "def get_last(items):\n    return items[len(items)]", 2,
     "This crashes with an IndexError, so try to catch it.",
     "def get_last(items):\n    try:\n        return items[len(items)]\n    except IndexError:\n        return None", False),
     
    ("Factorial", "def factorial(n):\n    result = 1\n    for i in range(1, n):\n        result *= i\n    return result", 3,
     "The loop stops before multiplying by n.",
     "def factorial(n):\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result", True),
     
    ("Celsius to Fahrenheit", "def c_to_f(c):\n    return c * 9 / 5 - 32", 2,
     "The conversion ratio is the wrong way round.",
     "def c_to_f(c):\n    return c * 5 / 9 + 32", False),
]