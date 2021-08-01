<template lang="html">
  <div class="modal fade"
       id="centerInfoModal"
       tabindex="-1"
       role="dialog"
       aria-labelledby="centerInfoModalLabel"
       aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="centerInfoModalLabel">{{ $t('title')}}</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body" v-if="show_data">

          <div class="infoCenter">
            <div class="infoCenter__info">
              <dl>
                <dt>{{ $t('name') }}</dt>
                <dd>{{center.details.nome}}</dd>

                <dt>{{ $t('cod') }}</dt>
                <dd>{{center.details.cod}}</dd>

                <dt>{{ $t('address') }}</dt>
                <dd>{{center.details.end}} </dd>

                <dt>{{ $t('cp') }}</dt>
                <dd>{{center.details.cp}} </dd>

                <dt v-if="center.details.tlf">{{ $t('tlf') }}</dt>
                <dd v-if="center.details.tlf">{{center.details.tlf}} </dd>

                <dt v-if="center.details.web">{{ $t('web') }}</dt>
                <dd v-if="center.details.web"><a :href="center.details.web">{{center.details.web}}</a></dd>
            </dl>
            </div>
            <div class="infoCenter__map">
              <div class="aqd-map-container">
                <l-map ref="map2" :zoom="zoom" :center="map_center">
                  <l-tile-layer :url="url" :attribution="attribution" ></l-tile-layer>
                  <l-marker :lat-lng="marker_posicion"></l-marker>
                  <l-marker :lat-lng="marker_centro"></l-marker>
                </l-map>
              </div>

              <div class="infoCenter__routeinfo" v-if="!!center.osm.details">
                <h5>Ruta</h5>

                <table>
                <thead>
                  <tr>
                    <th></th>
                    <th>
                      <span class="cat-icon cat-icon--1">1</span>
                    </th>
                    <th>
                      <span class="cat-icon cat-icon--2">2</span>
                    </th>
                    <th>
                      <span class="cat-icon cat-icon--3">3</span>
                    </th>
                    <th></th>
                  </tr>
                  <tr>
                    <th></th>
                    <th>
                      <p class="cat-info">Autovías ou velocidade >= 95Km/h</p>
                    </th>
                    <th>
                      <p class="cat-info">Velocidade >= 70Km/h</p>
                    </th>
                    <th>
                      <p class="cat-info">Outros</p>
                    </th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Distancia</td>
                    <td>{{ beautifyDistance(center.osm.routeData.cat1.distancia/1000)}}</td>
                    <td>{{ beautifyDistance(center.osm.routeData.cat2.distancia/1000)}}</td>
                    <td>{{ beautifyDistance(center.osm.routeData.cat3.distancia/1000)}}</td>
                    <td>{{ beautifyDistance(center.osm.details.distance/1000)}}</td>
                  </tr>
                  <tr>
                    <td>Tempo</td>
                    <td>{{ beautifyTime(center.osm.routeData.cat1.tiempo)}}</td>
                    <td>{{ beautifyTime(center.osm.routeData.cat2.tiempo)}}</td>
                    <td>{{ beautifyTime(center.osm.routeData.cat3.tiempo)}}</td>
                    <td>{{ beautifyTime(center.osm.details.duration)}}</td>
                  </tr>
                </tbody>
                </table>
              </div>



            </div>
            <div class="infoCenter__ensinanzas">
              <h4>Ensinanzas</h4>
              <ul class="infoCenter__ensinanzas__lista">
                <li class="infoCenter__ensinanzas__ensinanza" v-for="item in center.details.ens">
                  <span class="infoCenter__ensinanzas__ensinanza__tipo">{{item.tipo}}</span>
                  <span class="infoCenter__ensinanzas__ensinanza__grado" v-if="item.grado">
                    {{ nivelEnsinanza(item.grado) }}
                  </span>
                  <span class="infoCenter__ensinanzas__ensinanza__nome">{{item.nome}}</span>
                </li>
              </ul>
            </div>
          </div>

        </div>
        <div class="modal-body" v-else>
          <div class="d-flex justify-content-center">
            <div class="spinner-border" role="status">
              <span class="sr-only">{{ $t('loading')}}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import L from 'leaflet';
  import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';
  import OSMFunctions from '../assets/scripts/OSMFunctions.js'

  delete L.Icon.Default.prototype._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: '/static/img/marker-icon2.png',
    iconUrl: '/static/img/marker-icon2.png',
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
  });

  export default {
    props: {
      center: Object,
      position: Object
    },
    components: {
        LMap,
        LTileLayer,
        LMarker,
    },
    methods: {
      onShown(){
        var self = this;
        setTimeout(function () {
          self.$refs.map2.mapObject.invalidateSize();
        }, 500);

        if (this.center.osm.details) {
          this.draw_polyline();
        } else {
          OSMFunctions.getOSMDetailedRouteInfo(this.center, this.position, this.draw_polyline);
        }
      },
      draw_polyline() {
        var polyline = require('@mapbox/polyline');
        var colors = ['green', 'yellow', 'red'];

        //Dibujamos polylines...
        this.center.osm.details.legs[0].steps.forEach((step, i) => {
          var pol_array = polyline.decode(step.geometry);
          var step_cat = OSMFunctions.getStepCategory({
              distancia: step.distance,
              tiempo: step.duration,
              speed: step.distance / step.duration,
              ref: step.ref
          });
          L.polyline(pol_array, {color: colors[step_cat]}).addTo(this.$refs.map2.mapObject);
        });
      },
      beautifyDistance(distance) {
        return OSMFunctions.beautifyDistance(distance);
      },
      beautifyTime (seconds) {
        return OSMFunctions.beautifyTime(seconds);
      },
      nivelEnsinanza(nivel) {
        return {
          "B": "Básico",
          "M": "Medio",
          "S": "Superior"
        }[nivel];
      }
    },
    data() {
      return {
        zoom:8,
        map_center: L.latLng(43, -8),
        url:'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution:'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      }
    },
    computed: {
      marker_posicion() {
        return L.latLng(this.position.lat, this.position.lon);
      },
      marker_centro() {
        return L.latLng(this.center.coor.lat,this.center.coor.lon);
      },
      show_data() {
        if (this.center == null) return false;
        return !!this.center.details;
      }
    },
    mounted() {
      $("#centerInfoModal").on("shown.bs.modal", this.onShown);
    }
  }
</script>

<style lang="scss" scoped>
  @import "~leaflet/dist/leaflet.css";
  @import "~leaflet-geosearch/assets/css/leaflet.css";

  .aqd-map-container {
    width: 100%;
    height: 300px;
  }

  .modal-dialog {
    max-height: 900px;
    max-width: 900px;
  }

  .infoCenter {

    display:grid;

    grid-template-columns: 1fr 1fr;

    &__info{
      grid-column: 1 / 1;
    }

    &__map {
      grid-column: 2 / 2;
    }

    &__ensinanzas {
      grid-column: 1 / span 2;

      &__ensinanza {
        margin: 0.4em 0;
        list-style: none;

        &__tipo, &__grado {
          padding: 0.1em;
          border: 0.25px solid black;
          border-radius: 15%;
        }

        &__tipo {
          background-color: red;
          font-size: 0.8em;
        }

        &__grado {
          background-color: yellow;
          font-size: 0.5em;
        }

        &__nome {
          margin-left: 0.5em;
        }
      }
    }

    &__routeinfo {
      margin-top: 1em;
    }
  }

  .cat-icon {
    display: inline-block;
    height: 15px;
    width: 15px;

    margin-right: 1px;
    padding: 0;
    padding-bottom: 1px;
    border-radius: 100%;

    text-align: center;
    font-style: normal;
    font-size: 0.8em;
    font-weight: bold;
    color: white;

    &--1 {background-color: green}
    &--2 {background-color: orange}
    &--3 {background-color: red}
  }

  .cat-info {
    font-size: 8px;
    margin: 0;
    padding: 0;
    line-height: 10px;

    &::before {
      content: "("
    }

    &::after {
      content: ")"
    }
  }

  table {
    margin: auto;

    th {
      text-align: center;
      font-size: 0.8em;
    }

    td,th:not(:first-child) {
      width: 80px;
      border: rgba(0, 0, 0, 0.25) 0.5px solid;
      border-top: none;
      border-bottom: none;
      padding: 0 0.3em;
    }
  }

</style>


<i18n>
  {
    "gl": {
      "title": "Detalles do centro",
      "loading": "Cargando...",
      "name": "Nome",
      "cod": "Código",
      "cp": "Código Postal",
      "address": "Enderezo",
      "tlf": "Teléfono",
      "web": "Web"
    },
    "es": {
      "title": "Detalles do centro",
      "loading": "Cargando...",
      "name": "Nombre"
    }
  }
</i18n>
