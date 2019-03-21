<?php

include('debug.php'); 

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
    $url = 'https://code.responsivevoice.org/getvoice.php?tl=pl&pitch=0.5&rate=0.5&vol=1&t='.urlencode($word);
    $audio = file_get_contents_curl($url);

    file_put_contents('mpg/'.$filename.'.mpg', $audio);

    shell_exec ( "ffmpeg -i mpg/$filename.mpg   -ar 16000  -ab 48000 -acodec libvorbis ogg/$filename.ogg");
    unlink("mpg/$filename.mpg");
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
