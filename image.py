import os
import cv2
from scipy import ndimage
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        self.source_path = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Image:").pack()
        self.source_entry = tk.Entry(self.root, textvariable=self.source_path, width=50)
        self.source_entry.pack(side=tk.LEFT)
        tk.Button(self.root, text="Browse", command=self.browse_source).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(self.root, text="Process Image", command=self.process_image).pack(pady=10)

    def browse_source(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", ("*.jpeg", "*.jpg", "*.png"))])
        if file_path:
            self.source_path.set(file_path)

    def process_image(self):
        source_path = self.source_path.get()

        if not source_path or not (source_path.endswith(".jpeg") or source_path.endswith(".jpg") or source_path.endswith(".png")):
            messagebox.showerror("Error", "Please select a valid image file.")
            return

        result_path = "Results"
        os.makedirs(result_path, exist_ok=True)

        try:
            result_file = os.path.join(result_path, "processed_image.png")
            self.process_image_helper(source_path, result_file)
            messagebox.showinfo("Success", "Image processing completed. Result saved to 'Results' folder.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def process_image_helper(self, source_path, result_path):
        image = cv2.imread(source_path)

        enhanced_image = self.enhance_image(image)
        cv2.imwrite(result_path, enhanced_image)

    def enhance_image(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        deNoised = ndimage.median_filter(gray_image, 3)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        highPass = clahe.apply(deNoised)

        gamma = highPass/255.0
        gammaFilter = cv2.pow(gamma, 1.5) * 255
        
        return gammaFilter

def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
