//THIS FILE WAS RAN IN GOOGLE EARTH ENGINE

var table = ee.FeatureCollection("TIGER/2016/Counties")
var ar = table.filterMetadata('STATEFP','equals','05')
//Map.addLayer(ar)

//var washington = table.filterMetadata('GEOID','equals','05143')

var NLCD = ee.ImageCollection("USGS/NLCD_RELEASES/2021_REL/NLCD")
            .select('landcover')
            .first()
            .clip(ar)
//print(NLCD)
 
var agMask = NLCD.updateMask(NLCD.eq(81).or(NLCD.eq(82)));
//Map.addLayer(agMask)
var forMask = NLCD.updateMask(NLCD.eq(41).or(NLCD.eq(42)).or(NLCD.eq(43)));

var urbMask = NLCD.updateMask(NLCD.eq(21).or(NLCD.eq(22)).or(NLCD.eq(23)).or(NLCD.eq(24)));

var calcLandCover = function(county) {
  var county_name = county.get('NAME') // i.e. 'NAME' equals 'Washington"
  
  var pixelArea = ee.Image.pixelArea();
  
  var agArea = agMask.multiply(pixelArea).reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: county.geometry(),
    scale: 30, //NLCD 30 m resolution
    maxPixels: 1e9
  });
  var forArea = forMask.multiply(pixelArea).reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: county.geometry(),
    scale: 30, //NLCD 30 m resolution
    maxPixels: 1e9
  });
  var urbArea = urbMask.multiply(pixelArea).reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: county.geometry(),
    scale: 30, //NLCD 30 m resolution
    maxPixels: 1e9
  });
  
  var totArea = NLCD.multiply(pixelArea).reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: county.geometry(),
    scale: 30, //NLCD 30 m resolution
    maxPixels: 1e9
  })
  
  var percentAg = (agArea.getNumber('landcover'))
                  .divide(totArea.getNumber('landcover'))
                  .multiply(100);
  var percentFor = (forArea.getNumber('landcover'))
                  .divide(totArea.getNumber('landcover'))
                  .multiply(100);
  var percentUrb = (urbArea.getNumber('landcover'))
                  .divide(totArea.getNumber('landcover'))
                  .multiply(100);
                  
  return county.set({'AgPer':percentAg,
                     'ForPer':percentFor,
                     'UrbPer':percentUrb
  })
};


var results = ar.map(calcLandCover);

Export.table.toDrive({
  collection: results,
  description: 'Arkansas_LandCover_Percent',
  fileFormat: 'CSV',
  selectors: ['COUNTY', 'AgPer', 'ForPer', 'UrbPer']
});
