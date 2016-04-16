/**
 * Created by davidgreenfield on 4/15/16.
 */

var markers = [];
var map;
function initMap() {

  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {lat: 39.8282, lng: -98.5795}
  });

  map.addListener('click', function(){drop()});
}

function drop () {
    for (var i = 0; i < gps.length; i++) {
        for (var x = 0; x < gps[i].length; x++) {
            addMarkerWithTimeout({lat: gps[i][x][1], lng: gps[i][x][2]},i*500,i,gps[i][x][0]);
        }
    }
  }


function addMarkerWithTimeout(position, timeout,i,name) {
    var image = {
              url: 'https://s3.amazonaws.com/dg2815/leafcircle.gif',
              // This marker is 20 pixels wide by 32 pixels high.
              size: new google.maps.Size(25, 25),
              // The origin for this image is (0, 0).
              origin: new google.maps.Point(0, 0),
              // The anchor for this image is the base of the flagpole at (0, 32).
              anchor: new google.maps.Point(0, 32)
          };

    window.setTimeout(function () {
        document.getElementById("mapyear").innerHTML = '<h2>Meetup Groups:   ' + years[i] + '</h2>';
        var infowindow = new google.maps.InfoWindow({
    content: name
        });
        var marker =new google.maps.Marker({
                position: position,
                map: map,
                title: name,
                icon:image
            })
        marker.addListener('click', function() {
        infowindow.open(map, marker);})
        markers.push(marker);
    }, timeout);

}


function clearMarkers() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
    drop();
}



