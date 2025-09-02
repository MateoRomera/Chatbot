import os
import hashlib

def sha256sum(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_checksums(data_dir="backend/data", checksum_file="backend/data/checksums.sha256"):
    if not os.path.exists(checksum_file):
        print("⚠️ No se encontró el archivo de checksums. Genera datasets primero.")
        return False

    expected = {}
    with open(checksum_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                h, fname = line.strip().split("  ")
                expected[fname] = h

    for fname, expected_hash in expected.items():
        fpath = os.path.join(data_dir, fname)
        if not os.path.exists(fpath):
            print(f"❌ Falta el archivo {fname}")
            return False
        actual_hash = sha256sum(fpath)
        if actual_hash != expected_hash:
            print(f"❌ Checksum no coincide para {fname}")
            return False
    print("✅ Verificación de integridad: todos los archivos están OK.")
    return True
