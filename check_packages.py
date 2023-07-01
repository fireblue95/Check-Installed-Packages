import yaml
import subprocess
from argparse import ArgumentParser

class CheckPackages:
    def __init__(self):
        self.config_yml = 'config.yml'
        self.__get_opt__()

    def __get_opt__(self) -> None:
        parser = ArgumentParser()

        parser.add_argument('--no-check-dpkg', action="store_true")
        parser.add_argument('--no-check-pypi', action="store_true")

        self.opt = parser.parse_args()

    def __read_yaml__(self) -> None:
        with open(self.config_yml, 'r') as f:
            self.cfg = yaml.load(f, Loader=yaml.FullLoader)

        for k in self.cfg:
            self.cfg[k] = sorted(sorted(filter(lambda x:x, self.cfg[k]), key=len), key=lambda x: x[0].lower())

        self.max_len_dpkg = len(max(self.cfg['dpkg'], key=len))
        self.max_len_pip = len(max(self.cfg['pypi'], key=len))

    def __search_dpkg__(self, pkg: str) -> None:
        command = f"dpkg -l  | grep -v 'local repository' | grep -i {pkg} | wc -l"

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        output = int(result.stdout.strip())

        if output == 0:
            return False
        
        command = f"dpkg -l  | grep -v 'local repository' | grep -i {pkg}"

        result = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip()

        r_list = result.split('\n')

        for line in r_list:
            temp = line.strip().split()
            temp[4] = ' '.join(temp[4:])
            temp = temp[:5]

            if pkg.lower() in temp[1].lower():
                return True
        return False

    def __check_dpkg__(self) -> None:
        
        print(f'{" Checking Dpkg ":=^50}')

        for item in self.cfg['dpkg']:
            is_installed = self.__search_dpkg__(item)

            msg = f"{item:>{self.max_len_dpkg}} : "
            msg += f'\033[32m{"Installed":>13}\033[0m' if is_installed else '\033[31mNot Installed\033[0m'

            print(msg)

        print()

    def __check_pypi__(self) -> None:
        print(f'{" Checking PyPI ":=^50}')

        command = 'pip3 freeze'
        pip_list = list(filter(lambda x:x, subprocess.run(command, shell=True, capture_output=True, text=True).stdout.split('\n')))

        pip_pkgs = {x.split('==')[0].lower():x.split('==')[1] for x in pip_list}

        for item in self.cfg['pypi']:
            msg = f"{item:>{self.max_len_pip}} : "
            msg += f'\033[32m{"Installed":>13} --> {pip_pkgs[item.lower()]}\033[0m' if item.lower() in pip_pkgs else '\033[31mNot Installed\033[0m'

            print(msg)

    def run(self) -> None:
        self.__read_yaml__()

        if self.opt.no_check_dpkg and self.opt.no_check_pypi:
            raise "You're using no check both dpkg and pypi, please active at least one."

        if not self.opt.no_check_dpkg:
            self.__check_dpkg__()

        if not self.opt.no_check_pypi:
           self.__check_pypi__()


if __name__ == "__main__":
    app = CheckPackages()
    app.run()


