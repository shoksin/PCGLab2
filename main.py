import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image

class ImageInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Информация об изображениях')
        self.root.geometry('800x600')
        self.root.resizable(False, False) 

        self.btnLoad = tk.Button(root, text='Выбрать папку', command=self.loadFolder)
        self.btnLoad.pack(pady=10)

        self.table = ttk.Treeview(root, columns=('Имя файла', 'Размер (пиксели)', 'Разрешение (dpi)', 'Глубина цвета', 'Сжатие'), show='headings')
        self.table.heading('Имя файла', text='Имя файла')
        self.table.heading('Размер (пиксели)', text='Размер (пиксели)')
        self.table.heading('Разрешение (dpi)', text='Разрешение (dpi)')
        self.table.heading('Глубина цвета', text='Глубина цвета')
        self.table.heading('Сжатие', text='Сжатие')

        column_widths = [200, 150, 150, 150, 150]
        for col, width in zip(self.table['columns'], column_widths):
            self.table.column(col, width=width)

        self.table.pack(expand=True, fill='both')

    def loadFolder(self):
        folder = filedialog.askdirectory(title='Выберите папку с изображениями')
        if folder:
            self.displayImageInfo(folder)

    def displayImageInfo(self, folder):
        for row in self.table.get_children():
            self.table.delete(row)

        for root, _, files in os.walk(folder):
            for filename in files:
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff')):
                    file_path = os.path.join(root, filename)
                    info = self.getImageInfo(file_path)
                    if info:
                        self.table.insert('', 'end', values=info)

    def getImageInfo(self, image_path):
        try:
            with Image.open(image_path) as img:
                dpi = img.info.get('dpi', (72, 72))
                color_depth = {
                    '1': '1 бит (чёрно-белый)',
                    'L': '8 бит (градации серого)',
                    'P': '8 бит (палитра)',
                    'RGB': '24 бита',
                    'RGBA': '32 бита (цвет + альфа)',
                    'CMYK': '32 бита (цвет с учетом печати)'
                }.get(img.mode, 'Не указано')

                resolution = f"{dpi[0]}x{dpi[1]}"
                size = f"{img.width} x {img.height}"
                return (os.path.basename(image_path), size, resolution, color_depth, img.info.get('compression', '0'))
        except Exception as e:
            print(f"Ошибка при обработке файла {image_path}: {e}")
            return None

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageInfoApp(root)
    root.mainloop()