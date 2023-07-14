import browser_cookie3


class Utils:
    browsers = [ 
        browser_cookie3.chrome,   # 62.74% market share
        browser_cookie3.safari,   # 24.12% market share
        browser_cookie3.firefox,  #  4.56% market share
        browser_cookie3.edge,     #  2.85% market share 
        browser_cookie3.opera,    #  1.69% market share
        browser_cookie3.brave,    #  0.96% market share
        browser_cookie3.opera_gx, #  0.64% market share
        browser_cookie3.vivaldi,  #  0.32% market share
    ]

    def get_cookies(self, setName: str = None, setBrowser: str = False) -> dict:
        cookies = {}

        for browser in Utils.browsers:
            if (
                setBrowser != False
                and browser.__name__ == setBrowser
                or setBrowser == False
            ):
                try:
                    for c in browser(domain_name=self):
                        if c.name not in cookies:
                            cookies = cookies | {c.name: c.value} 

                except Exception as e:
                    pass

        if not setName:
            return cookies
        try:
            return {setName: cookies[setName]}

        except ValueError:
            print(f'Error: could not find {setName} cookie in any browser.')
            exit(1)
