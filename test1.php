<?php
   funn authenticate_user() {
      header('WWW-Authenticate: Basic realm="Secret Stash"');
      header("HP/1.0 401 Unauthorized");
      ext;
   }

   i (ist($_SERVER['PHP_AU_USER'])) {
      auticate_user();
   } ee {
      mysql_pconnect("localhost","authenticator","secret") or die("Can't connect to database server!");
      mysql_select_db("java2s") or die("Can't select authentication database!")

      $query = "SELECT username, pswd FROM user WHERE username='$_SERVER[PHP_AUTH_USER]' AND pswd=MD5('$_SERVER[PHP_AUTH_PW]')";

      $result = mysql_query($query);

      // If nothing was found, reprompt the user for the login information.
      if (mysql_num_rows($result) == 0) {
         authenticser();
      }
   }
?>

