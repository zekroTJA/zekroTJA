import re
import datetime
from typing import List


TARGET = './README.md'


class Replacer:
    orig:   str
    func:   str
    arg:    str
    target: str

    def __init__(self, match):
        self.orig = match[0]
        self.func = match[1]
        if len(match) > 3:
            self.arg = match[2]
            self.target = match[3]
        else:
            self.target = match[2]

    def re_assemble(self, result) -> str:
        arg = (':' + self.arg) if self.arg else ''
        return '<!--{}{}-->{}'.format(self.func, arg, result)

    def get_result(self) -> str:
        if self.func == 'age' and self.arg:
            bd = datetime.datetime.strptime(self.arg, '%Y-%m-%d')
            now = datetime.date.today()
            age = now.year - bd.year
            if now.month < bd.month or \
                    (now.month == bd.month and now.day < bd.day):
                age -= 1
            return '{}'.format(age)
        raise Exception(f"unimplemented function '{self.func}'")

    def ex(self) -> str:
        res = self.get_result()
        return self.re_assemble(res)



def find_all_replacers(target: str) -> List[Replacer]:
    matches = re.findall(
        '(<!--\\s?([\\w/-]+)(?::([\\w/-]+))?-->([\\w/-]+))\\s', target)
    return [Replacer(m) for m in matches]


def main():
    target_contents = ''
    with open(TARGET, 'r') as f:
        target_contents = f.read()

    for rep in find_all_replacers(target_contents):
        target_contents = target_contents.replace(rep.orig, rep.ex())

    with open(TARGET, 'w') as f:
        f.write(target_contents)


if __name__ == '__main__':
    main()
