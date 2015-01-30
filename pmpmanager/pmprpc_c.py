import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
print c.hello("RPC")
client_type = "dbacfc64-493d-4f96-9cac-c2bb5427f721"

print c.dink(1)


print c.register(1)
print c.registerd()
