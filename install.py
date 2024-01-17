import os
import stat

base = os.path.dirname(__file__)

print(f"copying {os.path.join(base, "takecli", "main.py")} -> {os.path.join(base, "bin", "take")}")

with open(os.path.join(base, "takecli", "main.py"), "r") as f:
    script = f.read()

with open(os.path.join(base, "bin", "take"), "w") as f:
    f.write(script)

print(f"chmod +x {os.path.join(base, "bin", "take")}")
st = os.stat(os.path.join(base, "bin", "take"))
os.chmod(os.path.join(base, "bin", "take"), st.st_mode | stat.S_IEXEC)
