
import hashlib
from pathlib import Path
import hmac

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "model" / "phishing_model.joblib"
HASH_PATH = PROJECT_DIR / "model" / "trusted_model_hash.txt"


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def main():
    print("PHISHGUARD - SHA-256 INTEGRITY VERIFICATION")
    print("-" * 48)

    if not MODEL_PATH.exists():
        print("ERROR: Model file not found.")
        return

    current_hash = calculate_sha256(MODEL_PATH)

    if not HASH_PATH.exists():
        HASH_PATH.write_text(current_hash + "\n", encoding="utf-8")
        print("Reference hash created.")
        print("SHA-256:", current_hash)
        print("Run the program again to verify the saved reference.")
        return

    trusted_hash = HASH_PATH.read_text(
        encoding="utf-8"
    ).strip()

    if not trusted_hash:
        print("ERROR: Reference hash is empty.")
        print("Restore a trusted reference before checking integrity.")
        return

    if hmac.compare_digest(current_hash, trusted_hash):
        print("INTEGRITY VERIFIED")
        print("The model matches the saved reference.")
    else:
        print("INTEGRITY CHECK FAILED")
        print("The model does not match the saved reference.")

    print("Current SHA-256:", current_hash)


if __name__ == "__main__":
    main()
