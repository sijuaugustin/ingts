features_singlefamily = ["listprice", "postalcode", "latitude", "longitude", "view_weight",
                         "watersource_weight", "bedroomstotal", "bathroomsfull", "livingarea",
                         "buildingareatotal", "garageyn_weight", "garagespaces_weight", "carportspaces_weight",
                         "parkingfeatures_weight", "stories_weight", "yearbuilt", "heating_weight",
                         "heatingyn_weight", "cooling_weight", "architecturalstyle_weight", "laundryfeatures_weight",
                         "parkname_weight", "accessibilityfeatures_weight", "poolfeatures_weight", "elementaryschool_weight",
                         "middleorjuniorschool_weight", "highschool_weight", "waterfrontyn_weight", "spayn_weight",
                         "taxannualamount", "taxyear", "securityfeatures_weight"]

rfeatures = ["ListPrice", "WaterSource_weight", "sewer_weight", "BedroomsTotal", "BathroomsFull", "CloseDate",
             "LivingArea", "GarageYN_weight", "CarportSpaces_weight",
             "CarportYN_weight", "ParkingFeatures_weight", "OtherParking_weight", "ParkingTotal_weight",
             "storiestotal_weight", "Levels_weight", "YearBuilt", "HeatingYN_weight", "coolingYN_weight", "InteriorFeatures_weight",
             "ExteriorFeatures_weight", "PatioAndPorchFeatures_weight", "WindowFeatures_weight", "Roof_weight",
             "ConstructionMaterials_weight", "LaundryFeatures_weight", "SecurityFeatures_weight", "PoolFeatures_weight", "PoolPrivateYN_weight",
             "SpaYN_weight", "ElementarySchool_weight", "MiddleOrJuniorSchool_weight", "HighSchool_weight", "WaterfrontYN_weight",
             "Latitude", "Longitude"]

rfeatures_filter = {"_common_filter": {"$ne": None, "$gte": 0},
                    "ListPrice": {"$gt": 10000},
                    "LivingArea": {"$gt": 100},
                    }

features_regression_model = ["Latitude", "Longitude", "CloseDate",
                             "WaterSource_weight", "BedroomsTotal", "BathroomsFull", "ListPrice", "LivingArea",
                             "ParkingFeatures_weight", "YearBuilt", "Heating_weight",
                             "HeatingYN_weight", "Cooling_weight", "ArchitecturalStyle_weight", "LaundryFeatures_weight", "AccessibilityFeatures_weight", "PoolFeatures_weight", "ElementarySchool_weight",
                             "MiddleOrJuniorSchool_weight", "HighSchool_weight", "WaterfrontYN_weight", "SpaYN_weight",
                             "TaxAnnualAmount", "SecurityFeatures_weight"]

features_regression_model_lexp = ["Latitude", "Longitude", "ModificationTimestamp",
                                  "WaterSource_weight", "BedroomsTotal", "BathroomsFull", "ListPrice", "LivingArea",
                                  "ParkingFeatures_weight", "YearBuilt", "Heating_weight",
                                  "HeatingYN_weight", "Cooling_weight", "ArchitecturalStyle_weight", "LaundryFeatures_weight", "AccessibilityFeatures_weight", "PoolFeatures_weight", "ElementarySchool_weight",
                                  "MiddleOrJuniorSchool_weight", "HighSchool_weight", "WaterfrontYN_weight", "SpaYN_weight",
                                  "TaxAnnualAmount", "SecurityFeatures_weight"]

features_mlslite = ["Latitude", "Longitude", "BedroomsTotal", "BathroomsTotalInteger", "CloseDate", "ListPrice", "LivingArea", "YearBuilt"]
