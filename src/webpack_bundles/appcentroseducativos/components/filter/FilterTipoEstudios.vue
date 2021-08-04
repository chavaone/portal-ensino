<template lang="html">
  <div class="filter">
    <h5>{{ $t('studiestype') }}</h5>
    <div class="">
      <div class="filterList">
        <span v-for="tipo in tiposDeEstudios"
              :class="{active: checkedTiposDeEstudios.indexOf(tipo.cod) != -1}"
              @click="addOrDeleteEstudio(tipo.cod)"
              v-t="tipo.nombre"></span>
      </div>
      <div class="filterList action-buttons">
        <span @click="disableAll();">{{ $t('disable-all') }}</span>
        <span @click="enableAll();">{{ $t('enable-all') }}</span>
      </div>
    </div>
    <div class="no-flex-fallback">
      <div class="form-check"
           v-for="tipo in tiposDeEstudios">
        <input  type="checkbox"
                class="form-check-input"
                :value="tipo.cod" :id="tipo.cod + '-checkbox'"
                v-model="checkedTiposDeEstudios"
                @change="filterChanged()">
        <label  class="form-check-label"
                :for="tipo.cod + '-checkbox'"
                v-t="tipo.nombre"></label>
      </div>
    </div>
  </div>
</template>

<script>
import { eventBus } from '../../main.js';

export default {
  data : function() {
    return {
      //The property 'nombre' is the key to be translated by VueI18n.
      tiposDeEstudios: [
        {
          nombre: 'infantil',
          cod: 'INF'
        },
        {
          nombre: 'primaria',
          cod: 'PRI'
        },
        {
          nombre: 'eso',
          cod: 'ESO'
        },
        {
          nombre: 'bac',
          cod: 'BAC'
        },
        {
          nombre: 'esa',
          cod: 'ESA'
        },
        {
          nombre: 'esp',
          cod: 'ESP'
        },
        {
          nombre: 'fp',
          cod: 'FP'
        },
        {
          nombre: 'musica',
          cod: 'MUS'
        },
        {
          nombre: 'art-des',
          cod: 'ARDE'
        },
        {
          nombre: 'idiomas',
          cod: 'IDI'
        },
        {
          nombre: 'danza',
          cod: 'DAN'
        },
        {
          nombre: 'dramatico',
          cod: 'ARDR'
        }
      ],
      checkedTiposDeEstudios: []
    };
  },
  methods: {
    filter(centro) {
      for(var i = 0; i < this.checkedTiposDeEstudios.length; i++) {
        if (centro.ens.indexOf(this.checkedTiposDeEstudios[i]) != -1)
          return true;
      }
      return false;
    },
    filterChanged() {
      eventBus.$emit('filterOrSortChanged', 'filterTipoDeEstudios');
    },
    addOrDeleteEstudio(est) {
      var index = this.checkedTiposDeEstudios.indexOf(est);
      if(index == -1) {
        this.checkedTiposDeEstudios.push(est);
      } else {
        this.checkedTiposDeEstudios.splice(index, 1);
      }
      eventBus.$emit('filterOrSortChanged', 'filterTipoDeEstudios');
    },

    enableAll() {
      this.checkedTiposDeEstudios = this.tiposDeEstudios.map((c)=>{return c.cod;});
      eventBus.$emit('filterOrSortChanged', 'filterTipoDeEstudios');
    },
    disableAll() {
      this.checkedTiposDeEstudios = [];
      eventBus.$emit('filterOrSortChanged', 'filterTipoDeEstudios');
    }
  },
  created(){
    this.checkedTiposDeEstudios = this.tiposDeEstudios.map((c)=>{return c.cod;});
  }
}
</script>

<style lang="scss">
</style>

<i18n>
  {
    "gl": {
      "studiestype": "Estudos:",
      "infantil": "Infantil",
      "primaria": "Primaria",
      "eso": "ESO",
      "bac": "BAC",
      "esa": "ESO de Adultos",
      "esp": "Educación Especial",
      "fp": "FP",
      "musica": "Música",
      "art-des": "Arte e Deseño",
      "idiomas": "Idiomas",
      "dramatico": "Arte Dramático",
      "danza": "Danza",
      "disable-all": "Desactivar todas",
      "enable-all": "Activar todas"
    },
    "es": {
      "studiestype": "Estudios:",
      "infantil": "Infantil",
      "primaria": "Primaria",
      "eso": "ESO",
      "bac": "BAC",
      "esa": "ESO de Adultos",
      "esp": "Educación Especial",
      "fp": "FP",
      "musica": "Música",
      "art-des": "Arte y Diseño",
      "idiomas": "Idiomas",
      "dramatico": "Arte Dramático",
      "danza": "Danza",
      "disable-all": "Desactivar todas",
      "enable-all": "Activar todas"
    }
  }
</i18n>
