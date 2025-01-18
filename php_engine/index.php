<?php
/**
 * index.php
 *
 * Kontrolní „router“. Podle parametru `action=find` nebo `action=parse`
 * přesměruje na příslušný soubor.
 *
 * - ?action=find&startUrl=...
 * - ?action=parse&detailUrl=...

**Autor:** PB  
**Email:** pavel.bartos.pb@gmail.com  
**Datum:** 2/2025  
**ORCID:** <https://orcid.org/0009-0001-3558-4312>  
**GitHub:** <https://github.com/Pavel852>  
**Licence:** Creative Commons (CC)



 */

$action = isset($_GET['action']) ? $_GET['action'] : null;

if ($action === 'find') {
    // přesměrování na find.php
    require __DIR__ . '/find.php';
    exit;
} elseif ($action === 'parse') {
    require __DIR__ . '/parse.php';
    exit;
} else {
    // Výchozí nápověda (CZ + EN)
    echo <<<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Index | Nastavení</title>
</head>
<body>
<h1>index.php – Zadávání parametrů</h1>
<p>V češtině:</p>
<ul>
  <li>Pro vyhledání detailů (find) použijte např.:</li>
</ul>
<pre>
?action=find&startUrl=https://www.firmy.cz/Velkoobchod-a-vyroba
</pre>

<ul>
  <li>Pro parsování detailu (parse) použijte např.:</li>
</ul>
<pre>
?action=parse&detailUrl=https://www.firmy.cz/detail/xxxxxx-nazev-firmy.html
</pre>

<hr>

<h2>EN – Quick Instructions</h2>
<p>This index.php routes the request based on the <code>action</code> parameter:</p>
<ul>
  <li><strong>?action=find&startUrl=URL</strong> – scans the listing page for detail URLs.</li>
  <li><strong>?action=parse&detailUrl=URL</strong> – parses a single detail page.</li>
</ul>
<pre>
?action=find&startUrl=https://www.firmy.cz/Velkoobchod-a-vyroba
?action=parse&detailUrl=https://www.firmy.cz/detail/xxxxxx-company.html
</pre>
</body>
</html>
HTML;
}
