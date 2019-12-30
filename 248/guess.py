MAX_NUMBER = 15


class InvalidNumber(Exception):
    pass


class GuessGame:

    def __init__(self, secret_number, max_guesses=5):
        self.secret_number = self._validate(secret_number)
        self.max_guesses = max_guesses
        self.attempt = 0

    def _validate(self, number):
        try:
            number = int(number)
        except ValueError:
            raise InvalidNumber('Not a number')
        if number < 0:
            raise InvalidNumber('Negative number')
        if number > MAX_NUMBER:
            raise InvalidNumber('Number too high')
        return number

    def __call__(self):
        while self.attempt < self.max_guesses:
            try:
                print('Guess a number: ')
                guess = int(input())
            except ValueError:
                print('Enter a number, try again')
                continue

            self.attempt += 1

            if guess < self.secret_number:
                print('Too low')
            elif guess > self.secret_number:
                print('Too high')
            else:
                print('You guessed it!')
                break

        else:
            print(f'Sorry, the number was {self.secret_number}')
