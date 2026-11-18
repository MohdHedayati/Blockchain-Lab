#!/bin/bash
# Experiment 2 - OpenSSL: symmetric keys, file encryption/decryption, RSA key pair
set -x
openssl version

# 1. Symmetric keys (128, 192, 256 bit = 16, 24, 32 random bytes, hex encoded)
openssl rand -hex 16 > key128.txt
openssl rand -hex 24 > key192.txt
openssl rand -hex 32 > key256.txt
cat key128.txt key192.txt key256.txt

# 2. File with name and address
printf 'Name: Mohammed Mehdi Hedayati\nAddress: Veermata Jijabai Technological Institute, Matunga, Mumbai - 400019\n' > details.txt
cat details.txt

# 3. Encrypt with AES-256-CBC using the 256-bit key (a random IV is generated too)
KEY=$(cat key256.txt)
IV=$(openssl rand -hex 16)
openssl enc -aes-256-cbc -in details.txt -out details.enc -K "$KEY" -iv "$IV"
echo "IV: $IV"
xxd details.enc | head

# 4. Decrypt
openssl enc -d -aes-256-cbc -in details.enc -out details_decrypted.txt -K "$KEY" -iv "$IV"
cat details_decrypted.txt
diff details.txt details_decrypted.txt && echo "DECRYPTION SUCCESSFUL: files match"

# (Same for 128/192-bit keys)
openssl enc -aes-128-cbc -in details.txt -out d128.enc -K "$(cat key128.txt)" -iv "$IV"
openssl enc -d -aes-128-cbc -in d128.enc -K "$(cat key128.txt)" -iv "$IV"
openssl enc -aes-192-cbc -in details.txt -out d192.enc -K "$(cat key192.txt)" -iv "$IV"
openssl enc -d -aes-192-cbc -in d192.enc -K "$(cat key192.txt)" -iv "$IV"

# 5. RSA key pair (2048 bit)
openssl genrsa -out rsa_private.pem 2048
openssl rsa -in rsa_private.pem -pubout -out rsa_public.pem
openssl rsa -in rsa_private.pem -noout -text | head -5
cat rsa_public.pem

# Bonus: encrypt/decrypt with RSA
echo "hello blockchain" > msg.txt
openssl pkeyutl -encrypt -pubin -inkey rsa_public.pem -in msg.txt -out msg.enc
openssl pkeyutl -decrypt -inkey rsa_private.pem -in msg.enc
