from zeep import Client

# URL WSDL
wsdl = "http://127.0.0.1:8000/calculator/soap/?wsdl"

# Inisialisasi klien Zeep
client = Client(wsdl=wsdl)

# Menampilkan daftar operasi SOAP yang tersedia
print("Available operations:")
for operation in client.service._binding._operations.keys():
    print(operation)

result = client.service.add(a=5, b=3)
print(f"Result: {result}")
