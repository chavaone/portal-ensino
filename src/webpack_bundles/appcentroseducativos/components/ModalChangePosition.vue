<template lang="html">
  <div class="modal fade"
       id="cambiarPosicionModal"
       tabindex="-1"
       role="dialog"
       aria-labelledby="cambiarPosicionModalLabel"
       aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="cambiarPosicionModalLabel">{{ $t('title')}}</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <p>{{$t('explicacion')}}</p>
          <div class="aqd-map-container">
            <l-map ref="map" :zoom="zoom" :center="center" @click="mapClicked">
              <l-tile-layer :url="url" :attribution="attribution" ></l-tile-layer>
              <l-marker :lat-lng="marker"></l-marker>
              <v-geosearch :options="geosearchOptions"></v-geosearch>
            </l-map>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import L from 'leaflet';
import { eventBus } from '../main.js';
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';
import { OpenStreetMapProvider } from 'leaflet-geosearch';
import VGeosearch from 'vue2-leaflet-geosearch/Vue2LeafletGeosearch';
import $ from "jquery";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'marker-icon-blue.png',
  iconUrl: 'marker-icon-blue.png',
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

export default {
  props: {
    position: Object
  },
  components: {
      LMap,
      LTileLayer,
      LMarker,
      VGeosearch },
  data() {
    return {
      zoom:8,
      center: L.latLng(43, -8),
      url:'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      geosearchOptions: { // Important part Here
        provider: new OpenStreetMapProvider(),
        style: 'bar',
        searchLabel: this.$i18n.t('search-label'),
        marker: {                                           // optional: L.Marker    - default L.Icon.Default
          icon: L.icon({
            iconUrl: 'marker-icon-red.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34]
          }),
          draggable: false,
        },
        maxMarkers: 6,
      },
    }
  },
  computed: {
    marker() {
      return L.latLng(this.position.lat, this.position.lon);
    }
  },
  methods:{
    onShown() {
      var self = this;
      setTimeout(function () {
        self.$refs.map.mapObject.invalidateSize();
      }, 500);
    },
    changedLocation() {
      eventBus.$emit('locationChanged', this.position);
    },
    mapClicked(e){
      //Not move pointer if geosearch control is clicked.
      if(e.originalEvent.target.parentElement.parentElement.className.indexOf('geosearch') != -1 || e.originalEvent.target.parentElement.parentElement.parentElement.className.indexOf('geosearch') != -1) return;

      this.position.lat = e.latlng.lat;
      this.position.lon = e.latlng.lng;
      this.changedLocation();
    }
  },
  mounted() {
    $("#cambiarPosicionModal").on("shown.bs.modal", this.onShown);
  }
}

</script>

<style lang="scss">
  @import "~leaflet/dist/leaflet.css";
  @import "~leaflet-geosearch/assets/css/leaflet.css";

  .aqd-map-container {
    width: 100%;
    height: 75vh;
  }

  .modal-dialog {
    width: 80vw !important;
    height: 80v h !important;
    max-height: 100%;
    max-width: 100% !important;
  }

</style>

<i18n>
  {
    "gl": {
        "title": "Cambiar Localizaci??n",
        "explicacion": "Para cambiar a localizaci??n fai click no mapa. O punteiro azul marca a localizaci??n actual da aplicaci??n. Tam??n podes empregar a barra de busca para procurar algunhas r??as. Unha vez atopada a posici??n que queres preme no mapa para marcala.",
        "search-label": "Introduza enderezo"
    },
    "es": {
        "title": "Cambiar Localizaci??n",
        "explicacion": "Para cambiar la localizaci??n haz click en el mapa. El puntero azul marca a localizaci??n actual de la aplicaci??n. Tambi??n puedes usar a barra de busqueda para encontrar algunhas calles. Una vez encontrada la posici??n que quieres, haz click en el mapa para marcala.",
        "search-label": "Introduzca direcci??n"
    }
  }
</i18n>
