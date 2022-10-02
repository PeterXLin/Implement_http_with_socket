import subprocess

result = subprocess.run(
    # program and arguments
    ['php', 'D:\\Codes\\python\\Implement_http_with_socket\\webroot\\try_php\\test.php'],
    stdout=subprocess.PIPE,  # capture stdout
    check=True               # raise exception if program fails
)

print(result.stdout)         # result.stdout contains a byte-string
