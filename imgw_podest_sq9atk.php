<?php

    ini_set('max_execution_time', 1800);

    function getAllIdsFromImgw () {
        $res = shell_exec("curl --silent 'https://hydro.imgw.pl/api/map/?category=hydro' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: pl,en-US;q=0.7,en;q=0.3' --compressed -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: https://hydro.imgw.pl/' -H 'Cookie: SRV_=shsrv02.imgw.pl_SRV' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'");

        return json_decode($res);
    }

    function getRequestedIds ($base64json) {
        $data = json_decode(base64_decode($base64json));

        $res = array();
        foreach ($data as $row) {
            if (strstr($row, '.')) {
                $tmp = explode('.', $row);
                $row = $tmp[1];
            }
            $res[] = $row;
        }
        return $res;
    }

    function dataFileIsToOld ($filename, $olderThanSeconds=1800) {
        if (!file_exists($filename)) {
            return true;
        }
        return time() - filemtime($filename) > $olderThanSeconds;
    }

    $allIds = getAllIdsFromImgw();
    $requestIds = getRequestedIds($argv[1]);

    if(!file_exists('imgwpodest_data')){
        $oldmask = umask(0);
        mkdir('imgwpodest_data',0777);
        umask($oldmask);
    }

    $result = array();
    foreach($allIds as $row){

        if (!in_array($row->i, $requestIds)) continue;

        if (dataFileIsToOld('imgwpodest_data/'.$row->i.'.json', 3600)) {
            $json = shell_exec("curl  --silent 'https://hydro.imgw.pl/api/station/hydro/?id=".$row->i."' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: pl,en-US;q=0.7,en;q=0.3' --compressed -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: https://hydro.imgw.pl/' -H 'Cookie: SRV_=shsrv01.imgw.pl_SRV' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'");

            file_put_contents('imgwpodest_data/'.$row->i.'.json', $json);
       }

        $subdata = json_decode(file_get_contents('imgwpodest_data/'.$row->i.'.json'));

        $tmp_river = explode(' (',$subdata->status->river);

        $trends = array('const' => 0, 'unknown' => 0, 'down' => -1, 'up' => 1);
        $result[$row->i] = array(
            'id'                        => $row->i,
            'nazwa'                     => $subdata->status->description,
            'rzeka'                     => $tmp_river[0],
            'region'                    => $subdata->status->province,
            'tendencja'                 => $trends[$subdata->trend],
            'stan_cm'                   => isset($subdata->status->currentState) ?  $subdata->status->currentState->value : null,
            'poziom_ostrzegawczy'       => $subdata->status->warningValue,
            'poziom_alarmowy'           => $subdata->status->alarmValue,
        );
    }

    echo json_encode($result);
    echo "\n";

