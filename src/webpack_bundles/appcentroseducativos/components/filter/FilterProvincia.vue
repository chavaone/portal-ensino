<template lang="html">
  <div class="filter">
    <h5>{{ $t('provinces') }}</h5>
    <div class="filterList">
      <span v-for="(provincia, key) in provincias"
            :class="{active: checkedProvincias.indexOf(key) != -1}"
            @click="addOrDeleteProvincia(key)">
        {{provincia}}
      </span>
    </div>
    <div class="no-flex-fallback">
      <div class="form-check"
           v-for="(provincia, key) in provincias">
        <input  type="checkbox"
                class="form-check-input"
                :value="key" :id="key + '-checkbox'"
                v-model="checkedProvincias"
                @change="filterChanged()">
        <label class="form-check-label"
        :for="key + '-checkbox'">
          {{provincia}}
        </label>
      </div>
    </div>
  </div>
</template>

<script>
import { eventBus } from '../../main.js';

export default {
  data : function() {
    return {
      provincias: {
        'AC': 'A Coruña',
        'LU': 'Lugo',
        'OU': 'Ourense',
        'PO': 'Pontevedra'
      },
      checkedProvincias: [
        'AC',
        'LU',
        'OU',
        'PO'
      ]
    };
  },
  methods: {
    filter(centro) {
      return this.checkedProvincias.indexOf(centro.prov) != -1;
    },
    filterChanged() {
      eventBus.$emit('filterOrSortChanged', 'filterProvincia');
    },
    addOrDeleteProvincia(provincia) {
      var index = this.checkedProvincias.indexOf(provincia);
      if(index == -1) {
        this.checkedProvincias.push(provincia);
      } else {
        this.checkedProvincias.splice(index, 1);
      }
      eventBus.$emit('filterOrSortChanged', 'filterProvincia');
    }
  }
}
</script>

<style lang="scss">
</style>

<i18n>
  {
    "gl": {
      "provinces": "Provincias:"
    },
    "es": {
      "provinces": "Provincias:"
    }
  }
</i18n>
