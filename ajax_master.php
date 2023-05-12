<?php

$state=$_POST["state"];
echo"hello";

if($state==1){
    $xx=exec("sudo python3 /var/www/html/earthrover/VideoStreamingFlask/main.py");
    //$xx=exec("sudo python3 /var/www/html/earthrover/VideoStreamingFlask/main.py ");
     }
     else{
       $xx=exec("sudo pkill -f /var/www/html/earthrover/VideoStreamingFlask/main.py");
       // $xx=exec("sudo pkill -f /var/www/html/earthrover/VideoStreamingFlask/main.py");
      }
echo"$state";
?>
