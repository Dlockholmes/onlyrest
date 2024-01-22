<form method="post">
    <input type="submit" name="test" id="test">
</form>

<?php
    function testfun(){
        echo "Hello world";
    }
    if(array_key_exists('test',$_POST)){
        testfun();
    }
?>