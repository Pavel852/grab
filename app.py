import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import configparser
import requests
import csv
import os
import webbrowser  # pro otevírání odkazů v prohlížeči

class SettingsWindow(tk.Toplevel):
    """Okno pro nastavení URL 'urlengine'."""
    def __init__(self, parent, config, config_file, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Nastavení")
        self.config_parser = config
        self.config_file = config_file
        
        # Orámování vnitřního obsahu
        main_frame = ttk.Frame(self, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label + Entry pro urlengine
        ttk.Label(main_frame, text="URL engine:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.urlengine_var = tk.StringVar(value=self.config_parser["DEFAULT"].get("urlengine", ""))
        ttk.Entry(main_frame, textvariable=self.urlengine_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        
        # Tlačítka Uložit a Zavřít
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        save_btn = ttk.Button(btn_frame, text="Uložit", command=self.save_settings)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = ttk.Button(btn_frame, text="Zavřít", command=self.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)
        
        self.resizable(False, False)
        self.grab_set()  # Okno je modální (blokuje zbytek GUI)

    def save_settings(self):
        """Uložení nastavení do INI souboru."""
        new_value = self.urlengine_var.get().strip()
        if not new_value:
            messagebox.showwarning("Varování", "URL engine nemůže být prázdné!")
            return
        self.config_parser["DEFAULT"]["urlengine"] = new_value
        
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.config_parser.write(f)
        
        messagebox.showinfo("Uloženo", "Nastavení bylo uloženo.")
        self.destroy()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grabber")
        self.geometry("1000x600")

        # Nastavíme styl, aby to vypadalo více "user friendly"
        style = ttk.Style(self)
        style.theme_use("clam")

        # Čtení configu
        self.config_file = "settings.ini"
        self.config_parser = configparser.ConfigParser()
        
        if os.path.exists(self.config_file):
            self.config_parser.read(self.config_file, encoding="utf-8")
        else:
            # Pokud neexistuje, vytvoříme s výchozím nastavením
            self.config_parser["DEFAULT"] = {"urlengine": "https://prace.estudium.eu/app/test/"}
            with open(self.config_file, "w", encoding="utf-8") as f:
                self.config_parser.write(f)
        
        # Menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menu "Soubor"
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nastavení", command=self.on_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Ukončit", command=self.quit)
        menubar.add_cascade(label="Soubor", menu=file_menu)

        # Menu "Nápověda"
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Nápověda", command=self.on_help)
        help_menu.add_command(label="O programu", command=self.on_about)
        menubar.add_cascade(label="Nápověda", menu=help_menu)

        # Notebook (záložky)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Záložka 1
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Záložka 1 (Links)")

        # Záložka 2
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Záložka 2 (Detaily)")

        # Vytvoření obsahu záložky 1
        self.create_tab1()
        
        # Vytvoření obsahu záložky 2
        self.create_tab2()
        
        # Ukládání odkazů (z tab1) a detailů (z tab2)
        self.link_data = []
        self.detail_data = []

        # Pro postupné grabování
        self.link_index = 0
        self.stop_flag = False  # příznak pro zastavení

        # Status bar ve spodní části okna (počet řádků)
        self.status_label = ttk.Label(self, text="Počet řádků: 0", anchor="w")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Po vytvoření tabulek (viz create_tab1, create_tab2) přidáme SHIFT+šipky
        self.enable_shift_arrow_select(self.tree_links)
        self.enable_shift_arrow_select(self.tree_details)

    # -------------------------------------------------------------------------
    # Oprava: dříve se jmenovalo open_settings => nyní on_settings
    # -------------------------------------------------------------------------
    def on_settings(self):
        """Otevře okno nastavení."""
        SettingsWindow(self, self.config_parser, self.config_file)

    # -------------------------------------------------------------------------
    # Nápověda a O programu s proklikávacími odkazy
    # -------------------------------------------------------------------------
    def on_help(self):
        help_text = (
            "Tento program je určen k hromadnému sběru (scrapování) odkazů a následně detailů "
            "firem z portálu https://www.firmy.cz. \n"
            "Postup:\n"
            "  1) V záložce 1 (Links) klikněte na 'Start' a zadejte URL (např. https://www.firmy.cz/Velkoobchod-a-vyroba).\n"
            "     Program přes API (urlengine v settings.ini) načte odkazy a zobrazí je.\n"
            "  2) V záložce 2 (Detaily) klikněte na 'Grab detaily' a postupně se načtou detailní informace ke každé firmě.\n"
            "  3) Data pak můžete exportovat do CSV.\n\n"
            "V menu 'Soubor > Nastavení' lze měnit URL engine.\n"
            "Shift + Šipka nahoru/dolů: multi-select. Klávesou Del mažete vybrané řádky.\n"
        )
        messagebox.showinfo("Nápověda", help_text)

    def on_about(self):
        """Vlastní okno s textem (klikací odkazy, licence CC)."""
        about_win = tk.Toplevel(self)
        about_win.title("O programu")
        about_win.geometry("550x300")
        
        # Přidáme Text, do kterého vložíme info s odkazem
        txt = tk.Text(about_win, wrap="word")
        txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Nastavení stylů pro odkazy
        txt.tag_config("link", foreground="blue", underline=True)
        
        def callback_orcid(event):
            webbrowser.open_new("https://orcid.org/0009-0001-3558-4312")
        def callback_github(event):
            webbrowser.open_new("https://github.com/Pavel852")

        # Vložení textu
        txt.insert(tk.END, "Autor: PB\n")
        txt.insert(tk.END, "Email: pavel.bartos.pb@gmail.com\n")
        txt.insert(tk.END, "Verze: 1.8\n")
        txt.insert(tk.END, "Rok vytvoření: 2/2025\n")
        txt.insert(tk.END, "Licencováno pod Creative Commons (CC)\n\n")
        txt.insert(tk.END, "ORCID: ")
        # Klikací odkaz - orcid
        txt.insert(tk.END, "https://orcid.org/0009-0001-3558-4312", "link_orcid")
        txt.insert(tk.END, "\nGitHub: ")
        # Klikací odkaz - github
        txt.insert(tk.END, "https://github.com/Pavel852", "link_github")
        
        # Nastavení tagů
        txt.tag_config("link_orcid", foreground="blue", underline=True)
        txt.tag_bind("link_orcid", "<Button-1>", callback_orcid)
        
        txt.tag_config("link_github", foreground="blue", underline=True)
        txt.tag_bind("link_github", "<Button-1>", callback_github)
        
        # Vypneme editaci textu
        txt.config(state="disabled")

    # -------------------------------------------------------------------------
    # Multi-select (SHIFT + šipky)
    # -------------------------------------------------------------------------
    def enable_shift_arrow_select(self, tree: ttk.Treeview):
        """
        Přidá podporu pro SHIFT + šipka nahoru/dolů pro rozšíření výběru položek.
        """
        tree.last_focus_item = None

        def on_tree_click(event):
            """Zapamatuje si kliknutý řádek jako 'last_focus_item'."""
            row_id = tree.identify_row(event.y)
            if row_id:
                tree.last_focus_item = row_id
            else:
                tree.last_focus_item = None

        def on_tree_key(event):
            """
            Při stisku SHIFT + šipka nahoru/dolů vybere rozsah řádků od 'last_focus_item' po nový.
            """
            if event.keysym not in ("Up", "Down"):
                return

            SHIFT_MASK = 0x0001  # Bitmask SHIFT
            if not (event.state & SHIFT_MASK):
                # SHIFT není zmáčknutý
                focus_item = tree.focus()
                if focus_item:
                    tree.last_focus_item = focus_item
                return

            items = tree.get_children()
            if not items:
                return

            focus_item = tree.focus()
            if not focus_item:
                # Pokud ještě žádný focus nebyl, bereme první
                focus_item = items[0]

            old_index = items.index(focus_item)

            if event.keysym == "Up":
                new_index = max(0, old_index - 1)
            else:  # Down
                new_index = min(len(items) - 1, old_index + 1)

            new_focus_item = items[new_index]

            if tree.last_focus_item is None:
                tree.last_focus_item = focus_item

            last_index = items.index(tree.last_focus_item)

            start = min(last_index, new_index)
            end = max(last_index, new_index)

            tree.selection_set(items[start:end+1])

            tree.focus(new_focus_item)
            tree.see(new_focus_item)
            return "break"

        tree.bind("<Button-1>", on_tree_click, True)
        tree.bind("<Up>", on_tree_key, True)
        tree.bind("<Down>", on_tree_key, True)

    # -------------------------------------------------------------------------
    # Tvorba záložek (GUI)
    # -------------------------------------------------------------------------
    def create_tab1(self):
        frame = ttk.Frame(self.tab1, padding="10 10 10 10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Vyhledání odkazů (akce find)").pack(pady=5, anchor="w")

        # Rámeček pro tlačítka Start, Export, Nastavení (vedle sebe)
        btn_frame_tab1 = ttk.Frame(frame)
        btn_frame_tab1.pack(pady=5, anchor="w")

        # Tlačítko Start
        start_btn = ttk.Button(btn_frame_tab1, text="Start", command=self.on_start)
        start_btn.pack(side=tk.LEFT, padx=5)

        # Tlačítko Export - vedle Startu
        export_btn_tab1 = ttk.Button(btn_frame_tab1, text="Export (CSV)", command=self.on_export_links)
        export_btn_tab1.pack(side=tk.LEFT, padx=5)

        # Tlačítko Nastavení
        settings_btn = ttk.Button(btn_frame_tab1, text="Nastavení", command=self.on_settings)
        settings_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview - tabulka pro zobrazení odkazů (multi-select)
        columns = ("link",)
        self.tree_links = ttk.Treeview(frame, columns=columns, show="headings", height=15, selectmode="extended")
        self.tree_links.heading("link", text="Odkaz")
        self.tree_links.column("link", width=850)  # Šířka sloupce
        
        # Vertikální Scrollbar
        scroll_links = ttk.Scrollbar(frame, orient="vertical", command=self.tree_links.yview)
        self.tree_links.configure(yscroll=scroll_links.set)
        
        # Umístění Treeview a scrollbar vedle sebe
        self.tree_links.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_links.pack(side=tk.LEFT, fill=tk.Y, padx=2)

        # Bind pro smazání vybraného řádku klávesou Delete
        self.tree_links.bind("<Delete>", self.on_delete_link_row)

    def create_tab2(self):
        frame = ttk.Frame(self.tab2, padding="10 10 10 10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Postupné načítání detailů (akce parse)").pack(pady=5, anchor="w")

        # Rámeček pro tlačítka Grab, STOP, Export (vedle sebe)
        btn_frame_tab2 = ttk.Frame(frame)
        btn_frame_tab2.pack(pady=5, anchor="w")

        self.grab_btn = ttk.Button(btn_frame_tab2, text="Grab detaily", command=self.on_grab_details)
        self.grab_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame_tab2, text="STOP", command=self.on_stop_details, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = ttk.Button(btn_frame_tab2, text="Export detailů (CSV)", command=self.on_export_csv)
        self.export_btn.pack(side=tk.LEFT, padx=5)

        # Label pro zobrazení stavu (kolik firem bylo načteno apod.)
        self.progress_label = ttk.Label(frame, text="")
        self.progress_label.pack(pady=5, anchor="w")
        
        # Treeview - tabulka pro zobrazení detailů (multi-select)
        # První sloupec = "row_no" (#), potom ostatní
        self.detail_columns = ("row_no", "name", "description", "web", "tel", "email", "address", "zip", "city", "country")
        self.tree_details = ttk.Treeview(frame, columns=self.detail_columns, show="headings", height=15, selectmode="extended")
        
        # Sloupec # (row_no)
        self.tree_details.heading("row_no", text="#")
        self.tree_details.column("row_no", width=40, anchor="center")

        self.tree_details.heading("name", text="Název")
        self.tree_details.heading("description", text="Popis")
        self.tree_details.heading("web", text="Web")
        self.tree_details.heading("tel", text="Telefon")
        self.tree_details.heading("email", text="Email")
        self.tree_details.heading("address", text="Adresa")
        self.tree_details.heading("zip", text="PSČ")
        self.tree_details.heading("city", text="Město")
        self.tree_details.heading("country", text="Země")

        # Upravíme šířky některých sloupců
        self.tree_details.column("name", width=120)
        self.tree_details.column("description", width=220)
        self.tree_details.column("web", width=100)
        self.tree_details.column("tel", width=100)
        self.tree_details.column("email", width=120)
        self.tree_details.column("address", width=180)
        self.tree_details.column("zip", width=60)
        self.tree_details.column("city", width=100)
        self.tree_details.column("country", width=80)

        # Vertikální Scrollbar (záložka 2)
        scroll_details = ttk.Scrollbar(frame, orient="vertical", command=self.tree_details.yview)
        self.tree_details.configure(yscroll=scroll_details.set)

        # Umístění
        self.tree_details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_details.pack(side=tk.LEFT, fill=tk.Y, padx=2)

        # Bind pro smazání vybraného řádku klávesou Delete
        self.tree_details.bind("<Delete>", self.on_delete_detail_row)

    # -------------------------------------------------------------------------
    # Pomocná funkce - aktualizace status_label
    # -------------------------------------------------------------------------
    def update_status_label(self):
        """Zobrazí počet řádků v tabulce aktuálně vybrané záložky."""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            # Záložka 1
            row_count = len(self.tree_links.get_children())
            self.status_label.config(text=f"Počet řádků (Záložka 1): {row_count}")
        else:
            # Záložka 2
            row_count = len(self.tree_details.get_children())
            self.status_label.config(text=f"Počet řádků (Záložka 2): {row_count}")

    # -------------------------------------------------------------------------
    # Záložka 1 - Logika (Links)
    # -------------------------------------------------------------------------
    def on_start(self):
        """Po kliknutí na tlačítko 'Start' na záložce 1.
           Zeptá se uživatele na URL, zavolá akci 'find' a zobrazí odkazy."""
        url = tk.simpledialog.askstring("Vstup", "Zadejte adresu ke grabování (např. https://www.firmy.cz/Velkoobchod-a-vyroba):")
        if not url:
            return
        
        base_engine = self.config_parser["DEFAULT"].get("urlengine", "").strip()
        if not base_engine:
            messagebox.showerror("Chyba", "Nebyl nalezen urlengine v nastavení.")
            return
        
        find_url = f"{base_engine}?action=find&startUrl={url}"
        
        try:
            resp = requests.get(find_url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            links = data.get("links", [])
            self.link_data = links  # uložíme do paměti
            
            # Vyčištění treeview
            for i in self.tree_links.get_children():
                self.tree_links.delete(i)
            
            # Naplnění tabulky
            for link in links:
                self.tree_links.insert("", tk.END, values=(link,))
            
            # Po naplnění aktualizujeme status
            self.update_status_label()

            messagebox.showinfo("Info", f"Nalezeno odkazů: {len(links)}")
        
        except Exception as e:
            messagebox.showerror("Chyba", f"Nastala chyba při volání API:\n{e}")

    def on_export_links(self):
        """Exportuje data z první záložky (seznam odkazů) do CSV."""
        if not self.link_data:
            messagebox.showwarning("Upozornění", "Žádné odkazy k exportu.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV soubor", "*.csv")],
            title="Uložit CSV (odkazy)"
        )
        if not filename:
            return
        
        try:
            with open(filename, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                # Zápis hlavičky
                writer.writerow(["link"])
                # Zápis obsahu
                for link in self.link_data:
                    writer.writerow([link])
            
            messagebox.showinfo("Hotovo", f"Odkazy byly exportovány do souboru: {filename}")
        except Exception as e:
            messagebox.showerror("Chyba", f"Nastala chyba při exportu CSV:\n{e}")

    def on_delete_link_row(self, event):
        """Smazání vybraného/ých řádku/ů (odkazů) v záložce 1 po stisku klávesy Delete."""
        selected_items = self.tree_links.selection()
        if not selected_items:
            return
        for item_id in selected_items:
            self.tree_links.delete(item_id)
        # Po smazání aktualizujeme status
        self.update_status_label()

    # -------------------------------------------------------------------------
    # Záložka 2 - Logika (Detaily)
    # -------------------------------------------------------------------------
    def on_grab_details(self):
        """Spustí postupné načítání detailů z link_data."""
        if not self.link_data:
            messagebox.showwarning("Upozornění", "V záložce 1 nejsou žádné odkazy.")
            return
        
        # Příprava
        self.link_index = 0
        self.detail_data = []
        self.stop_flag = False  # reset stop příznaku
        
        # Vyčištění tree_details
        for i in self.tree_details.get_children():
            self.tree_details.delete(i)

        # Zablokujeme tlačítko Grab a povolíme STOP
        self.grab_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        self.progress_label.config(text="")
        self.update_status_label()

        # Spustíme cyklus
        self.grab_next_link()

    def on_stop_details(self):
        """Požadavek na zastavení grabování."""
        self.stop_flag = True
        self.progress_label.config(text="Zastavuji ... (počkáme na probíhající request)")

    def grab_next_link(self):
        """
        Načte detail pro link s indexem self.link_index a pak se zavolá znovu,
        dokud nejsou hotové všechny odkazy nebo nepřišel příkaz STOP.
        """
        if self.stop_flag:
            self.finish_grabbing("Grabování zastaveno uživatelem.")
            return

        if self.link_index >= len(self.link_data):
            self.finish_grabbing(f"Načteny všechny firmy ({len(self.detail_data)})")
            return

        base_engine = self.config_parser["DEFAULT"].get("urlengine", "").strip()
        if not base_engine:
            messagebox.showerror("Chyba", "Nebyl nalezen urlengine v nastavení.")
            self.finish_grabbing("Chyba: Chybí URL engine.")
            return
        
        link = self.link_data[self.link_index]
        parse_url = f"{base_engine}?action=parse&detailUrl={link}"
        
        try:
            resp = requests.get(parse_url, timeout=10)
            resp.raise_for_status()
            detail = resp.json()

            # Uložíme do detail_data
            self.detail_data.append(detail)

            # Sloupec # = pořadové číslo = počet řádků + 1
            row_no = len(self.tree_details.get_children()) + 1

            # Vložíme do TreeView (hned, aby bylo vidět řádek po řádku)
            row_values = (
                row_no,
                detail.get("name", ""),
                detail.get("description", ""),
                detail.get("web", ""),
                detail.get("tel", ""),
                detail.get("email", ""),
                detail.get("address", ""),
                detail.get("zip", ""),
                detail.get("city", ""),
                detail.get("country", ""),
            )
            self.tree_details.insert("", tk.END, values=row_values)
            
            # Aktualizace info labelu
            self.progress_label.config(text=f"Načítám firmu {self.link_index + 1}/{len(self.link_data)}")
            self.update_status_label()
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba při grabování detailu:\n{e}")
            # Pokračujeme

        self.link_index += 1
        self.after(200, self.grab_next_link)

    def finish_grabbing(self, msg):
        """Ukončí grabovací proces, obnoví tlačítka apod."""
        self.grab_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_label.config(text=msg)
        self.update_status_label()
        if "zastaveno" not in msg.lower():
            # Pokud to není STOP, zobrazíme info
            messagebox.showinfo("Hotovo", msg)

    def on_delete_detail_row(self, event):
        """Smazání vybraného/ých řádku/ů v záložce 2 (detaily) po stisku klávesy Delete."""
        selected_items = self.tree_details.selection()
        if not selected_items:
            return
        for item_id in selected_items:
            self.tree_details.delete(item_id)
        self.update_status_label()

    def on_export_csv(self):
        """Exportuje data z detailů (záložka 2) do CSV."""
        if not self.detail_data:
            messagebox.showwarning("Upozornění", "Žádná data k exportu (detaily).")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV soubor", "*.csv")],
            title="Uložit CSV (detaily)"
        )
        if not filename:
            return
        
        try:
            with open(filename, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                # Zápis hlavičky
                writer.writerow(["row_no", "name","description","web","tel","email","address","zip","city","country"])
                # Zápis obsahu
                for i, detail in enumerate(self.detail_data, start=1):
                    writer.writerow([
                        i,
                        detail.get("name", ""),
                        detail.get("description", ""),
                        detail.get("web", ""),
                        detail.get("tel", ""),
                        detail.get("email", ""),
                        detail.get("address", ""),
                        detail.get("zip", ""),
                        detail.get("city", ""),
                        detail.get("country", ""),
                    ])
            
            messagebox.showinfo("Hotovo", f"Data byla exportována do souboru: {filename}")
        except Exception as e:
            messagebox.showerror("Chyba", f"Nastala chyba při exportu CSV:\n{e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
