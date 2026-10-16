<?php

include('slownik.php'); // $slownik

// Skrypt korzysta z api ze strony responsivevoice.org
// aby dostać klucz i secret wystarczy się zarejestrować i kupić najtańszy pakiet za 9$ na miesiąc
// pamiętaj o anulowaniu subskrypcji po wygenerowaniu sampli!

define('RV_API_KEY', getenv('RESPONSIVEVOICE_API_KEY') ?: 'YOUR_API_KEY');
define('RV_API_SECRET', getenv('RESPONSIVEVOICE_API_SECRET') ?: 'YOUR_API_SECRET');
define('RV_ENDPOINT', 'https://texttospeech.responsivevoice.org/v2/text/synthesize');

function azAZ09($string)
{
    $polskie = array('ę','Ę','ó','Ó','Ą','ą','Ś','ś','ł','Ł','ż','Ż','Ź','ź','ć','Ć','ń','Ń');
    $miedzyn = array('e_','e_','o_','o_','a_','a_','s_','s_','l_','l_','z_','z_','z_','z_','c_','c_','n_','n_');

    $string = str_replace($polskie, $miedzyn, $string);
    $string = str_replace(' ', '_', $string);

    return $string;
}

function getOgg($word, $filename)
{
    @mkdir('mp3');
    @mkdir('ogg');

    $payload = json_encode([
        'text'   => $word,
        'lang'   => 'pl-PL', 
        'gender' => 'female',
        'format' => 'mp3',
        'pitch'  => 1,
        'rate'   => 1.04,
        'volume' => 1,
    ]);

    $ch = curl_init(RV_ENDPOINT);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'X-API-Key: ' . RV_API_KEY,
        'X-API-Secret: ' . RV_API_SECRET,
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $audio = curl_exec($ch);
    if (curl_errno($ch)) {
        curl_close($ch);
        throw new Exception("Błąd cURL: " . curl_error($ch));
    }

    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode !== 200) {
        throw new Exception("API zwróciło błąd HTTP $httpCode dla słowa '$word': $audio");
    }

    file_put_contents("mp3/$filename.mp3", $audio);

    shell_exec("ffmpeg -y -i mp3/$filename.mp3 -af silenceremove=start_periods=0:stop_periods=1:stop_threshold=-40dB:stop_duration=0.2 -ar 32000 -ab 48000 -acodec libvorbis ogg/$filename.ogg");
    unlink("mp3/$filename.mp3");
}

echo "\n-- początek generowania --\n\n";

foreach ($slownik as $row) {

    if (!is_array($row)) continue;

    if (isset($row[1]) && strlen(trim($row[1])) > 0) {
        $filename = azAZ09(trim($row[1]));
    } else {
        $filename = azAZ09(trim($row[0]));
    }

    $filename = strtolower($filename);
    $word = strtolower(trim($row[0]));

    print_r($word . ' - ' . $filename);
    echo "\n";

    getOgg($word, $filename);
}

echo "\n-- koniec generowania --\n\n";
