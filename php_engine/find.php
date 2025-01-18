/*

**Autor:** PB  
**Email:** pavel.bartos.pb@gmail.com  
**Datum:** 2/2025  
**ORCID:** <https://orcid.org/0009-0001-3558-4312>  
**GitHub:** <https://github.com/Pavel852>  
**Licence:** Creative Commons (CC)


*/

<?php
ini_set('display_errors','1');
error_reporting(E_ALL);

require __DIR__ . '/vendor/autoload.php'; // Guzzle stačí

use GuzzleHttp\Client;

$startUrl = $_GET['startUrl'] ?? '';
if(!$startUrl) die("Chybí 'startUrl'");

$client = new Client(['timeout'=>10]);

function fetchHtml($url, Client $client) {
    return (string) $client->get($url)->getBody();
}

function findDetailLinks($html) {
    // hledej <a href="https://www.firmy.cz/detail/xxxxx"> ...
    $regex = '~<a[^>]+href\s*=\s*"([^"]+)"[^>]*>~i';
    preg_match_all($regex, $html, $m);
    $found = [];
    foreach($m[1] as $href) {
        if(preg_match('~^https://www\.firmy\.cz/detail/~i', $href)) {
            $found[] = $href;
        }
    }
    return array_unique($found);
}

function findNextPage($html, $baseUrl) {
    // hledej: <a id="nextBtn" href=".."> NEBO class="pagingArrow btnNext"
    if(preg_match('~<a[^>]+id="nextBtn"[^>]+href="([^"]+)"~i', $html, $mm)) {
        return $mm[1]; // relat. odkaz
    }
    if(preg_match('~<a[^>]+class="[^"]*pagingArrow[^"]*btnNext[^"]*"[^>]+href="([^"]+)"~i', $html, $mm)) {
        return $mm[1];
    }
    // fallback atd...
    return null;
}

function absolutize($rel, $base) {
    // zjednodušeno, v praxi raději parse_url + poskládat:
    if(strpos($rel, 'http')===0) return $rel;
    // jinak ...
    $b = parse_url($base);
    $scheme = $b['scheme'] ?? 'https';
    $host   = $b['host']   ?? '';
    $path   = rtrim(dirname($b['path']),'/');
    if(substr($rel,0,1)=='/') {
        return $scheme.'://'.$host.$rel;
    } else {
        return $scheme.'://'.$host.$path.'/'.$rel;
    }
}

// --- main ---
$visited = [];
$q = $startUrl;
$allLinks = [];

while($q) {
    if(in_array($q, $visited)) break;
    $visited[] = $q;

    $html = fetchHtml($q, $client);
    $links = findDetailLinks($html);
    $allLinks = array_merge($allLinks, $links);

    $next = findNextPage($html, $q);
    if($next) {
        $q = absolutize($next, $q);
    } else {
        $q = '';
    }
}

$allLinks = array_values(array_unique($allLinks));

header('Content-Type: application/json; charset=utf-8');
echo json_encode([
   'count'=>count($allLinks),
   'links'=>$allLinks
], JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
?>