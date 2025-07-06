<?php
include("include/session.php");

// Check if user is logged in and userid is set in session
if (!isset($_SESSION['userid'])) {
    die("Access denied. Please log in." . $_SESSION['userid']);
}

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get form data
$pub_id = md5(md5($_POST['pubtext']) . "pubidkeyrofl");
$filename = md5(md5($_POST['pubtext']) . "secretkey") . ".txt";
$userid = $session->username;

$file = fopen("receipts/" . $filename, "w");
if ($file == 0) {
    die("Error");
}
fwrite($file, $_POST['pubtext']);
fclose($file);

// Prepare and execute statement
$result = $database->query("INSERT INTO publications  VALUES ('". $pub_id . "','" . $userid . "','" . $filename . "')");

if ($result) {
    header("Location: /readPub.php?fnSuccess=3&fnPubilcation=" . $filename);
    echo "Publication added successfully!";
    echo "<a href='/readPub.php?fnSuccess=3&fnPubilcation=" . $filename . "'> Открыть публикацию</a>";
} else {
    echo "Error: " . $stmt->error;
}
?>
