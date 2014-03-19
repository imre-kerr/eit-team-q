var draw;
var light_gradient;
var room_rects = [];
var temp_texts = [];
var lights = [];

$(document).ready(function () {
  //var rawSvg = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="2000" height="1000"> <rect x="50" y="50" height="900" width="700"    fill="rgba(255,192,192,1)" id="room1" />    <rect x="750" y="50" height="900" width="900"   fill="rgba(192,255,192,1)" id="room2" />    <rect x="50" y="50" height="900" width="700"    fill="rgba(255,0,0, 0)" stroke="black"  stroke-width="10" id="room1_wall" />    <rect x="750" y="50" height="900" width="900"   fill="rgba(255,0,0, 0)" stroke="black"  stroke-width="10" id="room2_wall" /></svg>'
  draw = SVG('floorplan').viewbox(50,50,750,750);
  
  light_gradient = draw.gradient('radial', function(stop) {
    s1 = stop.at({offset:0, color:'#ff0', opacity:1})
    s2 = stop.at({offset:0.5, color:'#ff0', opacity:0.5})
    s3 = stop.at({offset:01, color:'#ff0', opacity:0})
  });
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

function popup(room) {
  $('.room-dialog').dialog({
    modal: true,
    height:140
  });
  $('.room-dialog').text("Her skal det stå jævlig mye fet info om rom: " + room.name);
}

function add_popup(rect, room) {
  rect.click(function() {popup(room)});
}

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
  }
  temp_texts = [];
  if (room_rects.length == 0) {
    for (var i = 0; i < db_data.room.length; i++) {
      var room = db_data.room[i];
      var rect = room_rects[room_rects.length] = draw.svg(room.image);
      add_popup(rect.roots()[0], room);
    }
  }
  for (var i = 0; i < db_data.room.length; i++) {
    var room = db_data.room[i];
    var room_sensors = db_data.sensor.where("(el) => el.room ==" + room.id);
    var room_readings = []
    for (var j = db_data.sensorreading.length - 1; j >= 0; j--) {
      if (room_sensors.where("(el) => el.id == " + db_data.sensorreading[j].sensor).length > 0)
      {
        room_readings[room_readings.length] = db_data.sensorreading[j];
      }
    };
    if (room_readings.length > 0)
    {
      room_rects[i].roots()[0].fill(temp_color(room_readings[0].reading));
      var string = room_readings[0].reading.toFixed(1) + "°"
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


function draw_lights(db_data, draw) {
  var light_sensors = db_data.sensor.where("(el) => el.sensortype == 'Light'");
  var readings = [];
  for (var i = db_data.sensorreading.length - 1; i >= 0; i--) {
    if (light_sensors.where("(el) => el.id == " + db_data.sensorreading[i].sensor).length > 0)
    {
      readings[readings.length] = db_data.sensorreading[i];
    }
  }
  if (lights.length == 0) {
    for (var i = light_sensors.length - 1; i >= 0; i--) {
      
    };
  }

  // SHOW SOME GRADIENTS
}

function temp_color(temp) {
  var min_temp = 15.0;
  var max_temp = 25.0;
  var min_hue = 0.67;
  var max_hue = 0.0;

  var hue;
  if (temp < min_temp)
    hue = min_hue;
  else if (temp > max_temp)
    hue = max_hue;
  else
    hue = min_hue + (temp - min_temp)/(max_temp - min_temp) * (max_hue - min_hue);
  var rgb = HSVtoRGB(hue, 0.5, 1.0);
  return "rgba(" + rgb.r + "," + rgb.g + "," + rgb.b + ",0.4)";
}

/* accepts parameters
 * h  Object = {h:x, s:y, v:z}
 * OR 
 * h, s, v
*/
function HSVtoRGB(h, s, v) {
    var r, g, b, i, f, p, q, t;
    if (h && s === undefined && v === undefined) {
        s = h.s, v = h.v, h = h.h;
    }
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
    }
    return {
        r: Math.floor(r * 255),
        g: Math.floor(g * 255),
        b: Math.floor(b * 255)
    };
}