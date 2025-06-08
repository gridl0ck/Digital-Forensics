from iphone_backup_decrypt import EncryptedBackup
import os

passphrase = "Yousuock05!"
backup_path = "/home/gridl0ck/Downloads/00008140-000A55E236E3001C"

backup = EncryptedBackup(backup_directory=backup_path, passphrase=passphrase)

# This ensures Manifest.db is decrypted and opened
backup.test_decryption()

domain_map = {}

with backup.manifest_db_cursor() as cur:
    cur.execute("SELECT domain, relativePath FROM Files WHERE flags=1")
    for domain, rel_path in cur.fetchall():
        if domain and rel_path:
            domain_map.setdefault(domain, []).append(rel_path)

os.makedirs("./output", exist_ok=True)
with open("./output/all_paths.txt", "w") as f:
    for domain in sorted(domain_map):
        f.write(f"==== {domain} ====\n")
        for path in sorted(domain_map[domain]):
            f.write(f"{path}\n")
        f.write("\n")

print("[+] Successfully wrote all file paths to ./output/all_paths.txt")

