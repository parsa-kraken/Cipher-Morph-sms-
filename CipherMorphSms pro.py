import sys

#-------------------------------------------
# parsa kraken  (cipher morph sms pro)
#-------------------------------------------

digit_to_letter = {'0': 'q','1': 'w','2': 'e','3': 'r','4': 't','5': 'y','6': 'u','7': 'i','8': 'o','9': 'p'}
letter_to_digit = {v: k for k, v in digit_to_letter.items()}

def atbash_char(ch: str) -> str:
    if 'a' <= ch <= 'z':
        return chr(ord('z') - (ord(ch) - ord('a')))
    if 'A' <= ch <= 'Z':
        return chr(ord('Z') - (ord(ch) - ord('A')))
    return ch

symbol_map_enc = {':':'#','/':'*','.' :'~','-':'=','_':'+','?':'!','&':'%','@':'$'}
symbol_map_dec = {v: k for k, v in symbol_map_enc.items()}

def substitute_encode(text: str) -> str:
    return ''.join(
        digit_to_letter[ch] if ch.isdigit() else
        atbash_char(ch) if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') else
        symbol_map_enc.get(ch, ch)
        for ch in text
    )

def substitute_decode(text: str) -> str:
    return ''.join(
        letter_to_digit[ch] if ch in letter_to_digit else
        atbash_char(ch) if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') else
        symbol_map_dec.get(ch, ch)
        for ch in text
    )

def normalize_prefix_once(text: str) -> str:
    return "1" + text[len("vless://"):] if text.startswith("vless://") else text

def denormalize_prefix_once(text: str) -> str:
    return "vless://" + text[1:] if text.startswith("1") else text

# --- Secondary key XOR ---
def apply_key(data: str, key: str) -> str:
    key_bytes = key.encode()
    out = []
    for i, ch in enumerate(data.encode()):
        out.append(chr(ch ^ key_bytes[i % len(key_bytes)]))
    return ''.join(out)

def encrypt_message(plain: str, key: str) -> str:
    normalized = normalize_prefix_once(plain)
    sub = substitute_encode(normalized)
    return apply_key(sub, key)

def decrypt_message(ciphertext: str, key: str) -> str:
    sub = apply_key(ciphertext, key)
    normalized = substitute_decode(sub)
    return denormalize_prefix_once(normalized)

def main():
    print("1- Encrypt 🔐")
    print("2- Decrypt 🔓")
    choice = input("Your choice: ").strip()
    if choice == "1":
        msg = input("Enter message: ").strip()
        key = input("Enter secondary key: ").strip()
        print("Encrypted Output 📤:")
        print(encrypt_message(msg, key))
    elif choice == "2":
        msg = input("Enter encrypted text: ").strip()
        key = input("Enter secondary key: ").strip()
        print("Decrypted Output 📥:")
        print(decrypt_message(msg, key))
    else:
        print("Invalid option ❌")

if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] in ("enc", "dec"):
        mode, a, key = sys.argv[1], sys.argv[2], sys.argv[3]
        if mode == "enc":
            print("Encrypted Output 📤:")
            print(encrypt_message(a, key))
        else:
            print("Decrypted Output 📥:")
            print(decrypt_message(a, key))
    else:
        main()

#-------------------------------------------
# parsa kraken  (cipher morph sms pro)
#-------------------------------------------