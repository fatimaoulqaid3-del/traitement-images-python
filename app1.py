/"""
Application de Traitement d'Images
Conversion de l'application MATLAB app1.mlapp vers Python
Dépendances : pip install opencv-python numpy scipy pillow
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import numpy as np
import cv2
from scipy.ndimage import median_filter, convolve
from PIL import Image, ImageTk


class App1:
    def __init__(self, root):
        self.root = root
        self.root.title("Application Traitement d'Images")
        self.root.geometry("900x560")
        self.root.resizable(True, True)

        self.img_original = None  # image originale (numpy array BGR ou grayscale)

        self._build_menu()
        self._build_canvas()

    # ─────────────────────────────────────────────
    # CONSTRUCTION DE L'INTERFACE
    # ─────────────────────────────────────────────
    def _build_menu(self):
        menubar = tk.Menu(self.root)

        # ── Fichier ──
        fichier = tk.Menu(menubar, tearoff=0)
        fichier.add_command(label="Ouvrir",       command=self.ouvrir)
        fichier.add_command(label="Enregistrer",  command=self.enregistrer)
        fichier.add_separator()
        fichier.add_command(label="Quitter",      command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=fichier)

        # ── Opération ponctuelle ──
        op_ponct = tk.Menu(menubar, tearoff=0)
        op_ponct.add_command(label="Contraste",                    command=self.contraste)
        op_ponct.add_command(label="Décalage Additif",             command=self.decalage_additif)
        op_ponct.add_command(label="Mise à l'échelle Multiplicative", command=self.mise_echelle)
        op_ponct.add_command(label="Inversion",                    command=self.inversion)
        op_ponct.add_command(label="Seuillage",                    command=self.seuillage)
        menubar.add_cascade(label="Opération ponctuelle", menu=op_ponct)

        # ── Bruit ──
        bruit = tk.Menu(menubar, tearoff=0)
        bruit.add_command(label="Gaussien",    command=self.bruit_gaussien)
        bruit.add_command(label="Poivre et Sel", command=self.bruit_poivre_sel)
        menubar.add_cascade(label="Bruit", menu=bruit)

        # ── Filtre Fréquentiel ──
        freq = tk.Menu(menubar, tearoff=0)
        freq.add_command(label="Filtre Passe-Bas",                    command=self.filtre_passe_bas)
        freq.add_command(label="Filtre Passe-Haut",                   command=self.filtre_passe_haut)
        freq.add_command(label="Filtre Passe-bande",                  command=self.filtre_passe_bande)
        freq.add_command(label="Rehaussement des Hautes Fréquences",  command=self.rehaussement_hf)
        menubar.add_cascade(label="Filtre Fréquentiel", menu=freq)

        # ── Filtre Passe-bas ──
        pb = tk.Menu(menubar, tearoff=0)
        lineaire = tk.Menu(pb, tearoff=0)
        lineaire.add_command(label="Moyenneur 3x3",      command=self.moyenneur3)
        lineaire.add_command(label="Moyenneur 5x5",      command=self.moyenneur5)
        lineaire.add_command(label="Filtre Gaussien 3x3", command=self.gaussien3)
        lineaire.add_command(label="Filtre Gaussien 5x5", command=self.gaussien5)
        lineaire.add_command(label="Pyramidal",           command=self.pyramidal)
        lineaire.add_command(label="Conique",             command=self.conique)
        pb.add_cascade(label="Filtre Linéaire", menu=lineaire)
        non_lin = tk.Menu(pb, tearoff=0)
        non_lin.add_command(label="Médian", command=self.median)
        pb.add_cascade(label="Filtre Non Linéaire", menu=non_lin)
        menubar.add_cascade(label="Filtre Passe-bas", menu=pb)

        # ── Filtre Passe-haut ──
        ph = tk.Menu(menubar, tearoff=0)
        ph.add_command(label="Gradient",      command=self.gradient)
        ph.add_command(label="Sobel",         command=self.sobel)
        ph.add_command(label="Prewitt",       command=self.prewitt)
        ph.add_command(label="Robert",        command=self.robert)
        ph.add_command(label="Laplacien",     command=self.laplacien)
        ph.add_command(label="Canny",         command=self.canny)
        ph.add_command(label="Kirsch",        command=self.kirsch)
        ph.add_command(label="Marr-Hildreth", command=self.marr_hildreth)
        menubar.add_cascade(label="Filtre Passe-haut", menu=ph)

        # ── Morphologie ──
        morph = tk.Menu(menubar, tearoff=0)
        morph.add_command(label="Érosion",    command=self.erosion)
        morph.add_command(label="Dilatation", command=self.dilatation)
        morph.add_command(label="Ouverture",  command=self.ouverture)
        morph.add_command(label="Fermeture",  command=self.fermeture)
        menubar.add_cascade(label="Morphologie", menu=morph)

        self.root.config(menu=menubar)

    def _build_canvas(self):
        frame = tk.Frame(self.root, bg="#2b2b2b")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panneau gauche – image originale
        left = tk.Frame(frame, bg="#2b2b2b")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        tk.Label(left, text="Image originale", bg="#2b2b2b", fg="white",
                 font=("Helvetica", 11, "bold")).pack()
        self.canvas_orig = tk.Label(left, bg="#1a1a1a", relief="sunken",
                                    width=400, height=300)
        self.canvas_orig.pack(fill=tk.BOTH, expand=True)

        # Panneau droit – image filtrée
        right = tk.Frame(frame, bg="#2b2b2b")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        tk.Label(right, text="Image filtrée", bg="#2b2b2b", fg="white",
                 font=("Helvetica", 11, "bold")).pack()
        self.canvas_filt = tk.Label(right, bg="#1a1a1a", relief="sunken",
                                    width=400, height=300)
        self.canvas_filt.pack(fill=tk.BOTH, expand=True)

        self.root.configure(bg="#2b2b2b")

    # ─────────────────────────────────────────────
    # UTILITAIRES
    # ─────────────────────────────────────────────
    def _check_image(self):
        if self.img_original is None:
            messagebox.showerror("Erreur", "Veuillez ouvrir une image d'abord.")
            return False
        return True

    def _to_gray(self, img):
        if len(img.shape) == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    def _show(self, canvas, img_np):
        """Affiche un tableau numpy (uint8 ou float) dans un Label Tkinter."""
        if img_np.dtype != np.uint8:
            # Normalise vers 0-255
            mn, mx = img_np.min(), img_np.max()
            if mx > mn:
                img_np = ((img_np - mn) / (mx - mn) * 255).astype(np.uint8)
            else:
                img_np = img_np.astype(np.uint8)

        if len(img_np.shape) == 2:
            pil_img = Image.fromarray(img_np, mode="L")
        else:
            pil_img = Image.fromarray(cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB))

        w = canvas.winfo_width() or 400
        h = canvas.winfo_height() or 300
        pil_img.thumbnail((w, h), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(pil_img)
        canvas.configure(image=tk_img)
        canvas.image = tk_img  # garde la référence

    def _show_filtered(self, img_np):
        self._show(self.canvas_filt, img_np)

    # ─────────────────────────────────────────────
    # FICHIER
    # ─────────────────────────────────────────────
    def ouvrir(self):
        path = filedialog.askopenfilename(
            title="Choisir une image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp"), ("Tous", "*.*")]
        )
        if not path:
            return
        img = cv2.imread(path)
        if img is None:
            messagebox.showerror("Erreur", "Impossible de lire l'image.")
            return
        self.img_original = img
        self._show(self.canvas_orig, img)

    def enregistrer(self):
        if not self._check_image():
            return
        path = filedialog.asksaveasfilename(
            title="Enregistrer l'image",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
        )
        if not path:
            return
        cv2.imwrite(path, self.img_original)

    # ─────────────────────────────────────────────
    # OPÉRATIONS PONCTUELLES
    # ─────────────────────────────────────────────
    def contraste(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original).astype(np.float64)
        # imadjust équivalent : étirement de l'histogramme
        p2, p98 = np.percentile(gray, (2, 98))
        result = np.clip((gray - p2) / (p98 - p2 + 1e-8) * 255, 0, 255).astype(np.uint8)
        self._show_filtered(result)

    def decalage_additif(self):
        if not self._check_image():
            return
        val = simpledialog.askfloat("Décalage Additif", "Valeur de décalage :")
        if val is None:
            return
        img = self.img_original.astype(np.float64) + val
        img = np.clip(img, 0, 255).astype(np.uint8)
        self._show_filtered(img)

    def mise_echelle(self):
        if not self._check_image():
            return
        val = simpledialog.askfloat("Mise à l'échelle", "Facteur :")
        if val is None:
            return
        img = self.img_original.astype(np.float64) * val
        img = np.clip(img, 0, 255).astype(np.uint8)
        self._show_filtered(img)

    def inversion(self):
        if not self._check_image():
            return
        self._show_filtered(cv2.bitwise_not(self.img_original))

    def seuillage(self):
        if not self._check_image():
            return
        seuil = simpledialog.askfloat("Seuillage", "Valeur seuil (0-255) :")
        if seuil is None:
            return
        gray = self._to_gray(self.img_original)
        _, result = cv2.threshold(gray, seuil, 255, cv2.THRESH_BINARY)
        self._show_filtered(result)

    # ─────────────────────────────────────────────
    # BRUIT
    # ─────────────────────────────────────────────
    def bruit_gaussien(self):
        if not self._check_image():
            return
        noise = np.random.normal(0, 25, self.img_original.shape)
        noisy = np.clip(self.img_original.astype(np.float64) + noise, 0, 255).astype(np.uint8)
        self._show_filtered(noisy)

    def bruit_poivre_sel(self):
        if not self._check_image():
            return
        img = self.img_original.copy()
        ratio = 0.05
        nb = int(img.size * ratio)
        # sel
        coords = [np.random.randint(0, d, nb) for d in img.shape[:2]]
        img[coords[0], coords[1]] = 255
        # poivre
        coords = [np.random.randint(0, d, nb) for d in img.shape[:2]]
        img[coords[0], coords[1]] = 0
        self._show_filtered(img)

    # ─────────────────────────────────────────────
    # FILTRES FRÉQUENTIELS
    # ─────────────────────────────────────────────
    def _freq_filter(self, H):
        gray = self._to_gray(self.img_original).astype(np.float64)
        F = np.fft.fft2(gray)
        Fshift = np.fft.fftshift(F)
        G = H * Fshift
        g = np.real(np.fft.ifft2(np.fft.ifftshift(G)))
        return g

    def _make_grid(self, shape):
        M, N = shape
        u = np.arange(-N // 2, N // 2)
        v = np.arange(-M // 2, M // 2)
        V, U = np.meshgrid(v, u, indexing='ij')
        return np.sqrt(U ** 2 + V ** 2)

    def filtre_passe_bas(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original)
        D = self._make_grid(gray.shape)
        H = (D <= 50).astype(float)
        self._show_filtered(self._freq_filter(H))

    def filtre_passe_haut(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original)
        D = self._make_grid(gray.shape)
        H = (D > 30).astype(float)
        self._show_filtered(self._freq_filter(H))

    def filtre_passe_bande(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original)
        D = self._make_grid(gray.shape)
        H = ((D >= 20) & (D <= 60)).astype(float)
        self._show_filtered(self._freq_filter(H))

    def rehaussement_hf(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original)
        D = self._make_grid(gray.shape)
        Hlp = (D <= 30).astype(float)
        H = 1 - Hlp
        k = 1.5
        F = np.fft.fft2(gray.astype(np.float64))
        Fshift = np.fft.fftshift(F)
        G = (1 + k * H) * Fshift
        g = np.real(np.fft.ifft2(np.fft.ifftshift(G)))
        self._show_filtered(g)

    # ─────────────────────────────────────────────
    # FILTRES LINÉAIRES (PASSE-BAS SPATIAL)
    # ─────────────────────────────────────────────
    def _apply_kernel(self, kernel):
        img = self.img_original
        if len(img.shape) == 3:
            channels = [convolve(img[:, :, c].astype(float), kernel) for c in range(3)]
            result = np.stack(channels, axis=2)
        else:
            result = convolve(img.astype(float), kernel)
        return np.clip(result, 0, 255).astype(np.uint8)

    def _gaussian_kernel(self, size, sigma):
        ax = np.arange(-(size // 2), size // 2 + 1)
        xx, yy = np.meshgrid(ax, ax)
        k = np.exp(-(xx ** 2 + yy ** 2) / (2 * sigma ** 2))
        return k / k.sum()

    def moyenneur3(self):
        if not self._check_image():
            return
        self._show_filtered(self._apply_kernel(np.ones((3, 3)) / 9))

    def moyenneur5(self):
        if not self._check_image():
            return
        self._show_filtered(self._apply_kernel(np.ones((5, 5)) / 25))

    def gaussien3(self):
        if not self._check_image():
            return
        self._show_filtered(self._apply_kernel(self._gaussian_kernel(3, 0.5)))

    def gaussien5(self):
        if not self._check_image():
            return
        self._show_filtered(self._apply_kernel(self._gaussian_kernel(5, 1.0)))

    def pyramidal(self):
        if not self._check_image():
            return
        h = np.array([[1, 2, 1],
                      [2, 4, 2],
                      [1, 2, 1]], dtype=float) / 16
        self._show_filtered(self._apply_kernel(h))

    def conique(self):
        if not self._check_image():
            return
        h = np.array([[0, 1, 0],
                      [1, 4, 1],
                      [0, 1, 0]], dtype=float) / 8
        self._show_filtered(self._apply_kernel(h))

    # ─────────────────────────────────────────────
    # FILTRE NON LINÉAIRE
    # ─────────────────────────────────────────────
    def median(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original)
        result = median_filter(gray, size=3)
        self._show_filtered(result)

    # ─────────────────────────────────────────────
    # FILTRES PASSE-HAUT / DÉTECTION DE CONTOURS
    # ─────────────────────────────────────────────
    def gradient(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original).astype(np.float64)
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
        mag = np.sqrt(gx ** 2 + gy ** 2)
        self._show_filtered(mag)

    def sobel(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original)
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        result = cv2.magnitude(gx, gy)
        self._show_filtered(result)

    def prewitt(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original).astype(np.float64)
        kx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
        ky = kx.T
        gx = convolve(gray, kx)
        gy = convolve(gray, ky)
        result = np.sqrt(gx ** 2 + gy ** 2)
        self._show_filtered(result)

    def robert(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original).astype(np.float64)
        kx = np.array([[1, 0], [0, -1]], dtype=float)
        ky = np.array([[0, 1], [-1, 0]], dtype=float)
        gx = convolve(gray, kx)
        gy = convolve(gray, ky)
        result = np.sqrt(gx ** 2 + gy ** 2)
        self._show_filtered(result)

    def laplacien(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original)
        result = cv2.Laplacian(gray, cv2.CV_64F)
        self._show_filtered(result)

    def canny(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original)
        result = cv2.Canny(gray, 100, 200)
        self._show_filtered(result)

    def kirsch(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original).astype(np.float64)
        h = np.array([[5, 5, 5],
                      [-3, 0, -3],
                      [-3, -3, -3]], dtype=float)
        result = convolve(gray, h)
        self._show_filtered(result)

    def marr_hildreth(self):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0.5)
        result = cv2.Laplacian(blurred, cv2.CV_64F)
        self._show_filtered(result)

    # ─────────────────────────────────────────────
    # MORPHOLOGIE
    # ─────────────────────────────────────────────
    def _morph_op(self, op):
        if not self._check_image():
            return
        gray = self._to_gray(self.img_original)
        _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        result = op(bw, se)
        self._show_filtered(result)

    def erosion(self):
        self._morph_op(lambda img, se: cv2.erode(img, se))

    def dilatation(self):
        self._morph_op(lambda img, se: cv2.dilate(img, se))

    def ouverture(self):
        self._morph_op(lambda img, se: cv2.morphologyEx(img, cv2.MORPH_OPEN, se))

    def fermeture(self):
        self._morph_op(lambda img, se: cv2.morphologyEx(img, cv2.MORPH_CLOSE, se))


# ─────────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = App1(root)
    root.mainloop()
