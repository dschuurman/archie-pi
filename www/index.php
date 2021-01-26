<html>
<!-- ARCHIE Pi top-level web page -->
<head>
    <title>ARCHIE Pi</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
</head>
<body>
<table>
<tr>
    <td><img src="archie-pi.png"></td>
</tr>
<tr>
    <td style="font-size:1.2em;"><b>A</b>nother <b>R</b>emote <b>C</b>ommunity <b>H</b>otspot for <b>I</b>nstruction and <b>E</b>ducation</td>
</tr>
</table>

<p>Welcome to the <b>ARCHIE Pi</b>! Installed modules are listed below:</p>
<?php
// Show each installed module on the top level page
$files = scandir('/var/www/modules');
foreach ($files as $file) {
   if ($file == '.') continue;
   if ($file == '..') continue;
   $module = '/var/www/modules/'.$file.'/index.htmlf';
   $dir = 'modules/'.$file;
   include $module;
   }
?>

<p>
<b>ARCHIE Pi</b> version 0.22, January 2021
<br><a href="about.html">About</a> the ARCHIE Pi
</p>
</body>
</html>