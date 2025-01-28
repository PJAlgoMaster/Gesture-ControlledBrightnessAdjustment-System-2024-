import time
import hashlib

def generate_code():
    current_time = int(time.time() // 600)
    return hashlib.sha256(str(current_time).encode()).hexdigest()[:6]

# Example usage
if __name__ == "__main__":
    print("Current code:", generate_code())
