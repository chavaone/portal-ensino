import $ from 'jquery'


export default {
  updateOSMTimes(centros, currentLocation, callback) {
    const request_max_size = 300;
    var  ajax_calls = [],
          localizaciones = "";

    for (var i = 0; i < centros.length; i += request_max_size) {
      //Get center locations string
      localizaciones = centros.slice(i, i + request_max_size).map(function(centro) {
        return centro.coor.lon.toString()  + "," +  centro.coor.lat.toString();
      });

      //Create AJAX call
      ajax_calls.push(
        $.ajax({
          method: "GET",
          url: "https://osrm.aquelando.info/table/v1/driving/" +
                currentLocation.lon.toString() +
                "," +
                currentLocation.lat.toString() +
                ";" +
                localizaciones.join(";"),
          data: {
            sources: 0
          }
        })
      );
    }

    $.when.apply($, ajax_calls).then(
      function() {
        for (var i = 0; i < arguments.length; i++) {
          for(var j = 0; j < arguments[i][0].durations[0].length; j++) {
            if(! centros [i*request_max_size + j]) continue;
            if (! centros[i*request_max_size + j].osm) centros[i*request_max_size + j].osm = {};
            centros[i*request_max_size + j].osm.tiempo = arguments[i][0].durations[0][j+1];
          }
        }
        callback();
      },
      function(e) {
           console.log("My ajax failed");
      });
  },
  updateOSMDistances(centros, currentLocation, callback) {
    const R = 6371; // Radius of the earth in km
    var dLat,dLon,a;

    for (var i = 0; i < centros.length; i++) {
      dLat = (centros[i].coor.lat - currentLocation.lat) * Math.PI / 180;  // deg2rad below
      dLon = (centros[i].coor.lon - currentLocation.lon) * Math.PI / 180;
      a =
       0.5 - Math.cos(dLat)/2 +
       Math.cos(currentLocation.lat * Math.PI / 180) * Math.cos(centros[i].coor.lat * Math.PI / 180) *
       (1 - Math.cos(dLon))/2;

      if (! centros[i].osm) centros[i].osm = {};
      centros[i].osm.distancia = R * 2 * Math.asin(Math.sqrt(a));
    }
    callback();
  },
  getOSMDetailedRouteInfo(centro, currentLocation, callback) {
    var self = this;
    $.ajax({
      method: "GET",
      url: "https://osrm.aquelando.info/route/v1/driving/" +
            currentLocation.lon.toString() +
            "," +
            currentLocation.lat.toString() +
            ";" +
            centro.coor.lon.toString()  +
            "," +
            centro.coor.lat.toString(),
      data: {
        steps: true,
        overview: false
      }
    }).done (function(data) {
      centro.osm.details = data.routes[0];
      centro.osm.routeData = self.getOSMRouteInfo(centro.osm.details.legs[0].steps);
      callback();
    })
  },
  _reduceSteps (steps) {
    if (steps.length == 0) return {distancia: 0, tiempo: 0};
    return steps.reduce((step1, step2) => ({distancia: step1.distancia + step2.distancia, tiempo: step1.tiempo + step2.tiempo}));
  },
  getOSMRouteInfo(steps) {
    var ret = {},
        steps = steps.map(
          function(step) {
            return {
              distancia: step.distance,
              tiempo: step.duration,
              speed: step.distance / step.duration,
              ref: step.ref
            };
          });

    var stepscat1 = steps.filter((step) => (this.getStepCategory(step) == 0));
    ret.cat1 = this._reduceSteps(stepscat1);

    var stepscat2 = steps.filter((step) => (this.getStepCategory(step) == 1));
    ret.cat2 = this._reduceSteps(stepscat2);

    var stepscat3 = steps.filter((step) => (this.getStepCategory(step) == 2));
    ret.cat3 = this._reduceSteps(stepscat3);

    return ret;
  },
  getStepCategory(step) {
    //CAT1 Autovías -> ref empeza por A ou velocidade superior a 27m/s ~ 97Km/h.
    if (step.ref && step.ref.startsWith('A')) return 0;
    if (step.speed >= 27) return 0;

    //CAT2 Non autovías e velocidade superior a 18/s ~ 65Km/h
    if (step.speed >= 18) return 1;

    //CAT3 O Resto
    return  2;
  },
  beautifyDistance(distance) {
    if (distance < 1) {
        return (Math.floor(distance * 1000)).toString() + "m.";
    }
    return Math.floor(distance).toString() + "km.";
  },
  beautifyTime (seconds) {
    var ret = "",
        secondsInt = Math.floor(seconds),
        hours = Math.floor(secondsInt / 3600),
        minutes = Math.floor((secondsInt % 3600) / 60),
        secs = (secondsInt % 3600) % 60;

        if (hours) {
            ret = hours.toString() + "h.";
        }

        if (minutes) {
            ret = ret + minutes.toString() + "min.";
        }

        if (secondsInt && ! ret) {
            ret = ret + secs.toString() + "s.";
        }

    return ret;
  }
}
