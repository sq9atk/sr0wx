<?php

    ini_set('max_execution_time', 1800);
    
    function getAllIdsFromImgw () {
        return json_decode(file_get_contents('http://monitor.pogodynka.pl/api/map/?category=hydro'));
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
        
       if ( dataFileIsToOld('imgwpodest_data/'.$row->i.'.json', 3600)) {
            $json = file_get_contents('http://monitor.pogodynka.pl/api/station/hydro/?id='.$row->i);
            file_put_contents('imgwpodest_data/'.$row->i.'.json', $json);
       }

        $subdata = json_decode(file_get_contents('imgwpodest_data/'.$row->i.'.json'));

        $tmp_river = explode(' (',$subdata->status->river);

        $trends = array(2 => 0, 3 => -1, 4 => 1);
        
        $result[$row->i] = array(
            'id'                        => $row->i,
            'nazwa'                     => $subdata->status->description,
            'rzeka'                     => $tmp_river[0],
            'rzeka_id'                  => str_replace(')','',$tmp_river[1]),
            'region'                    => $subdata->status->province,
            'tendencja'                 => @$trends[$subdata->status->trend],
            'stan'                      => $subdata->status->state,
            'stan_cm'                   => $subdata->status->currentValue,
            'stan_cm_old'               => $subdata->status->previousValue,
            'poziom_ostrzegawczy'       => $subdata->status->warningValue,
            'poziom_alarmowy'           => $subdata->status->alarmValue,
            'water_gauge_zero_ordinate' => $subdata->status->waterGaugeZeroOrdinate,
            'lat'                       => $row->la,
            'lon'                       => $row->lo
        );    
    }

    echo json_encode($result);
    echo "\n";

