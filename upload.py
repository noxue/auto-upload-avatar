import requests
from config import COOKIES, HEADERS, API_URLS

def upload_image(image_path):
    # 上传接口URL
    url = API_URLS['user_alter']
    
    # 请求头
    headers = HEADERS
    
    # Cookie
    cookies = COOKIES
    
    # 准备文件
    files = {
        'avatar': ('1.png', open(image_path, 'rb'), 'image/png')
    }
    
    try:
        # 发送请求
        response = requests.post(url, headers=headers, cookies=cookies, files=files)
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            if result.get('errno') == 0:
                print('上传成功:', result)
                return True
            else:
                print('上传失败:', result.get('errmsg'))
                return False
        else:
            print(f'请求失败，状态码: {response.status_code}')
            return False
            
    except Exception as e:
        print(f'发生错误: {str(e)}')
        return False


def get_avatar_url():
    # 获取用户详情接口URL
    url = API_URLS['user_detail']
    
    # 请求头
    headers = HEADERS
    
    # Cookie
    cookies = COOKIES
    
    try:
        # 发送GET请求
        response = requests.get(url, headers=headers, cookies=cookies)
        
        # 检查响应状态码
        if response.status_code == 200:
            result = response.json()
            if result['errno'] == 0:
                # 返回头像URL
                return result['data']['img_url']
            else:
                print('获取失败:', result.get('errmsg'))
                return None
        else:
            print(f'请求失败，状态码: {response.status_code}')
            return None
            
    except Exception as e:
        print(f'发生错误: {str(e)}')
        return None
    
if __name__ == '__main__':
    # 上传当前目录下的1.png
    upload_image('./1.png')

    # 获取头像URL
    avatar_url = get_avatar_url()
    print(f'头像URL: {avatar_url}')


