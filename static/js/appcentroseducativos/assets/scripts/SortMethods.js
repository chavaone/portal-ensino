export default {
  sortByName(centro1, centro2) {
    return centro1.nome.localeCompare(centro2.nome);
  },
  sortByTime(centro1, centro2) {
    if (! centro1.osm.tiempo) return 1;
    if (! centro2.osm.tiempo) return -1;
    return centro1.osm.tiempo - centro2.osm.tiempo;
  },
  sortByDistance(centro1, centro2) {
    if (! centro1.osm.distancia) return 1;
    if (! centro2.osm.distancia) return -1;
    return centro1.osm.distancia - centro2.osm.distancia;
  }
}
