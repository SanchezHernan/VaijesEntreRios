# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 19:02:40 2018

@author: Hornyt0x
"""

def localizacion(lat, lon):
    latitud=str(lat)
    longitud=str(lon)
    html= \
"""
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Simple markers</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>
function addMarker(lati, long, map){
	var city = {lat: lati, lng: long};
  return (new google.maps.Marker({position: city, map: map}));
 };

function initMap() {
  var myLatLng = {lat: """+latitud+""" , lng: """+longitud+"""};
  var villaguay = {lat: -31.950, lng: -59.200};
  

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 7,
    center: villaguay
  });

  var marker = new google.maps.Marker({position: villaguay, map: map});
}

    </script>
    <script async defer
        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCXQfkDrWHjpnG-0DvUcgtFkGdsKm2esG0&callback=initMap"></script>
  </body>
</html>
"""
    return html