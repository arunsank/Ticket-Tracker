#!/bin/bash

<html>
<head> 
<meta charset="utf-8">
<Title>Ticket Tracker</Title>

<script src="d3.min.js"></script>
<script src="nv.d3.min.js"></script>

<link rel="stylesheet" type="text/css" href="Stylinginfo.css">

</head>


<body>


<div class="container" id="LeftPanel" style="width: 500; height: 100%; float: left;">
<header>
   <h1> Table of ticket counts (updates within 10 mins)</h1>
</header>

<?php 
session_set_cookie_params(1800,"/");
session_start();

$url1=$_SERVER['REQUEST_URI'];
header("Refresh: 60; URL=$url1");
if(isset( $_POST["domain"]))
$_SESSION["dom"] = $_POST["domain"];

if(isset( $_POST["username"]))
$_SESSION["username"]= $_POST["username"];

if(isset( $_POST["pwd"]))
$_SESSION["pwd"]= $_POST["pwd"];



$_SESSION["wd"] = getcwd();



?>

Domain : <?php echo $_SESSION["dom"]; ?><br>
Your email address is : <?php echo $_SESSION["username"]; ?> <br>

<?php



$fin = exec('/usr/bin/python2.7 '.$_SESSION["wd"] . '/Tracker.py ' . $_SESSION["dom"] . ' ' . $_SESSION["username"] . ' ' . $_SESSION["pwd"]);

echo "<pre>";





if (strlen($fin))
{  echo $fin;
   echo "<pre>";
   exit();


}
else
{ echo " Welcome " ;


}





echo "<html><body><table border=1>\n\n";
$f = fopen("Count.csv", "r");
while (($line = fgetcsv($f)) !== false) {
        echo "<tr>";
        foreach ($line as $cell) {
                echo "<td>" . htmlspecialchars($cell) . "</td>";
        }
        echo "</tr>\n";
}
fclose($f);
echo "\n</table></body></html>";








?>
</div>

<div class="container" id="RightPanel" style="width: 700; height: 100%; text-align: left; vertical-align: bottom; float: right;">
<header>
   <h1> Dynamic Ticket Visualization to analyze control limits </h1>
</header>

<svg id="chart" style="width:650; height:400;"></svg>  

</div>
</body>


<script type="text/javascript">
//Data Input
	d3.csv("Count.csv", function(error, data){
	console.log(data)
		
    var exampleData = [
    	{
    		key: "totals",
    		values: []
    	}
    ];
    data.forEach(function (d){
    	d.value = +d.value
    	exampleData[0].values.push(d)
    })       

//add nv graph values	
 	nv.addGraph(function() {
		
   		var chart = nv.models.discreteBarChart()
       		.x(function (d) { console.log(d); return d.ViewID })
       		.y(function (d) { return d.value })
       		.staggerLabels(true)
	        .showValues(true)
 
 	  	d3.select('#chart')
    	          .datum(exampleData)
    		  .attr("id", function (d) { console.log(d); })
    		  .transition().duration(500)
       		  .call(chart);
 
   		nv.utils.windowResize(chart.update);
//return chart
   		return chart;
 	});

 });
 
 
 
 
 
</script>

</html>