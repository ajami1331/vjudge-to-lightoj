import asyncio
from pyppeteer import launch
from lightoj import LightOJ
from vjudge import Vjudge
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
    print('Vjudge')
    vjudge_username = input('User Id or E-mail: ')
    vjudge_password = input('Password: ')
    vjudge = Vjudge(vjudge_username, vjudge_password)
    vjudge.downloadSubmissions()
    print('LightOJ')
    lightoj_username = input('User Id or E-mail: ')
    lightoj_password = input('Password: ')
    directory_path = 'solutions/LightOJ'
    lightOj = LightOJ(lightoj_username, lightoj_password, browser)
    await lightOj.login()
    print(await lightOj.get_solve_list())
    if not os.path.exists(directory_path):
        print('No LightOJ solutions')
        exit(0)
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