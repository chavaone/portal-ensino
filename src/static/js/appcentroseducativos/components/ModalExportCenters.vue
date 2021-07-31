<template lang="html">
  <div class="modal fade"
       id="cambiarExportarCentros"
       tabindex="-1"
       role="dialog"
       aria-labelledby="cambiarExportarCentrosModalLabel"
       aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="cambiarExportarCentrosLabel" v-html="$t('title')"></h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <p v-html="$t('explicacion-1')"></p>
          <h5>Segmento Actual</h5>

          <code id="listaCodigos" class="codigos" @copy="onCopy()">{{centersString}}</code>
          <div class="btn-group acciones" role="group" aria-label="Acciones">

            <div class="btn-group" role="group">
              <button id="btnGroupDescargaSegmento" type="button" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Descargar
              </button>
              <div class="dropdown-menu" aria-labelledby="btnGroupDrop1">
                <a class="dropdown-item" :href="'data:text/plain;charset=utf-8,' + encodeURIComponent(centersString)" :download="$t('download-txt-name')" v-html="$t('download-txt')"></a>
                <a class="dropdown-item" @click="downloadPDF" v-html="$t('download-pdf')"></a>
              </div>
            </div>
            <button class="btn btn-primary" type="button" name="button" @click="copy" v-html="$t('copy-clipboard')"></button>
            <a class="btn btn-primary" data-toggle="collapse" href="#save_segment" role="button" aria-expanded="false" aria-controls="save_segment">Engadir á lista</a>
          </div>

          <form class="needs-validation save-block collapse" novalidate id="save_segment">
              <p>Inclúe o nome do segmento para gardalo:</p>
              <div class="form-group">
                <label for="segmentName">Nome</label>
                <input type="text" class="form-control" id="segmentName" v-model="segmentName">
              </div>
              <a class="btn btn-primary " @click="addListBottom()">Engadir</a>
          </form>

          <h5>Lista Actual</h5>
          <AQDDraggable v-if="list.length"  v-model="list">
            <div v-for="(segmento, index) in list" class="segmento">
              <span>{{segmento.nome}}</span>
              <code>{{segmento.codigos}}</code>
              <a @click="load(index)"><i class="fas fa-eye"></i></a>
              <a @click="remove(index)"><i class="fa fa-trash"></i></a>
            </div>
          </AQDDraggable>
          <p v-else>Baleira</p>

          <div class="btn-group" role="group">
            <button id="btnGroupDescargaSegmento" type="button" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Descargar
            </button>
            <div class="dropdown-menu" aria-labelledby="btnGroupDrop1">
              <a class="dropdown-item" :href="'data:text/plain;charset=utf-8,' + encodeURIComponent(activeListText)" :download="$t('download-txt-list-name')" v-html="$t('download-txt')"></a>
              <a class="dropdown-item" :href="'data:application/json;charset=utf-8,' + encodeURIComponent(activeListJSON)" :download="$t('download-json-list-name')" v-html="$t('download-json')"></a>
            </div>
          </div>
        </div>

        <div id="pdftext" class="hidden" v-html="centersList"></div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import galite from 'ga-lite'
import jsPDF from 'jspdf'
import Draggable from 'vuedraggable'
import { eventBus } from '../main.js'

export default {
  props: {
    centers: Array,
    list: Array
  },
  computed: {
    centersString () {
      return this.centers.map((center) => {return center.cod;}).join(" ");
    },
    centersList () {
      return this.centers.map((center) => {return "<p>" + center.cod + " - " + center.nome + "</p>";}).join("");
    },
    activeListText(){
      return this.list.map((seg) => {return seg.nome + "\n" + seg.codigos + "\n"}).join("\n");
    },
    activeListJSON(){
      return JSON.stringify(this.list);
    }
  },
  data () {
    segmentName: ""
  },
  components: {
    'AQDDraggable': Draggable
  },
  methods: {
    copy() {
      navigator.clipboard.writeText(this.centersString);
      galite('send', 'event', 'export', 'copyCodes');
    },
    downloadPDF() {
      var doc = new jsPDF();
      doc.fromHTML(document.getElementById('pdftext').innerHTML, 15, 15, {
        'width': 170
      });
      galite('send', 'event', 'export', 'downloadPDF');
      doc.save(this.$i18n.t('download-pdf-name'));
    },
    onCopy() {
      galite('send', 'event', 'export', 'copyCodes');
    },
    addListBottom() {
      var segmento = {
        nome: this.segmentName,
        codigos: this.centersString
      };

      this.list.push(segmento);

      eventBus.$emit('filterOrSortChanged', 'filterCurrentList');

      $('#save_segment').collapse('hide');
    },
    load(index) {
      eventBus.$emit('loadSegment', this.list[index].codigos);
    },
    remove (index) {
      this.list.splice(index, 1);
    }
  }
}

</script>

<style lang="scss">
  .modal-dialog {
    width: 90vw !important;
    height: 90vh !important;

    max-height: 100%;
    max-width: 100%;
  }

  code.codigos {
    height: 95px;
    display: block;
    overflow-y: scroll;
    border: rgba(0,0,0,0.2) solid 0.5px;
    border-radius: 7px;
    padding: 5px;
    margin: 1em 0;
  }

  .acciones {
      display: flex;
      margin: 1em 0;
      justify-content: center;
  }

  .segmento {
     display: grid;
     grid-template-columns: 200px 1fr 25px 25px;
     grid-auto-rows: 60px;
     align-items: center;

     code {
       display: block;
       overflow-y: hidden;
       border: rgba(0,0,0,0.2) solid 0.5px;
       border-radius: 7px;
       padding: 5px;
       margin: 1em 0.3em;
       align-self: stretch;
     }

     a {
       text-align: center;

       &:hover {
         opacity: 0.8em;
       }

     }
  }

  .save-block {
    border: rgba(0,0,0,0.25) solid 0.5px;
    padding: 1em;
    margin-bottom: 2em;
    border-radius: 10px;
  }

  #pdftext {
    display: none;
  }
</style>

<i18n>
  {
    "gl": {
      "download-txt": "Descargar como ficheiro de texto",
      "download-pdf": "Descargar como PDF",
      "download-txt-name": "centros.txt",
      "download-pdf-name": "centros.pdf",
      "title": "Exportar Centros",
      "copy-clipboard": "Copiar ó portapapeis",
      "explicacion-1": "No seguinte cadro podes ver os códigos de todos os centros que tiñas na lista por orde:"
    },
    "es": {
      "download-txt": "Descargar como ficheiro de texto",
      "download-pdf": "Descargar como PDF",
      "download-txt-name": "centros.txt",
      "download-pdf-name": "centros.pdf",
      "title": "Exportar Centros",
      "copy-clipboard": "Copiar al portapapeles",
      "explicacion-1": "En el siguiente cuadro puedes ver los códigos de todos los centros que tenías en la lista por orden:"
    }
  }
</i18n>
