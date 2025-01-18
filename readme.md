
# Grabber (verze 1.8)

## Popis programu (Česká verze)

Program **Grabber** je webový bot řízený lokální aplikací, který umožňuje hromadné získávání kontaktů z portálu **firmy.cz**. Jeho hlavní funkcí je automatizované scrapování odkazů na firmy a následné načtení detailních informací pomocí přizpůsobitelného API. Program je uživatelsky přívětivý a obsahuje možnosti exportu dat do CSV souborů.

### Jak program funguje

1. **Instalace a spuštění**  
   - Vyžaduje Python 3.  
   - Používá knihovnu `requests` (lze nainstalovat pomocí `pip install requests`).  
   - Program se spouští příkazem `python app.py`.

2. **Nastavení**  
   - Konfigurační soubor `settings.ini` obsahuje klíč `urlengine`, který určuje URL API endpointu.  
   - Nastavení lze změnit v menu aplikace: **Menu > Soubor > Nastavení**.

3. **Funkce programu**  
   - **Záložka 1 (Links):**  
     - Uživatel zadá URL (např. `https://www.firmy.cz/Velkoobchod-a-vyroba`).  
     - Program získá seznam odkazů z API odpovědi.  
     - Data lze exportovat do CSV souboru.  
   - **Záložka 2 (Details):**  
     - Program načítá detailní informace o firmách z odkazů získaných v první záložce.  
     - Uživatel může proces zastavit tlačítkem `STOP`.  
     - Načtená data lze exportovat do CSV.

4. **Ovládání**  
   - **Multi-select:** Uživatel může vybírat více řádků pomocí kláves `Ctrl` nebo `Shift`.
   - **Mazání:** Vybrané řádky lze smazat stiskem klávesy `Delete`.

5. **Poznámky**  
   - Program neukončuje stahování uprostřed probíhajícího požadavku. Tlačítko `STOP` se projeví až po dokončení aktuálního požadavku.  
   - CSV export používá jako oddělovač hodnot středník (`;`).

---

## Program Description (English Version)

The **Grabber** program is a web bot controlled by a local application that enables mass collection of contact information from the **firmy.cz** portal. Its main functionality is automated scraping of company links and subsequent retrieval of detailed information using a customizable API. The program is user-friendly and provides options for exporting data to CSV files.

### How the Program Works

1. **Installation and Launch**  
   - Requires Python 3.  
   - Utilizes the `requests` library (installable via `pip install requests`).  
   - Launch the program using the command `python app.py`.

2. **Configuration**  
   - The configuration file `settings.ini` contains the `urlengine` key, specifying the API endpoint URL.  
   - Settings can be modified through the application menu: **Menu > File > Settings**.

3. **Program Features**  
   - **Tab 1 (Links):**  
     - The user provides a URL (e.g., `https://www.firmy.cz/Velkoobchod-a-vyroba`).  
     - The program fetches a list of links from the API response.  
     - Data can be exported to a CSV file.  
   - **Tab 2 (Details):**  
     - The program retrieves detailed information about companies from the links obtained in the first tab.  
     - Users can stop the process using the `STOP` button.  
     - Retrieved data can be exported to CSV.

4. **Controls**  
   - **Multi-select:** Users can select multiple rows using the `Ctrl` or `Shift` keys.
   - **Deleting:** Selected rows can be deleted using the `Delete` key.

5. **Notes**  
   - The program does not terminate downloading in the middle of a request. The `STOP` button will take effect only after the current request is completed.  
   - CSV export uses a semicolon (`;`) as the value delimiter.

---

**Autor / Author:** PB  
**Email:** pavel.bartos.pb@gmail.com  
**Datum / Date:** 2/2025  
**ORCID:** <https://orcid.org/0009-0001-3558-4312>  
**GitHub:** <https://github.com/Pavel852>  
**Licence / License:** Creative Commons (CC)
