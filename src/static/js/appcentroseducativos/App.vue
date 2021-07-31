<template>
  <div id="app">
      <nav class="appnav">
        <span class="info">{{ $t('number-centers', [currentPage + 1, totalPages, activeCenters.length]) }}</span>
        <span class="boton">
          <a class="btn btn-primary" data-toggle="collapse" href="#asideSortFilter" role="button" aria-expanded="false" aria-controls="asideSortFilter">Filtros</a>
        </span>
        <AQDTrash ref="trash"></AQDTrash>
      </nav>
      <div class="appmain">
        <aside class="appmain__bar collapse" id="asideSortFilter">
          <form>
            <AQDSortControl ref="sortList"></AQDSortControl>
            <AQDFilterList ref="filterList"></AQDFilterList>
          </form>
        </aside>
        <div class="appmain__content">
          <AQDDraggable v-if="activeCenters.length > 0"  v-model="activeCenters" @change="setCustomSort()" :options="sortableoptions" class="mainCenterList">
              <AQDCenter v-for="centro in paginatedActiveCenters" :centro="centro" :key="centro.cod"></AQDCenter>
          </AQDDraggable>
          <nav class="center-pagination" v-if="activeCenters.length > 0">
            <ul class="pagination">
              <li class="page-item"
                  :class="{disabled: currentPage == 0}">
                <a class="page-link" href="#" tabindex="-1" @click="currentPage--">{{ $t('anterior') }}</a>
              </li>
              <li v-for="page in totalPages"
                  class="page-item"
                  :class="{active: currentPage == page - 1}">
                <a  class="page-link"
                    @click="currentPage = page - 1;"
                >{{page}}</a>
              </li>
              <li class="page-item" :class="{disabled: currentPage == totalPages - 1}">
                <a class="page-link" @click="currentPage++;">{{ $t('seguinte') }}</a>
              </li>
            </ul>
          </nav>
          <AQDLandingMessage v-if="activeCenters.length == 0" :loadedDistances="loadedDistances" :loadedTimes="loadedTimes"></AQDLandingMessage>
        </div>
      </div>
      <AQDModalChangePosition :position="position"></AQDModalChangePosition>
      <AQDModalExportCenters :centers="activeCenters" :list="activeList"></AQDModalExportCenters>
      <AQDModalCenterInfo :center="active_center_details" :position="position" ref="modalInfo"></AQDModalCenterInfo>
  </div>
</template>

<script>
import { eventBus } from './main.js'
import OSMFunctions from './assets/scripts/OSMFunctions.js'
import MetaData from './assets/scripts/MetaDataValues.js'
import Config from './config.js'

var raw_centers_db;

//Components
import Draggable from 'vuedraggable'
import Center from './components/Center.vue'
import MainHeaderBar from './components/MainHeaderBar.vue'
import FilterList from './components/filter/FilterList.vue'
import SortList from './components/sort/SortList.vue'
import Trash from './components/Trash.vue'
import LandingMessage from './components/LandingMessage.vue'
import ModalChangePosition from './components/ModalChangePosition.vue'
import ModalExportCenters from './components/ModalExportCenters.vue'
import ModalCenterInfo from './components/ModalCenterInfo.vue'

export default {
  metaInfo: MetaData,
  data () {
    return {
      activeCenters: [],
      activeList:[],
      position: {
        'lat': 43,
        'lon': -8
      },
      loadedDistances: false,
      loadedTimes: false,
      currentPage: 0,
      resultCount: 0,
      sortableoptions: {
        handle: 'h3.name',
      },
      active_center_details: null
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.resultCount / Config.centersPerPage);
    },
    paginatedActiveCenters() {
      this.resultCount = this.activeCenters.length;

      if (this.currentPage >= this.totalPages) {
        this.currentPage = Math.max(0, this.totalPages - 1);
      }

      var index = this.currentPage * Config.centersPerPage;

      return this.activeCenters.slice(index, index + Config.centersPerPage);
    }
  },
  components: {
    'AQDDraggable': Draggable,
    'AQDCenter': Center,
    'AQDFilterList': FilterList,
    'AQDMainHeaderBar': MainHeaderBar,
    'AQDSortControl': SortList,
    'AQDTrash': Trash,
    'AQDLandingMessage': LandingMessage,
    'AQDModalChangePosition': ModalChangePosition,
    'AQDModalExportCenters': ModalExportCenters,
    'AQDModalCenterInfo': ModalCenterInfo
  },
  methods: {
    loadCenters() {
      var showCenters =  raw_centers_db;
      showCenters = this.$refs.filterList.filter(showCenters);
      showCenters = showCenters.filter(this.$refs.trash.filter);
      showCenters = showCenters.filter(this.filterCurrentList);
      showCenters = this.$refs.sortList.sort(showCenters);

      this.activeCenters = showCenters;
    },
    getLocation() {
      var self = this;
      navigator.geolocation.getCurrentPosition (function(pos) {
            self.position = {
                lat: pos.coords.latitude,
                lon: pos.coords.longitude
            };
            eventBus.$emit('locationChanged', self.position);
        });
    },
    updateOSMData(position) {
      this.loadedTimes = false;
      this.loadedDistances = false;
      var self = this;

      //Reset OSM details
      raw_centers_db.forEach(function(center){
        center.osm = {
          distancia: 0,
          tiempo: 0,
          details: null,
          routeData: null
        };
      });

      OSMFunctions.updateOSMTimes(raw_centers_db, position, function () {
        self.loadedTimes = true;
      });

      OSMFunctions.updateOSMDistances(raw_centers_db, position, function () {
        self.loadedDistances = true;
      });
    },
    filterCurrentList(center) {
      for(var i= 0; i < this.activeList.length; i++) {
        if (this.activeList[i].codigos.includes(center.cod)) return false;
      };
      return true;
    },
    setCustomSort() {
      this.$refs.sortList.setCustomSort();
    },
    dbLoaded(response) {

      raw_centers_db = response.body;

      //We add trashed field so this field is 'reactified'.
      raw_centers_db.forEach(function(center){
        center.trashed = false;
        center.osm = {
          distancia: 0,
          tiempo: 0,
          details: null,
          loading: false
        };
        center.details = {}
      });
      this.getLocation();
    },
    resetCenters() {
      this.activeCenters = [];
    },
    getOSMCenterDetails (centro) {
      OSMFunctions.getOSMDetailedRouteInfo(centro, this.position, function () {});
    },
    getCenterDetails (centro) {
      this.active_center_details = centro;
      if (! this.active_center_details.details) {
        this.$http.get('/centros/api/centro/' + centro.cod).then(function(response) {
          this.active_center_details.details = response.body;
        });
      }
      $('#centerInfoModal').modal('show');
    },
    loadSegment(segmentList) {
      console.log(segmentList);
      var lista_codigos = segmentList.split(" "),
          show_centers = [];

      for (var i = 0; i < lista_codigos.length; i++) {
        var centro = raw_centers_db.find(centro => centro.cod == lista_codigos[i]);
        show_centers.push(centro);
      }

      this.activeCenters = show_centers;

    }
  },
  created() {
    eventBus.$on('locationChanged', this.updateOSMData);
    eventBus.$on('locationChanged', this.resetCenters);
    eventBus.$on('filterOrSortChanged', this.resetCenters);
    eventBus.$on('loadCenters', this.loadCenters);
    eventBus.$on('osmcenterdetails', this.getOSMCenterDetails);
    eventBus.$on('centerdetails', this.getCenterDetails);
    eventBus.$on('loadSegment', this.loadSegment);

    this.$http.get('/centros/api').then(this.dbLoaded);
  }
}
</script>

<style lang="scss">
  @import "./assets/styles/variables.scss";
  @import "~bootstrap/scss/bootstrap.scss";
  @import "./assets/styles/mixins.scss";


  .appnav {
    @include make-box;
    @include make-row;

    margin: 0.7em 0;
    align-items: center;
    justify-content: flex-start;

    .info {
      font-size:0.75em;
    }

    .boton {
      text-align: right;
      flex: 1;
    }

    @include media-breakpoint-up(md) {
      .boton {
        display:none;
      }

      #sortBar {
        display: inline-block;
        text-align: right;
        flex: 1;
      }
    }
  }

  .appmain {

    @include make-row();
    display: flex !important;

    &__bar {
      @include make-col-ready();
      @include make-col(12);
      margin-bottom: 1em;
      padding-right: 0;

      @include media-breakpoint-up(md) {
        @include make-col(3);
        display: inline-block !important;
      }

      &>form {
        @include make-box;
      }
    }

    &__content {
      @include make-col-ready();
      @include make-col(12);

      @include media-breakpoint-up(md) {
          @include make-col(9);
      }

      .pagination {
        justify-content: center;
        flex-wrap: wrap;
      }
    }
  }
</style>

<i18n>
  {
    "gl": {
      "number-centers": "Amosando a páxina {0} de {1} para un total de {2} centros",
      "seguinte": "Seguinte",
      "anterior": "Anterior"
    },
    "es": {
      "number-centers": "Mostrando la página {0} de {1} para un total de {2} centros",
      "seguinte": "Siguiente",
      "anterior": "Anterior"
    }
  }
</i18n>
