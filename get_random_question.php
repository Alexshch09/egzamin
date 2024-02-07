<?php
$servername = "192.168.0.185";
$username = "root";
$password = "";
$dbname = "ttt";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM questions ORDER BY CONCAT(NOW(), FLOOR(1000 * RAND())) LIMIT 1";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    echo json_encode($row);
} else {
    echo "No questions found";
}

$conn->close();
?>
