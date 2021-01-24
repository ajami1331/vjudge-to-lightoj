from pyquery import PyQuery

class LightOJ:
    def __init__(self, username: str, password: str, browser):
        self.username = username
        self.password = password
        self.browser = browser
        self.lang_dict = {'.cpp': 'C++ 14', '.c': 'C', '.java': 'Java 11'}

    async def login(self):
        page = await self.browser.newPage()
        await page.goto('https://lightoj.com/auth/login')
        print('logging in')
        await page.type('input[type="text"]', self.username)
        await page.type('input[type="password"]', self.password)
        await page.click('button[type="submit"]')
        try:
            await page.waitForNavigation()
        except:
            print("Unexpected error:")
            return False
        print('logged in')
        # await page.screenshot({'path': 'logged-in.png'})
        return True
    async def login_github(self):
        page = await self.browser.newPage()
        await page.goto('https://lightoj.com/api/v1/auth/social-redirect/github')
        print('logging in')
        await page.type('input[type="text"]', self.username)
        await page.type('input[type="password"]', self.password)
        await page.click('input[type="submit"]')
        # await page.screenshot({'path': 'logged-in2.png'})
        try:
            await page.waitForNavigation()
            # await page.screenshot({'path': 'logged-in3.png'})
        except:
            print("Unexpected error:")
            return False
        print('logged in')
        # await page.screenshot({'path': 'logged-in.png'})
        return True

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

    async def submit(self, problem_number: str, source_code: str, extension: str):
        print('Submitting ' + problem_number)
        page = await self.browser.newPage()
        await page.goto('https://lightoj.com/problem/' + problem_number, {
            'waitUntil': 'networkidle2',
            'timeout': 0
        })
        print('loaded problem page')
        # await page.screenshot({'path': 'loaded-problem.png'})
        await page.type('input[type="search"]', self.lang_dict[extension])
        await page.keyboard.press('Enter')
        print('selected language')
        await page.focus('textarea[autocorrect="off"]')
        await page.keyboard.down('Control')
        await page.keyboard.press('A')
        await page.keyboard.up('Control')
        await page.type('textarea[autocorrect="off"]', source_code)
        print('pasted code')
        buttons = await page.xpath("//button[contains(., 'Submit')]")
        if len(buttons) > 0:
            # await page.screenshot({'path': 'example1.png'})
            await buttons[0].click()
            # await page.screenshot({'path': 'example2.png'})
            # await page.waitForXPath("//*[contains(text(),'Submission:')]")
            # await page.screenshot({'path': 'example3.png'})
        print('Submitted ' + problem_number)