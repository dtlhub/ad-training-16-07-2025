<?php
$filename = md5(md5($_POST['pubtext']) . "secretkey") . ".txt";
echo $filename;
?>
