<?php

    ini_set('max_execution_time', 1800);

    function getAllIdsFromImgw () {
        $res = shell_exec("curl --silent 'https://hydro-back.imgw.pl/map/stations/hydrologic?onlyMainStations=false' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: pl,en-US;q=0.7,en;q=0.3' --compressed -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: https://hydro.imgw.pl/' -H 'Cookie: SRV_=shsrv02.imgw.pl_SRV' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'");

        return json_decode($res)->stations;
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

        if (!in_array($row->id, $requestIds)) continue;

        if (dataFileIsToOld('imgwpodest_data/'.$row->id.'.json', 3600)) {
            $json = shell_exec("curl  --silent 'https://hydro-back.imgw.pl/station/hydro/status?id=".$row->id."' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: pl,en-US;q=0.7,en;q=0.3' --compressed -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: https://hydro.imgw.pl/' -H 'Cookie: SRV_=shsrv01.imgw.pl_SRV' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'");

            file_put_contents('imgwpodest_data/'.$row->id.'.json', $json);
        }

        //file_put_contents('imgwpodest_data/'.$row->i.'.txt', print_r($subdata, true));
        $subdata = json_decode(file_get_contents('imgwpodest_data/'.$row->id.'.json'));

        if (isset($subdata->exception) || !isset($subdata->status)) {
            continue;
        }

        $tmp_river = explode(' (',$subdata->status->river);

        $trends = array('const' => 0, 'unknown' => 0, 'down' => -1, 'up' => 1);
        $result[$row->id] = array(
            'id'                        => $row->id,
            'nazwa'                     => $subdata->status->description,
            'rzeka'                     => $tmp_river[0],
            'region'                    => $subdata->status->province,
            'tendencja'                 => $subdata->status->trend,
            'stan_cm'                   => isset($subdata->status->currentState) ?  $subdata->status->currentState->value : null,
            'poziom_ostrzegawczy'       => $subdata->status->warningValue,
            'poziom_alarmowy'           => $subdata->status->alarmValue,
        );
    }

    //file_put_contents('imgwpodest_data/result.txt', print_r($result, true));
    //file_put_contents('imgwpodest_data/result.json', print_r(json_encode($result), true));

    echo json_encode($result);
    echo "\n";
