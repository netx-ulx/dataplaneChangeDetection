/*********************************************************
***************** BIT-SHIFT  FUNCTION ********************
**********************************************************/

void forecastShift(inout metadata meta) {
    if (ALPHA == 125){
        meta.aux_forecast = meta.forecast >> 1;
        meta.aux_forecast = meta.aux_forecast + meta.forecast >> 2;
        meta.aux_forecast = meta.aux_forecast + meta.forecast >> 3;
    } else if (ALPHA == 25){
        meta.aux_forecast = meta.forecast >> 1;
        meta.aux_forecast = meta.aux_forecast + meta.forecast >> 2;
    } else if (ALPHA == 375){
        meta.aux_forecast = meta.forecast >> 1;
        meta.aux_forecast = meta.aux_forecast + meta.forecast >> 3;
    } else if (ALPHA == 5){
        meta.aux_forecast = meta.forecast >> 1;
    } else if (ALPHA == 625){
        meta.aux_forecast = meta.forecast >> 2;
        meta.aux_forecast = meta.aux_forecast + meta.forecast >> 3;
    } else if (ALPHA == 75){
        meta.aux_forecast = meta.forecast >> 2;
    } else if (ALPHA == 875){
        meta.aux_forecast = meta.forecast >> 3;
    }
}

 void observedShift(inout metadata meta) {
    if (ALPHA == 125){
        meta.obs = SKETCH_UPDATE >> 3;
    } else if (ALPHA == 25){
        meta.obs = SKETCH_UPDATE >> 2;
    } else if (ALPHA == 375){
        meta.obs = SKETCH_UPDATE >> 2;
        meta.obs = meta.obs + SKETCH_UPDATE >> 3;
    } else if (ALPHA == 5){
        meta.obs = SKETCH_UPDATE >> 1;
    } else if (ALPHA == 625){
        meta.obs = SKETCH_UPDATE >> 1;
        meta.obs = meta.obs + SKETCH_UPDATE >> 3;
    } else if (ALPHA == 75){
        meta.obs = SKETCH_UPDATE >> 1;
        meta.obs = meta.obs + SKETCH_UPDATE >> 2;            
    } else if (ALPHA == 875){
        meta.obs = SKETCH_UPDATE >> 1;
        meta.obs = meta.obs + SKETCH_UPDATE >> 2;
        meta.obs = meta.obs + SKETCH_UPDATE >> 3;
    }
}