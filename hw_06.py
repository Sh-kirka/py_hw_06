import os
import shutil
import re

image_extensions = ('.jpeg', '.png', '.jpg', '.svg')
video_extensions = ('.avi', '.mp4', '.mov', '.mkv')
document_extensions = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
music_extensions = ('.mp3', '.ogg', '.wav', '.amr')
archive_extensions = ('.zip', '.gz', '.tar')
known_extensions = set()

# Словники
images = {}
videos = {}
documents = {}
music = {}
archives = {}
unknown = {}


def normalize(filename):
    # Транслітерація
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'iu', 'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'І': 'I', 'Ї': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ь': '', 'Ю': 'Iu', 'Я': 'Ia'
    }

    # Транслітерація
    translit_filename = ''.join(translit_dict.get(char, char)
                                for char in filename)

    # Заміна символів на '_'
    normalized_filename = re.sub(r'[^a-zA-Z0-9]', '_', translit_filename)

    return normalized_filename


def process_folder(folder_path):
    global images, videos, documents, music, archives, unknown

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            # Перевірка extension і додавання файлів в категорію
            if file_extension in image_extensions:
                images[file] = file_path
            elif file_extension in video_extensions:
                videos[file] = file_path
            elif file_extension in document_extensions:
                documents[file] = file_path
            elif file_extension in music_extensions:
                music[file] = file_path
            elif file_extension in archive_extensions:
                archives[file] = file_path
            elif file_extension != '.gitignore':  # Виключення файлів .gitignore
                unknown[file] = file_path

            normalized_filename = normalize(file)
            normalized_file_path = os.path.join(
                root, normalized_filename + file_extension)
            os.rename(file_path, normalized_file_path)

    # Оновлення known_extensions
    known_extensions.update(image_extensions, video_extensions,
                            document_extensions, music_extensions, archive_extensions)

    # Рекурсія для вкладених папок
    for folder in dirs:
        folder_path = os.path.join(root, folder)
        process_folder(folder_path)


# Виклик функції to process the folder
folder_path = '/Users/karinashevela/Desktop/hw'
process_folder(folder_path)

# Виведення результатів
print("List of files in the 'Images' category:")
for file in images:
    print(file)

print("List of files in the 'Videos' category:")
for file in videos:
    print(file)

print("List of files in the 'Documents' category:")
for file in documents:
    print(file)

print("List of files in the 'Music' category:")
for file in music:
    print(file)

print("List of files in the 'Archives' category:")
for file in archives:
    print(file)

print("List of files with unknown extension:")
for file in unknown:
    print(file)

print("List of all known extensions:")
known_extensions = set()
known_extensions.update(image_extensions, video_extensions, document_extensions,
                        music_extensions, archive_extensions)
for extension in known_extensions:
    print(extension)
