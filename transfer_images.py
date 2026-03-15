import subprocess
import sys

# --- KONFIGURACIJA ---
DB_NAME = "motogp"
DB_USER_LOCAL = "root"

REMOTE_USER = "root"
REMOTE_IP = "23.95.167.114"
REMOTE_DB_USER = "motogpuser"
REMOTE_DB_PASS = "3TEA8Tohoy6iwLbDVYEL"
GODINA = "2026"
LOCAL_IMAGES_PATH = "/home/boris/Documents/motogp_api/images/"
REMOTE_IMAGES_PATH = "/home/motoslicks-backend/htdocs/backend.motoslicks.com/images"

def run_command(command, shell=True):
    try:
        result = subprocess.run(command, shell=shell, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def deploy():
    print("🚀 Započeta sinhronizacija za MotoSlicks...")

    # 1. SINHRONIZACIJA BAZE (Sve tabele, samo nove stvari)
    # Koristimo .my.cnf koji si već napravio da ne kucamo pass za lokalni dump
    print("📦 1/2 Ažuriram bazu podataka (sve tabele)...")
    TABLES = "entries races"
    TABLES_NO_YEAR = "fastest_laps bikes circuit_info"
    
    db_cmd = (
        f"mariadb-dump -u {DB_USER_LOCAL} --no-create-info --insert-ignore --quick --where=\"year={GODINA}\" {DB_NAME} {TABLES}| "
        f"ssh {REMOTE_USER}@{REMOTE_IP} 'mariadb -u {REMOTE_DB_USER} -p{REMOTE_DB_PASS} {DB_NAME}'"
    )
    db_cmd_no_year = (
        f"mariadb-dump -u {DB_USER_LOCAL} --no-create-info --insert-ignore --quick {DB_NAME} {TABLES_NO_YEAR}| "
        f"ssh {REMOTE_USER}@{REMOTE_IP} 'mariadb -u {REMOTE_DB_USER} -p{REMOTE_DB_PASS} {DB_NAME}'"
    )
    success, output = run_command(db_cmd)
    succes_1, output_1 = run_command(db_cmd_no_year)
    if success:
        print("    Baza podataka je uspešno osvežena.")
    else:
        print(f"   Greška pri ažuriranju baze: {output}")

    if succes_1:
        print("   Baza podataka je uspešno osvežena.")
    else:
        print(f"   Greška pri ažuriranju baze: {output_1}")

    # 2. SINHRONIZACIJA SLIKA (rsync)
    print("🖼️  2/2 Prenosim nove slike/PDF-ove...")
    
    # Dodajemo '/' na kraj lokalne putanje da rsync ne duplira foldere
    rsync_cmd = f"rsync -avz {LOCAL_IMAGES_PATH} {REMOTE_USER}@{REMOTE_IP}:{REMOTE_IMAGES_PATH}"
    
    success, output = run_command(rsync_cmd)
    if success:
        print("   ✅ Slike/fajlovi su uspešno prebačeni.")
    else:
        print(f"   ❌ Greška pri rsync-u: {output}")

    print("\n Deploy završen!")

if __name__ == "__main__":
    deploy()