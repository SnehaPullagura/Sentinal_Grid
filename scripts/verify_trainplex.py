import os
import sys
import json
import urllib.request
import urllib.parse
import uuid

def check_trainplex(zip_path="sentinel_grid_submission.zip"):
    url = "https://train-plex-checker-bot-1--ttejaswar1234.replit.app/api/check"
    print(f"Submitting {zip_path} to {url}...")

    if not os.path.exists(zip_path):
        print(f"Error: {zip_path} does not exist.")
        return

    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    
    with open(zip_path, "rb") as f:
        file_bytes = f.read()

    body = []
    body.append(f"--{boundary}".encode("utf-8"))
    body.append(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(zip_path)}"'.encode("utf-8"))
    body.append(b"Content-Type: application/zip")
    body.append(b"")
    body.append(file_bytes)
    body.append(f"--{boundary}--".encode("utf-8"))
    body.append(b"")
    
    payload = b"\r\n".join(body)

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "SentinelGrid-Verifier/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            resp_bytes = response.read()
            resp_str = resp_bytes.decode("utf-8", errors="ignore")
            print("Response Status:", response.status)
            try:
                resp_json = json.loads(resp_str)
                print(json.dumps(resp_json, indent=2))
                return resp_json
            except Exception:
                print("Response Text:", resp_str)
                return resp_str
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_trainplex()
