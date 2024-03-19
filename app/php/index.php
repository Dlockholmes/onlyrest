<?php
if(isset($_SESSION)){
    echo $_SESSION;
} else {
    echo "NO SESS";
    session_start();
    $_SESSION["start"]="hi";
}
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Secured LOGIN</title>
        <link rel="stylesheet" href="./css/main.css">
    </head>
    <body>
        <form id="login" class="login" action="./index.php" method="POST">
            <div>
                <input type="text" name="id" placeholder="Insert ID">
            </div>
            <div>
                <input type="password" name="pw" placeholder="Insert PW">
                <button type="submit">LOGIN</button>
            </div>
        </form>
    </body>
</html>
<?php
function idfilter($id){
    $res = str_contains($id,"h");
    echo $res?"true":"false";
}
if($_SERVER["REQUEST_METHOD"]=="POST"){
    $id=NULL; $pw = NULL;
    if(array_key_exists("id",$_POST) && array_key_exists("pw",$_POST)){
        $id = $_POST["id"];
        $pw = $_POST["pw"];
    }
    echo "{$id} | {$pw}<br>";
    idfilter($id);
}
?>