/**
 * Created by davidgreenfield on 4/13/16.
 */
  window.onload = function() {
        var s = new WebSocket("ws://stream.meetup.com/2/rsvps");

        //document.getElementById("list").innerHTML=eventlist;
        //run on message from python webserver
        s.onmessage = function(e) {

            var ev = JSON.parse(e.data);
            if (eventlist.indexOf(ev.group.group_id) >= 0) {
            document.getElementById("messageboard").innerHTML='<h1>'+ev.event.event_name+'</h1>';
            }
        //insert into the body of the html dom the description, coordinates and a google api image of street view

        }
      };
