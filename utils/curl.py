import cloudscraper
import http.client as http_client
from utils.logger import logger

http_client.HTTPConnection.debuglevel = 1

# Инициализация cookies и headers
cookies = {
    '__Secure-ETC': '4daf92ab9c5390fed26a4347eda400f9',
    'xcid': 'cd1e23fae6d9e95dfc4b62746940560e',
    '__Secure-ext_xcid': 'cd1e23fae6d9e95dfc4b62746940560e',
    '__Secure-access-token': '8.0.2PzriFztTgmBCLsI3oG2sQ.50.Af98YGAylvUbzfaeK2BOunxV98tIinskIB93KBrS63KiMfe3k20d3PEgeAkfC3nF7TwzePdSWVwLpACNJtNLhEFXmgoPz7QI60CzlBFvKqe5..20250628105015.5R-QloKAob49zUQUsEdO2mCMsToM9mYGkGX_29j8rVQ.1612d897755df81cf',
    '__Secure-ab-group': '50',
    '__Secure-refresh-token': '8.0.2PzriFztTgmBCLsI3oG2sQ.50.Af98YGAylvUbzfaeK2BOunxV98tIinskIB93KBrS63KiMfe3k20d3PEgeAkfC3nF7TwzePdSWVwLpACNJtNLhEFXmgoPz7QI60CzlBFvKqe5..20250628105015.fX616YIG-cqaWJsD44q01o6ea92Fl1yNxX94IC7_nSM.14d3943507717379e',
    '__Secure-user-id': '0',
    'rfuid': 'LTE5NTAyNjU0NzAsMTI0LjA0MzQ3NTI3NTE2MDc0LDE5MDczMzM5MzQsLTEsODM5NTE1NDY3LFczc2libUZ0WlNJNklsQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMWxJRkJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFwZFcwZ1VFUkdJRlpwWlhkbGNpSXNJbVJsYzJOeWFYQjBhVzl1SWpvaVVHOXlkR0ZpYkdVZ1JHOWpkVzFsYm5RZ1JtOXliV0YwSWl3aWJXbHRaVlI1Y0dWeklqcGJleUowZVhCbElqb2lZWEJ3YkdsallYUnBiMjR2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZTeDdJblI1Y0dVaU9pSjBaWGgwTDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMWRmU3g3SW01aGJXVWlPaUpOYVdOeWIzTnZablFnUldSblpTQlFSRVlnVm1sbGQyVnlJaXdpWkdWelkzSnBjSFJwYjI0aU9pSlFiM0owWVdKc1pTQkViMk4xYldWdWRDQkdiM0p0WVhRaUxDSnRhVzFsVkhsd1pYTWlPbHQ3SW5SNWNHVWlPaUpoY0hCc2FXTmhkR2x2Ymk5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlMSHNpZEhsd1pTSTZJblJsZUhRdmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmVjE5TEhzaWJtRnRaU0k2SWxkbFlrdHBkQ0JpZFdsc2RDMXBiaUJQUkVZaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMWQsV3lKbGJpMVZVeUpkLDAsMSwwLDI0LDIzNzQxNTkzMCw4LDIyNzEyNjUyMCwwLDEsMCwtNDkxMjc1NTIzLFIyOXZaMnhsSUVsdVl5NGdUbVYwYzJOaGNHVWdSMlZqYTI4Z1YybHVNeklnTlM0d0lDaFhhVzVrYjNkeklFNVVJREV3TGpBN0lGZHBialkwT3lCNE5qUXBJRUZ3Y0d4bFYyVmlTMmwwTHpVek55NHpOaUFvUzBoVVRVd3NJR3hwYTJVZ1IyVmphMjhwSUVOb2NtOXRaUzh4TXpjdU1DNHdMakFnVTJGbVlYSnBMelV6Tnk0ek5pQXlNREF6TURFd055Qk5iM3BwYkd4aCxleUpqYUhKdmJXVWlPbnNpWVhCd0lqcDdJbWx6U1c1emRHRnNiR1ZrSWpwbVlXeHpaU3dpU1c1emRHRnNiRk4wWVhSbElqcDdJa1JKVTBGQ1RFVkVJam9pWkdsellXSnNaV1FpTENKSlRsTlVRVXhNUlVRaU9pSnBibk4wWVd4c1pXUWlMQ0pPVDFSZlNVNVRWRUZNVEVWRUlqb2libTkwWDJsdWMzUmhiR3xsWkNKOUxDSlNkVzV1YVc1blUzUmhkR1VpT25zaVEwRk9UazlVWDFKVlRpSTZJbU5oYm01dmRGOXlkVzRpTENKU1JVRkVXVjlVVDE5U1ZVNGlPaUp5WldGa2VWOTBiMTl5ZFc0aUxDSlNWVTVPU1U1SElqb2ljblZ1Ym1sdVp5SjlmWDE5LDY1LC0xMjg1NTUxMywxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LDExNjQyNjMwODQsMTI=',
    'abt_data': '7.LEz3eLvq2hjBxBb3qm5JBLYRJkNms8M-Z7sl7Gdt2vN4K4GZmMMclULvMCVF6G5S_pumwHDNyzRuEw7oLk8JaRdwDikwdaPIq44kAV49KR526JYFFIW21MuVAKH5lgwA1hkfqDPcJG9oLR-t3l4Hukevh8wcNozabOcCwOazHhKWPJNhni5Ezcw-spPvUtD2jNEkY8OR2miHmcubP9MMRHsQ7OEoOpC_4kAtPhCPqmA29fv51D-4j9FPygWRXbtRyeZvwDLX8CiaCbip4D6IDKhNGBi_dHk_TZBXNYrxYQbqXqfEgYtmsj-TGQCM16okEVsSzkcXosAJJr9qcK4yNuslOHk0p-PROkYmbdffWDF9ymLqvSn5SHsimDWzPmOD7bjL0dAH0I3lm1qd0k6VEVFgHQj2Df6w0dSQaqTsJMcyFZ6SllVIMXuf2ObBJJgbRPzHmU9mc8r99XdXbEhcHa2vBQa8p41aut_1PGQ6qAfaSA3n0M6GkL_Emg',
    'ADDRESSBOOKBAR_WEB_CLARIFICATION': '1751100693',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'referer': 'https://www.ozon.ru/product/lanch-boks-850-ml-konteyner-dlya-hraneniya-edy-s-otdeleniyami-i-priborami-1549274404/?__rr=2&abt_att=1',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-o3-app-name': 'dweb_client',
    'x-o3-app-version': 'release_26-5-2025_3df3a176',
    'x-o3-manifest-version': 'frontend-ozon-ru:3df3a1760e5fe7f836f2e165b20a52747b356b20,sf-render-api:ff810241b78f140424574dbbbc06b3cf55e8bdaa',
    'x-o3-parent-requestid': '50377e5ecdeeac364192d16fc613dc35',
    'x-page-view-id': 'de93efa6-f3ac-4d67-a8c0-a66aac28c04d',
}

scraper = cloudscraper.create_scraper()

def make_request(url, params=None):
    response = scraper.get(url, params=params, cookies=cookies, headers=headers) 

    logger.info(f'Статус {response.status_code}')
