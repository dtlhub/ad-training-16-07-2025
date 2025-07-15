<?php

include("include/database.php");
error_reporting(0);
if ($_GET['fnSuccess'] == 1) {
    set_include_path('/var/www/html/receipts/');
    $pub = file_get_contents($_GET['fnPubilcation'], TRUE);
    if ($pub == FALSE) {
        die("No such file");
    }
    echo $pub;
    unlink('/var/www/html/receipts/' . $_GET['fnPubilcation']);
    $database->query("DELETE FROM publications WHERE filename=" . "'" . $_GET['fnPubilcation'] . "';");
} else if ($_GET['fnSuccess'] == 3) {
    die("<head><meta charset=\"UTF-8\"></head>Пост содержит секретные материалы!");
} else {
    die("Ошибка");
}
?>
