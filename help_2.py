import shutil
import os
images_moto = '/home/boris/Documents/motogp_api/images'
class_moto = os.listdir('/home/boris/Documents/matplotlib_exercize/moto_pdfs')

for cm in class_moto:
    if cm not in ['motogp', 'moto2', 'moto3']:
        continue
    year = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}')
    for y in year:
        if y in ['2025']:#'2019', '2020', '2021', '2022', '2023', '2024']:
            continue
        list_of_year = os.listdir(f'{images_moto}/{cm}')
        if y not in list_of_year:
            os.mkdir(f'{images_moto}/{cm}/{y}')
        if not os.path.isdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}'):
            continue
        races = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}') 
        for r in races:
            seasion = os.listdir(f'/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}')
            for s in seasion:
                print(f"/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}")
                if s not in ['rac']:
                    continue
                source_path_1 = f"/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/circuit_big_page.png"
                source_path_2 = f"/home/boris/Documents/matplotlib_exercize/moto_pdfs/{cm}/{y}/{r}/{s}/circuit_small_page.png"
                destination_path_1 = f"{images_moto}/{cm}/{y}/{r}/{s}/circuit_big_page.png"
                destination_path_2 = f"{images_moto}/{cm}/{y}/{r}/{s}/circuit_small_page.png"

                try:
                    shutil.copy(source_path_1, destination_path_1)
                    shutil.copy(source_path_2, destination_path_2)
                    print(f"File '{source_path_1}' copied to '{destination_path_1}' successfully.")
                except FileNotFoundError:
                    print(f"Error: Source file '{source_path_1}' not found.")
                except shutil.SameFileError:
                    print("Error: Source and destination paths are the same.")
                except Exception as e:
                    print(f"An error occurred: {e}")