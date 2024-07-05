import subprocess

def main():
    subprocess.run(["powershell.exe", "-File", "setup.ps1"], check=True)

if __name__ == "__main__":
    main()
