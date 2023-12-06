import argparse
import requests
import time
from pathlib import Path

def reset_to_sync(host:str) -> bool:
    print("Trying to reset board.")
    r = requests.post("http://" + host + "/pgmmega/sync", timeout=10)
    if r.status_code != 204:
        return False
    r = requests.get("http://" + host + "/pgmmega/sync", timeout=2)
    print(r.text)
    return r.text.startswith("SYNC")

def upload_firmware_file(host:str, hex_path:str) -> bool:
    print("Uploading firmware " + hex_path)
    try:
        r = requests.post(
            "http://" + host + "/pgmmega/upload", 
            data=Path(hex_path).read_bytes(),
            timeout=20
        )
        print(r.text)
        return r.status_code == 200
    except requests.exceptions.RequestException as exc:
        print("Exception occurred during upload: " + repr(exc))
        return False

def upload(host:str, hex_path:str):
    print("==== ESP-LINK UPLOAD ===")
    print("Uploading to http://" + host)
    # out of experience: reset twice.
    maxtries = 5
    for _ in range(maxtries):
        if not reset_to_sync(host):
            print("Warning: Retrying to sync to Optiboot.")
            time.sleep(0.5)
        else:
            print("Reset to sync with Optiboot OK.")
            break
    for _ in range(maxtries):
        if upload_firmware_file(host, hex_path):
            print("Firmware uploaded successfully")
            # do instant reboot instead of waiting for bootloader exit timeout
            try:
                requests.post('http://' + host + '/console/reset')
            except:
                pass
            return True
        else:
            # reset for next try
            reset_to_sync(host)
    print("Exhausted retries for uploading.")
    return False

def main():
    parser = argparse.ArgumentParser(description='Upload using esp-link web API.')
    parser.add_argument('-P','--port', help='IP or hostname of esp-link', required=True)
    parser.add_argument('-b','--baud', help='Baud rate (ignored)', required=False)
    parser.add_argument('-D','--disable-erase', help='Disable erase (ignored)', action='store_const', required=False)
    parser.add_argument('file', nargs=1, help='Firmware .hex file')
    args = parser.parse_args()
    if len(args.file) != 1:
        print("Must give firmware hex file as argument.")
        exit(-1)
    ok = upload(args.port, args.file[0])
    exit(0 if ok else -1)

if __name__ == '__main__':
    main()