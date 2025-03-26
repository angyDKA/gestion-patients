from tkinter import *
from tkinter import ttk
import mysql.connector as mysc
from tkinter import messagebox

# Connexion à la base de données

def connect_to_db():
    return mysc.connect(host="localhost", user="root", password="", database="hopital")

# Compter les patients pour générer le matricule

def count_patient():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM patients")
        count = cur.fetchone()[0] + 1
        return f"24SJI{count}"
    except:
        return "24SJI1"
    finally:
        cur.close()
        conn.close()

# Fonctions CRUD

def ajouter():
    if not modifier_mode[0]:
        matricule = matricule_var.get()
        nom = nom_entry.get()
        prenom = prenom_entry.get()
        age = age_entry.get()
        adresse = adresse_entry.get()
        telephone = telephone_entry.get()
        remarque = remarque_entry.get()

        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("SELECT matricule FROM patients WHERE matricule=%s", (matricule,))
            if cur.fetchone():
                messagebox.showwarning("Attention", "Ce matricule existe déjà !")
                return
            cur.execute("INSERT INTO patients (matricule, nom, prenom, age, adresse, telephone, remarque) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (matricule, nom, prenom, age, adresse, telephone, remarque))
            conn.commit()
            messagebox.showinfo("Succès", "Patient enregistré avec succès !")
            vider_champs()
            actualiser_liste_patients()
        except mysc.Error as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cur.close()
            conn.close()
    else:
        matricule = matricule_var.get()
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("UPDATE patients SET nom=%s, prenom=%s, age=%s, adresse=%s, telephone=%s, remarque=%s WHERE matricule=%s",
                        (nom_entry.get(), prenom_entry.get(), age_entry.get(), adresse_entry.get(), telephone_entry.get(), remarque_entry.get(), matricule))
            conn.commit()
            messagebox.showinfo("Succès", "Modifications enregistrées avec succès.")
            vider_champs()
            actualiser_liste_patients()
            modifier_mode[0] = False
            for entry in [nom_entry, prenom_entry, age_entry, adresse_entry, telephone_entry, remarque_entry]:
                entry.config(state=DISABLED)
        except mysc.Error as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cur.close()
            conn.close()


def modifier():
    if not matricule_var.get():
        messagebox.showwarning("Alerte", "Veuillez d'abord sélectionner un patient.")
        return
    modifier_mode[0] = True
    for entry in [nom_entry, prenom_entry, age_entry, adresse_entry, telephone_entry, remarque_entry]:
        entry.config(state=NORMAL)
    messagebox.showinfo("Modification", "Vous pouvez maintenant modifier les champs. Cliquez sur 'Enregistrer' pour valider.")


def supprimer():
    if messagebox.askquestion("Confirmation", "Voulez-vous supprimer ce patient ?") == 'yes':
        matricule = matricule_var.get()
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM patients WHERE matricule=%s", (matricule,))
            conn.commit()
            messagebox.showinfo("Succès", "Patient supprimé.")
            vider_champs()
            actualiser_liste_patients()
        except mysc.Error as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cur.close()
            conn.close()

# Vider les champs et générer un nouveau matricule

def vider_champs():
    matricule_var.set(count_patient())
    for entry in [nom_entry, prenom_entry, age_entry, adresse_entry, telephone_entry, remarque_entry]:
        entry.config(state=NORMAL)
        entry.delete(0, END)
        entry.config(state=DISABLED)

# Remplir les champs au clic

def reagir_clic(event):
    selected = tableau.focus()
    if not selected:
        return
    valeurs = tableau.item(selected, 'values')
    matricule_var.set(valeurs[0])
    entries_data = [valeurs[1], valeurs[2], valeurs[3], valeurs[4], valeurs[5], valeurs[6]]
    for entry, value in zip([nom_entry, prenom_entry, age_entry, adresse_entry, telephone_entry, remarque_entry], entries_data):
        entry.config(state=NORMAL)
        entry.delete(0, END)
        entry.insert(0, value)
        entry.config(state=DISABLED)

# Actualiser tableau

def actualiser_liste_patients():
    for i in tableau.get_children():
        tableau.delete(i)
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients")
        for row in cur.fetchall():
            tableau.insert("", END, values=row)
    except:
        pass
    finally:
        cur.close()
        conn.close()

# Interface
root = Tk()
root.title("Gestion des patients - Saint Jean Hôpital")
root.configure(bg='#f7d3e9')

matricule_var = StringVar(value=count_patient())
modifier_mode = [False]

titre = Label(root, text="APPLICATION DE GESTION DES PATIENTS", font=("Helvetica", 18, "bold"), bg='#f7d3e9', fg='#d63384')
titre.grid(row=0, column=0, columnspan=2, pady=20)

form_frame = Frame(root, bg='#f7d3e9')
form_frame.grid(row=1, column=0, padx=20, sticky="n")

Label(form_frame, text="Matricule:", bg='#f7d3e9').grid(row=0, column=0, sticky="w")
matricule_entry = Entry(form_frame, textvariable=matricule_var, state=DISABLED)
matricule_entry.grid(row=0, column=1, pady=5)

labels = ["Nom", "Prénom", "Âge", "Adresse", "Téléphone", "Remarque"]
entries = []
for i, lab in enumerate(labels):
    Label(form_frame, text=f"{lab}:", bg='#f7d3e9').grid(row=i+1, column=0, sticky="w")
    e = Entry(form_frame, state=DISABLED)
    e.grid(row=i+1, column=1, pady=5)
    entries.append(e)

nom_entry, prenom_entry, age_entry, adresse_entry, telephone_entry, remarque_entry = entries

Button(form_frame, text="Enregistrer", command=ajouter, bg='#ff69b4', fg='white').grid(row=7, column=0, pady=10)
Button(form_frame, text="Modifier", command=modifier, bg='#ff69b4', fg='white').grid(row=7, column=1)
Button(form_frame, text="Supprimer", command=supprimer, bg='#ff69b4', fg='white').grid(row=8, column=0, columnspan=2, pady=5)

# Affichage liste patients
liste_frame = Frame(root, bg='#f7d3e9')
liste_frame.grid(row=1, column=1, padx=10)

Label(liste_frame, text="Liste des patients", font=("Helvetica", 14, "bold"), bg='#f7d3e9', fg='#c2185b').pack(pady=5)

scrollbar = Scrollbar(liste_frame)
scrollbar.pack(side=RIGHT, fill=Y)

entetes = ["Matricule", "Nom", "Prénom", "Age", "Adresse", "Téléphone", "Remarque"]
tableau = ttk.Treeview(liste_frame, columns=entetes, show="headings", yscrollcommand=scrollbar.set, height=15)
for col in entetes:
    tableau.heading(col, text=col)
    tableau.column(col, width=100)
tableau.pack()
tableau.bind("<ButtonRelease-1>", reagir_clic)
scrollbar.config(command=tableau.yview)

actualiser_liste_patients()
root.mainloop()