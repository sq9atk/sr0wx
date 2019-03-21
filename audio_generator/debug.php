<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

 function _d($var="Nie podano parametru", $text="yellow", $background = '#222255')
{
    $bt = debug_backtrace();
    $caller = array_shift($bt);

    $title = $caller['file']."\nlinia: ".$caller['line'];
    $title = str_replace('/www/htdocs','',$title);

    echo '<pre id="dump" style="background-color:'.$background.';color:'.$text.';font-size:10px;text-align:left;line-height:12px;padding:2px;" title="'.$title.'" >';

    $type = gettype($var);
    if (in_array($type, array('boolean', 'integer', 'double', 'string', 'resource', 'NULL', 'unknown type'))) {
        var_dump($var);
    }else{
        print_r($var);
    }
    echo '</pre>';
}
