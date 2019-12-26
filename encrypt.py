import base64
x = base64.b64encode(bytes('pawar', 'utf-8'))
print(x)

stringValue = base64.b64decode(x).decode('utf-8')
print(stringValue)