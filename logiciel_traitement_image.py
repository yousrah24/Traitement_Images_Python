## Partie 1 : implementation filtres
from PIL import Image

## fct qui renvoie une image où les pixels sont négatif donc inverser
def invpixel_gray(pix):
    return 255 - pix
def invpixel_rgb(pix):
    return (255-pix[0],255-pix[1],255-pix[2])
def inversion(im1):
    im2 = im1.copy()
    (w,h)=im1.size
    pim1 = im1.load()
    pim2 = im2.load()
    if im1.mode == 'L':
        invpixel = invpixel_gray
    else:
        invpixel = invpixel_rgb
    for x in range(w):
        for y in range(h):
            pix= pim1[x,y]
            pim2[x,y]=invpixel(pix)
    return im2

## fct qui renvoie une image flouter
def floutage(im1):
    (w, h) = im1.size
    im2 = im1.copy()
    pim1=im1.load()
    for x in range(1,w-1):
        for y in range(1,h-1):
            ## on prends la moyenne des pixels voisins (x-1,y-1) et (x+1,y+1),
            ## pour les mettre aux pixels courant (x,y)
            pixvoisin=(pim1[x-1,y-1][0]+pim1[x+1,y+1][0]//2,
                       pim1[x-1,y-1][1]+pim1[x+1,y+1][1]//2,
                       pim1[x-1,y-1][2]+pim1[x+1,y+1][2]//2)
            im2.putpixel((x,y),pixvoisin)
    return im2

## fct qui renvoie une image gris à partir d'une image courante
def teintGris(im1):
    (w, h) = im1.size
    im2 = im1.copy()
    pim1=im1.load()
    pim2=im2.load()
    for x in range(w):
        for y in range(h):
            # prend la moyenne des pixels pour les mettre dans chaque pixels
            (r,g,b)=pim1[x,y]
            m=(r+g+b)//3
            pim2[x,y]=(m,m,m)
    return im2
## fct qui renvoie une image rouge
def teintRouge(im1):
    (w, h) = im1.size
    im2 = im1.copy()
    pim1=im1.load()
    pim2=im2.load()
    for x in range(w):
        for y in range(h):
            (r,g,b)=pim1[x,y]
            pim2[x,y]=(0,g,b)
    return im2

## fct qui renvoie une image tourner vers le bas
def flipHorizontale(im1):
    pim1 = im1.load()
    (w, h) = im1.size
    im2 = im1.copy()
    pim2 = im2.load()
    all_pixels = []
    for x in range(w):
       for y in range(h):
           cpixel = pim1[x, y]
           all_pixels.append(cpixel)
    for x in range(w):
       for y in range(h):
           pim2[x,y]=all_pixels.pop()
    return im2

## fct qui renvoie une image en miroir
def flipVerticale(im1):
    pim1 = im1.load()
    (w, h) = im1.size
    im2 = im1.copy()
    pim2 = im2.load()
    for y in range(h):
       for x in range(w):
           pix=pim1[x,y]
           im2.putpixel((w-x-1,y),pix)
    return im2

"""
im1=Image.open("oiseau.png")
im1.show()

im2=floutage(im1)
im2.show()
"""

## Partie 2 : Interface grafique Tkinter

import tkinter as tk
from tkinter.filedialog import*
from PIL import Image
from PIL import ImageTk

# variables globale
image_gauche=None
image_droite=None
temp=None
# Elements de l'interface
dict_tkinter = {"img_g": None, "img_d": None, "id_img_g": None, 
                "id_img_d": None, "canvas_g": None, "canvas_d": None}

# Fonctions utilitaires
def update_pictures():
    """
    Cette procédure doit être appelée après toute modification de image_gauche
    ou image_droite.
    Elle a pour effet de :
      - convertir les 2 images (sauf si à None) en images tkinter
      - effacer les images éventuellement présentes dans les canvas
      - afficher à leur place les 2 images tkinter (en gardant une référence
        dans dict_tkinter)
    """
    if dict_tkinter["img_g"] is not None:
        dict_tkinter["canvas_g"].delete(dict_tkinter["img_g"])
        dict_tkinter["img_g"] = None

    if dict_tkinter["img_d"] is not None:
        dict_tkinter["canvas_d"].delete(dict_tkinter["img_d"])
        dict_tkinter["img_d"] = None

    if image_gauche is not None:
        dict_tkinter["img_g"] = ImageTk.PhotoImage(image=image_gauche)
        dict_tkinter["id_img_g"] = dict_tkinter["canvas_g"].create_image(0, 0, image=dict_tkinter["img_g"], anchor=tk.NW)

    if image_droite is not None:
        dict_tkinter["img_d"] = ImageTk.PhotoImage(image=image_droite)
        dict_tkinter["id_img_d"] = dict_tkinter["canvas_d"].create_image(0, 0, image=dict_tkinter["img_d"], anchor=tk.NW)

def open_file():
    """
    Procédure qui ouvre un sélecteur de fichier.
    L'utilisateur choisit une image : elle devient
    l'image de gauche de l'interface
    """
    global image_gauche,temp
    filename = askopenfilename(parent=root)
    img = Image.open(filename)
    image_gauche = img.copy()
    temp = img.copy()
    update_pictures()
    
def croiser():
    """
    Procédure qui croise les images : l'image gauche devient
    l'image de droite de l'interface
    """
    global image_gauche
    image_gauche=image_droite
    update_pictures()
    
def actualiser():
    """
    Procédure qui permet de remettre l'image de gauche initial aprés le croisement
    """
    global image_gauche
    image_gauche=temp
    update_pictures()
    

    
       
"""
    Procédure appliquant les filtres à l'image de gauche
"""

def reverse():
    global image_droite
    image_droite=inversion(image_gauche)
    update_pictures()

def flou():
    global image_droite
    image_droite=floutage(image_gauche)
    update_pictures()

def gris():
    global image_droite
    image_droite=teintGris(image_gauche)
    update_pictures()
    
def miroir():
    global image_droite
    image_droite=flipVerticale(image_gauche)
    update_pictures()
    
def bas():
    global image_droite
    image_droite=flipHorizontale(image_gauche)
    update_pictures()
    

def creation_interface(root):
    """
    Cette procédure place les éléménts de l'interface, 
    et leur associe des actions
    """
    root.title("Traitement images")
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=1)
    
    ## fenetre où va contenir l'image gauche
    dict_tkinter["canvas_g"] = tk.Canvas(frame,width=256, height=400, background="grey")
    dict_tkinter["canvas_g"].pack(padx=8, pady=8, side=tk.LEFT, fill=tk.BOTH, expand=1)
    
    ## fenetre où va contenir l'image droit
    panneau_boutons = tk.Frame(frame, background="yellow")
    panneau_boutons.pack(side=tk.LEFT, fill=tk.X, expand=0)
    
    ## fenetre où va contenir l'image droit
    dict_tkinter["canvas_d"] = tk.Canvas(frame, width=256, height=400, background="grey")
    dict_tkinter["canvas_d"].pack(padx=8, pady=8, side=tk.LEFT, fill=tk.BOTH, expand=1)
    
    ## Implémentation des boutons
    btn = tk.Button(panneau_boutons, text="Ouvrir", command=open_file)
    btn.pack(fill=tk.X, expand=1)
    
    btn = tk.Button(panneau_boutons, text="<--", command=croiser)
    btn.pack(fill=tk.X, expand=1)
    
    btn = tk.Button(panneau_boutons, text="Actualiser", command=actualiser)
    btn.pack(fill=tk.X, expand=1)
    
    btn = tk.Button(panneau_boutons, text="Gris", command=gris)
    btn.pack(fill=tk.X, expand=1)
    
    btn = tk.Button(panneau_boutons, text="Reverse", command=reverse)
    btn.pack(fill=tk.X, expand=1)
    
    btn = tk.Button(panneau_boutons, text="Flou", command=flou)
    btn.pack(fill=tk.X, expand=1)

    btn = tk.Button(panneau_boutons, text="Miroir", command=miroir)
    btn.pack(fill=tk.X, expand=1)

    btn = tk.Button(panneau_boutons, text="Tourner", command=bas)
    btn.pack(fill=tk.X, expand=1)
    
## Main
root = tk.Tk()
creation_interface(root)
root.mainloop()
 

    




    
    


