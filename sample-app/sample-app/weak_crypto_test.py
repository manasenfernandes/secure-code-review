import hashlib

password = "test123"

md5_hash = hashlib.md5(password.encode()).hexdigest()
sha1_hash = hashlib.sha1(password.encode()).hexdigest()

print(md5_hash)
print(sha1_hash)
