var draw;
var temp_texts = [];

$(document).ready(function () {
  //var rawSvg = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="2000" height="1000"> <rect x="50" y="50" height="900" width="700"    fill="rgba(255,192,192,1)" id="room1" />    <rect x="750" y="50" height="900" width="900"   fill="rgba(192,255,192,1)" id="room2" />    <rect x="50" y="50" height="900" width="700"    fill="rgba(255,0,0, 0)" stroke="black"  stroke-width="10" id="room1_wall" />    <rect x="750" y="50" height="900" width="900"   fill="rgba(255,0,0, 0)" stroke="black"  stroke-width="10" id="room2_wall" /></svg>'
  draw = SVG('floorplan').viewbox(0,0,750,750);
  var store;
  $.ajax({
    url: '../static/images/floorplan2.svg',
    type: 'GET',
    async: false
  })
  .done(function(data) {
    store = draw.svg(data.firstChild.outerHTML);
  });
  ready = true;
});

function draw_temps (db_data, draw) {
  for (var i = temp_texts.length - 1; i >= 0; i--) {
    temp_texts[i].remove();
  };
  temp_texts = [];
  var readings = [];
  var temp_sensors = db_data.sensor.where("(el) => el.sensortype == 'Temperature'");
  for (var i = db_data.sensorreading.length - 1; i >= 0; i--) {
    if (temp_sensors.where("(el) => el.id == " + db_data.sensorreading[i].sensor).length > 0)
    {
      readings[readings.length] = db_data.sensorreading[i];
    }
  };
  temp_texts = [];
  for (var i = 0; i < db_data.room.length; i++) {
    var room = db_data.room[i];
    var room_sensors = db_data.sensor.where("(el) => el.room ==" + room.id);
    var room_readings = []
    for (var j = db_data.sensorreading.length - 1; j >= 0; j--) {
      if (room_sensors.where("(el) => el.id == " + db_data.sensorreading[i].sensor).length > 0)
      {
        room_readings[room_readings.length] = db_data.sensorreading[j];
      }
    };
    if (room_readings.length > 0)
    {
      var string = room_readings[0].reading + "°"
      var text = draw.text(string).font({
        family:   'Helvetica'
        , size:     20
        , anchor:   'topleft'
        , leading:  '1.5em'
      });

      text.x(room.xpos + 10);
      text.y(room.ypos + 10);

      temp_texts[i] = text;
    }
  };
}

function roominfo(db_data, room_id) {
  var room_sensors = db_data.sensor.where("()");
}