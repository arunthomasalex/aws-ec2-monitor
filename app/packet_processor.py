
def main():
    response_bytes = (b'GET /favicon.ico HTTP/1.1\r\nHost: 13.127.77.9\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36\r\nAccept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8\r\nReferer: http://13.127.77.9/\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-GB,en-US;q=0.9,en;q=0.8\r\n\r\n')
    response = str(response_bytes, 'utf-8')
    response_lines = response.splitlines()
    method, url, protocol = response_lines[0].split(' ')
    print(method, protocol)
    # print([line for line in response_lines if ':' in line])

if __name__ == "__main__":
    main()