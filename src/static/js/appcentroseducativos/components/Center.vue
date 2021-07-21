<template lang="html">
  <article :data-cod="centro.cod" :class="{trashed: centro.trashed}" class="centro">
        <div class="info">
            <header>
                <h3 class="name">{{centro.nome}}</h3>
                <h5 class="city">{{centro.con}}, {{centro.prov}}</h5>
              </header>
            <div class="travel-info">
                <span class="travel-info__title">{{ $t('info-travel') }}</span>

                <div class="travel-info__content">

                  <span class="travel-info__item">
                    <i class="fas fa-route"></i>
                    {{prettyDistance}}
                    <span class="travel-info__itemmore" v-if="centro.osm.routeData">
                      <span v-if="showTIDistance('cat1')">
                        <span class="cat-icon cat-icon--1">1</span>{{ beautifyDistance(centro.osm.routeData.cat1.distancia/1000)}}
                      </span>
                      <span v-if="showTIDistance('cat2')">
                        <span class="cat-icon cat-icon--2">2</span>{{ beautifyDistance(centro.osm.routeData.cat2.distancia/1000)}}
                      </span>
                      <span v-if="showTIDistance('cat3')">
                        <span class="cat-icon cat-icon--3">3</span>{{ beautifyDistance(centro.osm.routeData.cat3.distancia/1000)}}
                      </span>
                    </span>
                  </span>

                  <span class="travel-info__item">
                    <i class="fas fa-clock"></i>
                    {{prettyTime}}
                    <span class="travel-info__itemmore" v-if="centro.osm.routeData">
                      <span v-if="showTITime('cat1')">
                        <span class="cat-icon cat-icon--1">1</span>
                        <span>{{ beautifyTime(centro.osm.routeData.cat1.tiempo)}}</span>
                      </span>
                      <span v-if="showTITime('cat2')">
                        <span class="cat-icon cat-icon--2">2</span><span>{{ beautifyTime(centro.osm.routeData.cat2.tiempo)}}</span>
                      </span>
                      <span v-if="showTITime('cat3')">
                        <span class="cat-icon cat-icon--3">3</span><span>{{ beautifyTime(centro.osm.routeData.cat3.tiempo)}}</span>
                      </span>
                    </span>
                  </span>

                  <span class="travel-info__item" v-if="centro.osm.details">
                    <i class="fas fa-road"></i>
                    {{centro.osm.details.legs[0].summary}}
                  </span>
                </div>
            </div>
        </div>
        <div class="botones">
            <div class="btn-group pull-right btn-group-vertical" role="group" aria-label="Basic example">
              <button type="button"
                      class="btn btn-sm btn-primary"
                      v-clipboard:copy="centro.cod">
                      <i class="fa fa-clipboard"></i>
              </button>
              <button type="button" class="btn btn-sm btn-primary" @click="trash()"><i class="fa fa-trash"></i></button>
              <button type="button" class="btn btn-xs btn-primary" @click="getOSMDetails()" :class="{disabled: detailsCounter}"><i class="fas fa-map-signs"></i></button>
              <button type="button" class="btn btn-sm btn-primary" @click="getDetails()"><i class="fa fa-info"></i></button>
            </div>
        </div>
    </article>
</template>

<script>
import { eventBus } from '../main.js';
import OSMFunctions from '../assets/scripts/OSMFunctions.js';

export default {
  props: {
    centro: Object,
    detailsCounter: Date
  },
  computed: {
    prettyDistance() {
      if (! this.centro.osm) return "---";
      var distance = this.centro.osm.distancia;
      if (this.centro.osm.details) distance = this.centro.osm.details.distance/1000;
      return this.beautifyDistance(distance);
    },
    prettyTime () {
      if (! this.centro.osm) return "---";
      var seconds = this.centro.osm.tiempo;
      if (this.centro.osm.details) seconds = this.centro.osm.details.duration;
      return this.beautifyTime(seconds);
    }
  },
  methods: {
    trash(){
      this.centro.trashed = ! this.centro.trashed;
      eventBus.$emit('trashcenter', this.centro);
    },
    getOSMDetails() {
      eventBus.$emit('osmcenterdetails', this.centro);
    },
    getDetails() {
      eventBus.$emit('centerdetails', this.centro);
    },
    beautifyDistance(distance) {
      return OSMFunctions.beautifyDistance(distance);
    },
    beautifyTime (seconds) {
      return OSMFunctions.beautifyTime(seconds);
    },
    showTIDistance(cat) {
      return this.centro.osm.routeData[cat] && (this.centro.osm.routeData[cat].distancia > 500 || (this.centro.osm.details.distance < 1000 && this.centro.osm.routeData[cat].distancia > 0));
    },
    showTITime(cat) {
      return this.centro.osm.routeData[cat] && (this.centro.osm.routeData[cat].tiempo > 120 || (this.centro.osm.details.duration < 900 && this.centro.osm.routeData[cat].tiempo > 0))
    }
  }
}
</script>

<style lang="scss">
@import "./../assets/styles/mixins.scss";

article.centro {
  @include make-box;
  margin-bottom: 1em;

  display: flex;
  flex-wrap: wrap;

  .botones {
      flex: 1 1 50px;
      display: flex;
      justify-content: center;
      .btn { font-size: 1.25em;}

  }

  @media (min-width: 760px) {
    .botones {
      .btn { font-size: 1em;}
    }
  }

  .info {
      flex: 1 1 calc(100% - 50px);

      header {
        border-bottom: 1px solid rgba(0, 0, 0, 0.125);
        margin-bottom: 1em;

        .city {
          font-style: italic;
          font-size: 0.9em;
        }

        .city::before {
          content: "(";
        }

        .city::after {
          content: ")";
        }
      }

      .travel-info {
        padding-left: 1em;

        &__title {
            font-weight: bold;
            margin-right: 0.5em;
        }

        &__content {
            display: inline-grid;
        }

        &__item {
          font-style: italic;

          svg {
              margin-right: 0.2em;
          }
        }

        &__itemmore {
          font-size:0.8em;
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
  }

  .more-info {
    flex: 1 1 100%;

    margin-top: 1em;
    border-top: 1px solid rgba(0, 0, 0, 0.125);
    padding: 1em;


    dl {
      display: flex;
      flex-wrap: wrap;
      margin-bottom: 0;

      div {
        flex: 1 1 300px;
      }
    }
  }

  @media (min-width: 1000px) {
    grid-template-rows: [start-center] 95px [start-info] 1fr [end-center];

    .info {
      header>h3,
      header>.city {
        display: inline-block;
        margin-left: 0.5em;
      }
    }
  }

}

.mainCenterList article.trashed {
  display:none;
}
</style>

<i18n>
  {
    "gl": {
      "info-travel": "Info Viaxe:",
      "num-linhas": "Liñas",
      "xornada-inf": "Xornada de Educación Infantil",
      "xornada-prim": "Xornada de Educación Primaria",
      "telefono": "Teléfono",
      "fax": "Fax",
      "web": "Web",
      "email": "Enderezo email",
      "ramas-bac": "Ramas Bacharelato",
      "enderezo": "Enderezo",
      "servizos": "Servizos"
    },
    "es": {
      "info-travel": "Info Viaje:",
      "xornada-inf": "Jornada de Educación Infantil",
      "xornada-prim": "Jornada de Educación Primaria",
      "telefono": "Teléfono",
      "fax": "Fax",
      "web": "Web",
      "email": "Dirección email",
      "ramas-bac": "Ramas Bachillerato",
      "enderezo": "Direccioń",
      "servizos": "Servicios"
    }
  }
</i18n>
