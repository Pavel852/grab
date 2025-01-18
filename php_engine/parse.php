<?php
/**
 * parse.php
 *
 * Přijme parametr detailUrl (např. ?action=parse&detailUrl=https://www.firmy.cz/detail/xxxxxxx-nazev.html)
 * a z dané stránky vyparsuje jméno, popis, web, tel, email, address, zip, city...
 * Výstup = JSON.

**Autor:** PB  
**Email:** pavel.bartos.pb@gmail.com  
**Datum:** 2/2025  
**ORCID:** <https://orcid.org/0009-0001-3558-4312>  
**GitHub:** <https://github.com/Pavel852>  
**Licence:** Creative Commons (CC)


 */

require __DIR__ . '/vendor/autoload.php';

use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;
use Symfony\Component\DomCrawler\Crawler;

$detailUrl = isset($_GET['detailUrl']) ? $_GET['detailUrl'] : null;
if (!$detailUrl) {
    header('Content-Type: text/plain; charset=utf-8');
    die("Chybí parametr 'detailUrl'.");
}

$client = new Client([
    'timeout' => 10.0,
]);

// Pomocná funkce pro extrakci
function parseDetailPage(string $detailUrl, Client $client): array
{
    $data = [
        'name'        => '',
        'description' => '',
        'web'         => '',
        'tel'         => '',
        'email'       => '',
        'address'     => '',
        'zip'         => '',
        'city'        => '',
        'country'     => '',
    ];

    try {
        $resp = $client->get($detailUrl, [
            'headers' => [
                'User-Agent' => 'Mozilla/5.0 (PHP parse script)',
            ]
        ]);
        $html = (string) $resp->getBody();
    } catch (RequestException $e) {
        $data['name'] = "Chyba načtení: " . $e->getMessage();
        return $data;
    }

    $crawler = new Crawler($html, $detailUrl);

    // name => <h1.detailPrimaryTitle>
    $h1 = $crawler->filter('h1.detailPrimaryTitle');
    if ($h1->count()) {
        $data['name'] = trim($h1->text());
    }

    // description => .detailDescription .description
    $desc = $crawler->filter('.detailDescription .description');
    if ($desc->count()) {
        $data['description'] = trim($desc->text());
    }

    // web => <a.detailWebUrl.url> => extrahujeme host
    $webNode = $crawler->filter('a.detailWebUrl.url');
    if ($webNode->count()) {
        $rawWeb = $webNode->attr('href');
        $host = parse_url($rawWeb, PHP_URL_HOST);
        $data['web'] = $host ?: $rawWeb;
    }

    // tel => <span data-dot="origin-phone-number">
    $telNode = $crawler->filter('span[data-dot="origin-phone-number"]');
    if ($telNode->count()) {
        $data['tel'] = trim($telNode->text());
    }

    // email => <a href="mailto:...">
    $mailNode = $crawler->filter('a[href^="mailto:"]');
    if ($mailNode->count()) {
        $rawMail = $mailNode->first()->attr('href');
        $data['email'] = preg_replace('/^mailto:/i', '', $rawMail);
    }

    // address => .detailAddress.speakable.location
    $addrNode = $crawler->filter('.detailAddress.speakable.location');
    if ($addrNode->count()) {
        $addrText = $addrNode->text();
        // Odstranit "Navigovat"
        $addrText = str_ireplace('Navigovat', '', $addrText);
        $addrText = trim(preg_replace('/\s+/', ' ', $addrText));

        $data['address'] = $addrText;

        // PSČ
        if (preg_match('/\b(\d{3}\s?\d{2})\b/', $addrText, $mm)) {
            $data['zip'] = $mm[1];
        }
        // city
        if (preg_match('/\b\d{3}\s?\d{2}\s+(.*)$/', $addrText, $mm)) {
            $data['city'] = trim($mm[1]);
        }
    }

    return $data;
}

$result = parseDetailPage($detailUrl, $client);
header('Content-Type: application/json; charset=utf-8');
echo json_encode($result, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);

?>