/*
======================================
======================================

THIS FILE IS TO BE RUN AT THE BEGINNING OF EACH GENERIC SEASON

File generates a plane of grass. Upon this plane is where everything is placed.
Random number generation is used to determine what spawns in the environment.

======================================
======================================
 */

const chanceOcean = Math.round(Math.random() * 100);

function createLakes() {
  
 }

function assign(heights) {

}

function generateTerrain() {
    var terrainHeights = [];
    let mapsize = 800;
    for (var i = 0; i < mapsize; i++) {
      value = Math.random() * 1;
      rounded = Math.round(value * 10) / 10;
      terrainHeights.push(rounded);
    }
    assign(terrainHeights)
}
