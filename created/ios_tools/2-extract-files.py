from iphone_backup_decrypt import EncryptedBackup
import os

# Setup
passphrase = "Yousuock05!"
backup_path = "/home/gridl0ck/Downloads/00008140-000A55E236E3001C"
paths_file = "./output/all_paths.txt"
output_root = "./output/extracted_files"

backup = EncryptedBackup(backup_directory=backup_path, passphrase=passphrase)

# Ensure manifest is decrypted
backup.test_decryption()

# === Parse all_paths.txt ===
extraction_jobs = []  # List of (domain, relative_path)

with open(paths_file, "r") as f:
    current_domain = None
    for line in f:
        line = line.strip()
        if line.startswith("====") and line.endswith("===="):
            current_domain = line.strip("= ").strip()
        elif line and current_domain:
            extraction_jobs.append((current_domain, line))

# === Extract each file ===
for domain, rel_path in extraction_jobs:
    sanitized_domain = domain.replace("/", "_")
    rel_output_path = os.path.join(output_root, sanitized_domain, rel_path)
    os.makedirs(os.path.dirname(rel_output_path), exist_ok=True)

    try:
        print(f"[+] Extracting {domain} :: {rel_path}")
        backup.extract_file(relative_path=rel_path, domain_like=domain, output_filename=rel_output_path)
    except Exception as e:
        print(f"[!] Failed to extract {domain}/{rel_path}: {e}")
