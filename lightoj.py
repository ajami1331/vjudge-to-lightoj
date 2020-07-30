from pyquery import PyQuery

class LightOJ:
    def __init__(self, username: str, password: str, browser):
        self.username = username
        self.password = password
        self.browser = browser

    async def login(self):
        page = await self.browser.newPage()
        await page.goto('http://lightoj.com/login_main.php')
        await page.type('#myuserid', self.username)
        await page.type('#mypassword', self.password)
        await page.click('input[type="submit"]')
        await page.waitForNavigation()

    async def get_solve_list(self) -> list:
        page = await self.browser.newPage()
        await page.goto('http://lightoj.com/volume_userstat.php', {
            'waitUntil': 'networkidle2',
            'timeout': 0
        })
        html = await page.content()
        s = PyQuery(html)
        self.solved = list(s('.leftTop').eq(3).parent().parent().find('a').map(lambda i, e: PyQuery(e).text()))
        self.solved_count = len(self.solved)
        return self.solved

    def is_solved(self, problem_number: str) -> bool:
        return problem_number in self.solved

    async def submit(self, problem_number: str, source_code: str):
        print('Submitting ' + problem_number)
        page = await self.browser.newPage()
        await page.goto('http://lightoj.com/volume_submit.php?problem=' + problem_number, {
            'waitUntil': 'networkidle2',
            'timeout': 0
        })
        await page.type('textarea', source_code)
        await page.click('input[type="submit"]')
        print('Submitted ' + problem_number)