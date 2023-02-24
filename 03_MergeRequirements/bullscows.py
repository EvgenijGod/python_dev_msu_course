from collections import defaultdict
import random
import argparse
import os
import urllib.request
from cowsay import cowsay, get_random_cow

def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    secret_chars = defaultdict(int)
    for c in secret:
        secret_chars[c] += 1
    for i in range(len(guess)):
        if i < len(secret) and guess[i] == secret[i]:
            bulls += 1
            secret_chars[guess[i]] -= 1
        elif secret_chars[guess[i]]:
            secret_chars[guess[i]] -= 1
            cows += 1
    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    prompt = f"""
    # @==@ {prompt}
    #        \  
    #         \   !__!
    #          \  (*o)\_______
    #             (__)\ @@@@@@)\/\\
    #                 ||----w |
    #                 ||     ||
    """
    guess = input(prompt)
    if not valid:
        while guess not in valid:
            guess = input(prompt)
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay(message = format_string.format(bulls, cows), cow=get_random_cow()) + '\n')


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    cnt = 0
    while True:
        cnt += 1
        guess = ask("Введите слово: ", words)
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
        if b == len(secret):
            break
    return cnt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cowsay app')
    parser.add_argument('dictionary', type=str, nargs=1,
                    help='allowed words dictionary')
    parser.add_argument('--word_len', type=int, default=5, required=False, help='an integer for the accumulator')
    args = parser.parse_args()

    if os.path.exists(args.dictionary[0]):
        file_name = args.dictionary[0]
    else:
        file_name = args.dictionary[0].split('/')[-1]
        urllib.request.urlretrieve(args.dictionary[0], file_name)

    words = []
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            if len(line) == args.word_len:
                words.append(line)
    
    cnt = gameplay(ask=ask, inform=inform, words=words)
    print(cowsay(message = f"Верно! Вы потратили {cnt} попыток", cow=get_random_cow()) + '\n')