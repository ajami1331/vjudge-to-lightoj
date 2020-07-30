import asyncio
from pyppeteer import launch
from lightoj import LightOJ
import os

async def main():
    browser = await launch({
            'args': [
                '--disable-gpu',
                '--disable-dev-shm-usage',
                '--disable-setuid-sandbox',
                '--no-first-run',
                '--no-sandbox',
                '--no-zygote',
                '--single-process']
    })
    username = input('User Id or E-mail: ')
    password = input('Password: ')
    directory_path = 'solutions'
    lightOj = LightOJ(username, password, browser)
    await lightOj.login()
    print(await lightOj.get_solve_list())
    for problem_number in os.listdir(directory_path):
        if lightOj.is_solved(problem_number):
            print(problem_number + " is already solved")
        else:
            print(problem_number + " is not solved")
            for file in os.listdir(directory_path + '/' + problem_number):
                with open(directory_path + '/' + problem_number + '/' + file) as file:
                    source_code = file.read()
                    await lightOj.submit(problem_number, source_code)

    print(await lightOj.get_solve_list())

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())