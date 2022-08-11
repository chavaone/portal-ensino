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
          <section class="modal-block">
            <h5>{{ $t('current-segment')}}</h5>

            <p v-html="$t('exp-segment')"></p>

            <code id="listaCodigos" class="codigos" @copy="onCopy()">{{segmentString}}</code>
            <div class="btn-group acciones" role="group" aria-label="Acciones">
              <div class="btn-group" role="group">
                <button id="btnGroupDescargaSegmento" type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">{{ $t('download-segment')}}</button>
                <div class="dropdown-menu" aria-labelledby="btnGroupDrop1">
                  <a class="dropdown-item" :href="'data:text/plain;charset=utf-8,' + encodeURIComponent(segmentString)" :download="$t('download-segment-txt-name')">{{$t('download-segment-txt')}}</a>
                  <a class="dropdown-item" :href="'data:text/csv;charset=utf-8,' + encodeURIComponent(segmentCSV)" :download="$t('download-segment-csv-name')">{{$t('download-segment-csv')}}</a>
                  <a class="dropdown-item" @click="downloadPDF">{{$t('download-segment-pdf')}}</a>
                </div>
              </div>
              <button class="btn btn-primary" type="button" name="button" @click="copy" v-html="$t('copy-clipboard')"></button>
              <a class="btn btn-primary" data-toggle="collapse" href="#save_segment" role="button" aria-expanded="false" aria-controls="save_segment" >{{ $t('add-segment-list') }}</a>
            </div>

            <form class="needs-validation save-block collapse" novalidate id="save_segment">
                <p>{{$t('exp-add-segment')}}</p>
                <div class="form-group">
                  <label for="segmentName">{{$t('name')}}</label>
                  <input type="text" class="form-control" id="segmentName" v-model="segmentName">
                </div>
                <a class="btn btn-primary " @click="addListBottom()">{{$t('do-add-segment-list')}}</a>
            </form>
          </section>

          <section class="modal-block">

            <h5>{{ $t('current-list')}}</h5>
            <p v-html="$t('exp-list')"></p>

            <AQDDraggable v-if="list.length"  v-model="segment_list" @update="dragList()">
              <div v-for="(segmento, index) in segment_list" class="segmento">
                <span>{{segmento.nome}}</span>
                <code>{{segmento.codigos}}</code>
                <a @click="load(index)"><i class="fas fa-eye"></i></a>
                <a @click="remove(index)"><i class="fa fa-trash"></i></a>
              </div>
            </AQDDraggable>
            <p v-else>{{ $t('empty-list')}}</p>

            <div class="btn-group" role="group">
              <button id="btnGroupDescargaSegmento" type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">{{ $t('download-list')}}</button>
              <div class="dropdown-menu" aria-labelledby="btnGroupDrop1">
                <a class="dropdown-item" :href="'data:text/plain;charset=utf-8,' + encodeURIComponent(activeListText)" :download="$t('download-list-txt-name')">{{$t('download-list-txt')}}</a>
                <a class="dropdown-item" :href="'data:application/json;charset=utf-8,' + encodeURIComponent(activeListJSON)" :download="$t('download-list-json-name')">{{$t('download-list-json')}}</a>
              </div>
              <a class="btn btn-primary" data-toggle="collapse" href="#save_list" role="button" aria-expanded="false" aria-controls="save_list" :class="{disabled: saved_list.result != 'ok'}">{{ $t('save-list') }}</a>
              <a class="btn btn-primary" data-toggle="collapse" href="#load_file_list" role="button" aria-expanded="false" aria-controls="load_file_list">{{ $t('load-list') }}</a>

            </div>

            <form class="needs-validation save-block collapse" novalidate id="save_list">
                <p>{{$t('exp-save-list')}}</p>
                <div class="form-group">
                  <label for="listName">{{$t('name')}}</label>
                  <input type="text" class="form-control" id="listName" v-model="listName">
                </div>
                <a class="btn btn-primary " @click="saveList()">{{$t('save')}}</a>
            </form>

            <div class="save-block collapse" id="load_file_list">
              <p>{{$t('exp-load-list')}}</p>
              <input type="file" @change="parseFile">
              <p>{{loadFileMessage}}</p>
            </div>
          </section>

          <section class="modal-block">
            <h5>{{$t('saved-lists')}}</h5>
            <p v-if="saved_list.result == 'not-loaded'">{{$t('loading')}}</p>
            <p v-else-if="saved_list.result == 'not-authenticated'">{{$t('not-authenticated')}}</p>
            <div v-else-if="saved_list.list.length">
              <div v-for="(lista, index) in saved_list.list" class="lista">
                <span>{{lista.titulo}}</span>
                <span class="lista__data">{{ lista.data | moment("from")}}</span>
                <a @click="askLoadRemoveList('load', index)"><i class="fas fa-eye"></i></a>
                <a @click="askLoadRemoveList('remove', index)" :style="{disabled: ! lista.deletable}"><i class="fa fa-trash"></i></a>
              </div>
            </div>
            <p v-else>{{$t('no-saved-lists')}}</p>

            <div class="save-block collapse" id="confirmList">
              <p>{{confirmSavedListMessage}}</p>
              <div class="btn-group">
                <a class="btn btn-primary " @click="loadRemoveList(1)">{{$t('yes')}}</a>
                <a class="btn btn-primary " @click="loadRemoveList(0)">{{$t('no')}}</a>
              </div>
            </div>
          </section>


        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import galite from 'ga-lite'
import jsPDF from 'jspdf';
import Draggable from 'vuedraggable'
import { eventBus } from '../main.js'
import $ from "jquery";

export default {
  props: {
    centers: Array,
    list: Array
  },
  computed: {
    segmentString () {
      return this.centers.map((center) => {return center.cod;}).join(" ");
    },
    segmentPDFText () {
      return this.centers.map((center) => {return "<p>" + center.cod + " - " + center.nome + "</p>";}).join("");
    },
    segmentCSV () {
      var header = "Código, Nome Centro, Concello, Provincia\n";
      var body   = this.centers.map((center) => {return center.cod + ", " + center.nome + ", " + center.con + ", " + center.prov  }).join("\n");
      return header + body;
    },
    activeListText(){
      return this.segment_list.map((seg) => {return seg.nome + "\n" + seg.codigos + "\n"}).join("\n");
    },
    activeListJSON(){
      return JSON.stringify(this.segment_list);
    }
  },
  data () {
    return {
      segmentName: "",
      listName: "",
      saved_list: {result: "not-loaded"},
      confirmSavedListMessage: "",
      savedListIndex: -1,
      savedListMethod: '',
      segment_list: [],
      loadFileMessage: ""
    }
  },
  components: {
    'AQDDraggable': Draggable
  },
  methods: {
    copy() {
      navigator.clipboard.writeText(this.segmentString);
      galite('send', 'event', 'export', 'copyCodes');
    },
    downloadPDF() {
      const CENTERS_PER_PAGE = 27;
      var lista = this.centers.map((center) => {return  center.cod + " - " + center.nome + " - " + center.con + "(" + center.prov +  ")";})
      const doc = new jsPDF();

      for (var i = 0; i < lista.length; i++) {
        var page_index = i % (CENTERS_PER_PAGE + 1);
        var y = 15 + 10 * page_index;
        doc.text(lista[i], 10, y);

        if (page_index == CENTERS_PER_PAGE) {
          doc.addPage();
        }
      }

      doc.save(this.$i18n.t('download-pdf-name'));
    },
    onCopy() {
      galite('send', 'event', 'export', 'copyCodes');
    },
    addListBottom() {
      var segmento = {
        nome: this.segmentName,
        codigos: this.segmentString
      };

      var nova_lista = this.segment_list;
      nova_lista.push(segmento);

      eventBus.$emit('changeList', nova_lista);
      this.segment_list = nova_lista;

      $('#save_segment').collapse('hide');
    },
    load(index) {
      eventBus.$emit('loadSegment', this.list[index].codigos);
    },
    remove (index) {
      var nova_lista = this.segment_list;
      nova_lista.splice(index, 1);

      eventBus.$emit('changeList', nova_lista);
      this.segment_list = nova_lista;
    },
    saveList() {
      var body = {
        titulo: this.listName,
        centros: this.list
      };

      this.$http.post('/centros/api/listas/', JSON.stringify(body)).then(function(response){
        this.saved_list = response.body;
      });

      $('#save_list').collapse('hide');
    },
    onShown() {
      this.$http.get('/centros/api/listas/').then(function(response) {
        this.saved_list = response.body;
      });
    },
    askLoadRemoveList(method, index) {
      this.savedListMethod = method;
      this.savedListIndex = index;

      this.confirmSavedListMessage = "Eliminar o cargar..."; //TODO

      $('#confirmList').collapse('toggle');
    },
    loadRemoveList(confirm) {
      if (confirm) {
          if (this.savedListMethod == 'load') {
            eventBus.$emit('changeList', this.saved_list.list[this.savedListIndex].centros);
            this.segment_list = this.saved_list.list[this.savedListIndex].centros;
          } else if (this.savedListMethod == 'remove') {
            this.$http.delete('/centros/api/listas/' + (this.saved_list.list[this.savedListIndex].pk)).then(function(response){
              this.saved_list = response.body;
            });
          }
      }

      $('#confirmList').collapse('hide');
    },
    dragList() {
      eventBus.$emit('changeList', this.segment_list);
    },
    parseFile(event) {
      var reader = new FileReader();
      var self = this;

      reader.onload = function(){
        var raw_list = JSON.parse(reader.result);
        try {
          var lista = []
          for (var i = 0; i < raw_list.length;i++) {
            const regex = new RegExp('([0-9]{8} )*[0-9]{8}');
            if(! regex.test(raw_list[i].codigos)) throw 'Formato non válido';

            lista.push({
              nome: raw_list[i].nome,
              codigos: raw_list[i].codigos
            });
          }

          eventBus.$emit('changeList', lista);
          self.segment_list = lista;

          self.loadFileMessage = "Ficheiro cargado correctamente!";
          $('#load_file_list').collapse('hide');

        } catch(e) {
          self.loadFileMessage = "Error cargando ficheiro.";
        }
      };

      reader.readAsText(event.target.files[0]);
    }
  },
  mounted() {
    $("#cambiarExportarCentros").on("shown.bs.modal", this.onShown);
    this.segment_list = this.list;
  }
}

</script>

<style lang="scss" scoped>
  .modal-dialog {
    width: 75vw !important;
    height: 90vh !important;

    max-height: 100%;
    max-width: 100% !important;
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
         opacity: 0.5;
       }

     }
  }

  .lista {
     display: grid;
     grid-template-columns: 1fr 175px  25px 25px;
     grid-auto-rows: 60px;
     align-items: center;
     grid-column-gap: 5px;

     a {
       text-align: center;

       &:hover {
         opacity: 0.5;
       }
     }

     &__data {
       font-size: 0.8em;
       font-style: italic;
       text-align: right;

       &::before {
         content: "(";
       }

       &::after {
         content: ")";
       }
     }
  }

  .save-block {
    border: rgba(0,0,0,0.25) solid 0.5px;
    padding: 1em;
    border-radius: 10px;
    margin: 0.5em 0;
  }

  .modal-block {
    padding-bottom: 1em;

    &:not(:last-child) {
      border-bottom: rgba(0,0,0,0.25) solid 0.5px;
      margin-bottom: 1.5em;
    }
  }

  #pdftext {
    display: none;
  }
</style>

<i18n>
  {
    "gl": {
      "current-segment": "Segmento actual",
      "exp-segment": "No seguinte bloque poderá ver os códigos dos centros que actualmente está filtrando.",
      "download-segment": "Descargar",
      "current-list": "Lista actual",
      "exp-list": "No seguinte bloque poderá ver a lista de segmentos que actualmente está creando. Pode reordear esta lista de segmentos, eliminar algún ou volvelo a cargar.",
      "empty-list": "Lista baleira",
      "download-list": "Descargar",
      "save-list": "Gardar lista",
      "load-list": "Cargar lista",
      "exp-save-list": "Para gardar unha lista nun ficheiro debe introducir o seu nome:",
      "name": "Nome",
      "save": "Gardar",
      "exp-load-list": "Para cargar unha lista dende un ficheiro JSON que anteriormente descargou deste sitio deberá seleccionar a localización do dito ficheiro na súa computadora:",
      "saved-lists": "Listas Gardadas",
      "download-segment-txt": "Descargar segmento como TXT",
      "download-segment-pdf": "Descargar segmento como PDF",
      "download-segment-csv": "Descargar segmento como CSV",
      "download-segment-txt-name": "segmento.txt",
      "download-segment-pdf-name": "segmento.pdf",
      "download-segment-csv-name": "segmento.csv",
      "download-list-txt": "Descargar lista como TXT",
      "download-list-json": "Descargar lista como JSON",
      "download-list-txt-name": "lista.txt",
      "download-list-json-name": "lista.json",
      "add-segment-list": "Engadir á lista",
      "title": "Cargar/Gardar centros",
      "copy-clipboard": "Copiar ó portapapeis",
      "not-authenticated": "Sen autenticar. Inicie sesión para ver as listas gardadas.",
      "loading": "Cargando...",
      "yes": "Si",
      "no": "Non",
      "exp-add-segment": "Para engadir o segmento actual ao final da lista actual debe darlle un nome ó segmento:",
      "do-add-segment-list": "Engadir"
    },
    "es": {
      "current-segment": "Segmento actual",
      "exp-segment": "En el siguiente bloque podrá ver los códigos de los centros que está actualmente filtrando.",
      "download-segment": "Descargar",
      "current-list": "Lista actual",
      "exp-list": "En el siguiente bloque podrá ver la lista de los segmentos que está actualmente creando. Puede reordenar esta lista de segmentos, eliminar alguno o volver a cargarlo.",
      "empty-list": "Lista vacia",
      "download-list": "Descargar",
      "save-list": "Guardar lista",
      "load-list": "Cargar lista",
      "exp-save-list": "Para guardar una lista en un fichero debe introdurcir su nombre:",
      "name": "Nombre",
      "save": "Guardar",
      "exp-load-list": "Para cargar una lista desde un fichero JSON que anteriormente descargó de este sitio, deberá seleccionar la localización de dicho fichero en su ordenador:",
      "saved-lists": "Listas Guardadas",
      "download-segment-txt": "Descargar segmento como TXT",
      "download-segment-pdf": "Descargar segmento como PDF",
      "download-segment-csv": "Descargar segmento como CSV",
      "download-segment-txt-name": "segmento.txt",
      "download-segment-pdf-name": "segmento.pdf",
      "download-segment-csv-name": "segmento.csv",
      "download-list-txt": "Descargar lista como TXT",
      "download-list-json": "Descargar lista como JSON",
      "download-list-txt-name": "lista.txt",
      "download-list-json-name": "lista.json",
      "add-segment-list": "Añadir a la lista",
      "title": "Cargar/Gardar centros",
      "copy-clipboard": "Copiar al portapapeles",
      "not-authenticated": "Sin autenticar. Inicie sesión para ver las listas guardadas.",
      "loading": "Cargando...",
      "yes": "Si",
      "no": "No",
      "exp-add-segment": "Para añadir el segmento actual al final de la lista actual, debe darle un nombre al segmento:",
      "do-add-segment-list": "Añadir"
    }
  }
</i18n>
