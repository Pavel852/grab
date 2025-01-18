======================================
 SCRAPER PRO WEB FIRMY.CZ
======================================

Popis (Česky):
----------------
Tento projekt slouží k prohledávání stránek www.firmy.cz a vyhledání
odkazů na detaily firem podle zadané kategorie (např. "Velkoobchod a výroba"),
případně pro parsování samotné stránky s detailem firmy, odkud se
získají údaje (jméno, adresa, e-mail, telefon atd.).

Soubory:
  - index.php   ... Hlavní "router" – podle action=find/parse volá find.php nebo parse.php
  - find.php    ... Hledá detailní odkazy (https://www.firmy.cz/detail/*)
  - parse.php   ... Z jedné detailní URL vyparsuje jméno, adresu, web atd.
  - composer.json, vendor/ ... Knihovny (Guzzle, DomCrawler) instalované přes Composer

Použití:
  1) Nahrajte všechny zmíněné soubory na server, včetně "vendor/" (Composer).
  2) V prohlížeči otevřete:
       index.php?action=find&startUrl=...
     nebo
       index.php?action=parse&detailUrl=...
  3) Skript vrací JSON výstup.

Poznámka:
  Pokud se další stránky načítají JavaScriptem, je nutné místo Guzzle+DomCrawler
  použít headless browser (např. Selenium, Panther, Playwright).

Description (EN):
-----------------
This project is a simple scraper for www.firmy.cz pages. It can:
 - Find all detail links in a category listing ("Velkoobchod a výroba" etc.).
 - Parse specific detail pages to extract name, address, phone, email, etc.
 
Files:
 - index.php  ... router for ?action=find or ?action=parse
 - find.php   ... collects all detail links from listing pages
 - parse.php  ... parse a single detail page
 - composer.json, vendor/... composer libraries for Guzzle + DomCrawler

Usage:
  1) Upload these files to your PHP server (with composer libraries).
  2) Access in browser:
       index.php?action=find&startUrl=...
       index.php?action=parse&detailUrl=...
  3) Output is in JSON format.

Note:
 If the site is loaded mostly by JavaScript, you will need a headless browser
 approach instead of Guzzle+DomCrawler.

--------------------------------------
 LICENCE - Creative Commons (CC BY 4.0)
--------------------------------------
Tento projekt je dostupný pod licencí Creative Commons Attribution 4.0 International (CC BY 4.0).
Můžete jej libovolně sdílet, upravovat a používat i komerčně za podmínky, že zachováte autorství
a uvedete odkaz na tuto licenci.

Více informací o licenci:
  https://creativecommons.org/licenses/by/4.0/

English summary of CC BY 4.0:
You are free to:
  - Share, copy and redistribute the material in any medium or format
  - Adapt, remix, transform, build upon the material for any purpose, 
    even commercially
Under the following terms:
  - Attribution: You must give appropriate credit, provide a link 
    to the license, and indicate if changes were made.

(c) 2025 Váš Autorský Tým
