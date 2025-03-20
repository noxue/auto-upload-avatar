import requests
import logging
from datetime import datetime
import json
import os
from config import HEADERS, COOKIES, API_URLS

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cookie_check.log'),
        logging.StreamHandler()
    ]
)

class CookieChecker:
    def __init__(self):
        self.url = API_URLS['user_detail']
        self.headers = HEADERS
        self.cookies = COOKIES
        
        # 创建cookie存储目录
        self.cookie_dir = 'cookies'
        if not os.path.exists(self.cookie_dir):
            os.makedirs(self.cookie_dir)

    def save_cookies(self):
        """保存Cookie到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{self.cookie_dir}/cookies_{timestamp}.json'
        with open(filename, 'w') as f:
            json.dump(self.cookies, f, indent=4)
        logging.info(f'Cookies已保存到文件: {filename}')

    def check_alive(self):
        """检查Cookie是否有效"""
        try:
            # 发送请求
            response = requests.get(
                self.url, 
                headers=self.headers, 
                cookies=self.cookies,
                timeout=10
            )
            
            # 检查响应
            if response.status_code == 200:
                result = response.json()
                if result['errno'] == 0:
                    logging.info('Cookie状态正常')
                    # 保存有效的Cookie
                    self.save_cookies()
                    return True
                else:
                    logging.warning(f'接口返回错误: {result.get("errmsg")}')
            else:
                logging.warning(f'请求失败，状态码: {response.status_code}')
            
            return False
            
        except Exception as e:
            logging.error(f'检查Cookie发生错误: {str(e)}')
            return False

if __name__ == '__main__':
    checker = CookieChecker()
    try:
        result = checker.check_alive()
        print('Cookie检查结果:', '有效' if result else '无效')
    except Exception as e:
        logging.error(f'程序异常: {str(e)}')