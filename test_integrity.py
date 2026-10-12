
import hashlib
import tempfile
import hmac
from pathlib import Path


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


print("PHISHGUARD - SHA-256 TAMPER DETECTION TEST")
print("-" * 48)

# Create a temporary test file
with tempfile.TemporaryDirectory() as temp_dir:
    test_file = Path(temp_dir) / "sample.txt"

    test_file.write_text(
        "Original PhishGuard test data",
        encoding="utf-8"
    )

    # Record the original hash
    trusted_hash = calculate_sha256(test_file)
    print("Original hash:", trusted_hash)

    # Verify the unchanged file
    current_hash = calculate_sha256(test_file)

    if hmac.compare_digest(current_hash, trusted_hash):
        print("\nTest 1: INTEGRITY VERIFIED")
    else:
        print("\nTest 1: INTEGRITY CHECK FAILED")

    # Change the temporary file
    test_file.write_text(
        "Modified PhishGuard test data",
        encoding="utf-8"
    )

    # Verify again against the original reference
    changed_hash = calculate_sha256(test_file)

    if hmac.compare_digest(changed_hash, trusted_hash):
        print("Test 2: INTEGRITY VERIFIED")
    else:
        print("Test 2: INTEGRITY CHECK FAILED")

    print("\nOriginal and changed hashes match:",
          hmac.compare_digest(trusted_hash, changed_hash))

print("\nTest completed. Temporary test file removed.")
