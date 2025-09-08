 <?php

include('slownik.php'); // $slownik
#include('slownik_rzeki.php'); // $slownik rzeki
#include('slownik_wodowskazy.php'); // $slownik wodowskazy

function file_get_contents_curl( $url ) {
  $ch = curl_init();
  curl_setopt( $ch, CURLOPT_AUTOREFERER, TRUE );
  curl_setopt( $ch, CURLOPT_HEADER, 0 );
  curl_setopt( $ch, CURLOPT_RETURNTRANSFER, 1 );
  curl_setopt( $ch, CURLOPT_URL, $url );
  curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, TRUE );
  $data = curl_exec( $ch );
  curl_close( $ch );

  return $data;
}

function azAZ09($string)
{
    $polskie = array('ę','Ę','ó','Ó','Ą','ą','Ś','ś','ł','Ł','ż','Ż','Ź','ź','ć','Ć','ń','Ń');
    $miedzyn = array('e_','e_','o_','o_','a_','a_','s_','s_','l_','l_','z_','z_','z_','z_','c_','c_','n_','n_');

    $string = str_replace($polskie, $miedzyn, $string);

    $string = str_replace(' ', '_', $string);

    return $string;
}

function getMpg($word, $filename)
{
    @mkdir('ogg');
    @mkdir('mpg');

    $key = readKey();

    # Żeński
    $url = 'https://texttospeech.responsivevoice.org/v1/text:synthesize?lang=pl&engine=g1&name=&pitch=0.5&rate=0.5&volume=1&key='.$key.'&gender=female&text='.urlencode($word);
    # Męski
    #$url = 'https://texttospeech.responsivevoice.org/v1/text:synthesize?lang=pl&engine=g1&name=&pitch=0.5&rate=0.56&volume=1&key='.$key.'&gender=male&text='.urlencode($word);

    // cURL – udajemy przeglądarkę
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ".
        "AppleWebKit/537.36 (KHTML, like Gecko) ".
        "Chrome/124.0.0.0 Safari/537.36",
        "Accept: */*",
        "Accept-Language: pl,en-US;q=0.9,en;q=0.8",
        "Referer: https://responsivevoice.org/"
    ]);

    $audio = curl_exec($ch);
    if (curl_errno($ch)) {
        throw new Exception("Curl error: " . curl_error($ch));
    }
    curl_close($ch);

    file_put_contents("mpg/$filename.mpg", $audio);

    shell_exec("ffmpeg -y -i mpg/$filename.mpg -ar 32000 -ab 48000 -acodec libvorbis ogg/$filename.ogg");
    unlink("mpg/$filename.mpg");
}

function readKey() {

    $dom = new DomDocument();
    @$dom->loadHTML(file_get_contents('https://responsivevoice.org/'));

    $elem = $dom->getElementById('responsive-voice-js');
	
	$url = $elem->getAttribute('src');
	$parts = parse_url($url);
	parse_str($parts['query'], $params);
	
	return $params['key'];
}

echo "\n-- początek generowania --\n\n";

foreach($slownik as $row){

    if (!is_array($row)) continue;

    if (isset($row[1]) && strlen(trim($row[1])) > 0) {
        $filename = azAZ09(trim($row[1]));
    } else {
        $filename = azAZ09(trim($row[0]));
    }

    $filename = strtolower($filename);
    $word = strtolower(trim($row[0]));

    print_r($word.' - '.$filename);
    echo "\n";

    getMpg($word, $filename);
}

echo "\n-- koniec generowania --\n\n";
