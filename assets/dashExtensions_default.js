window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng, context) {
            return L.circleMarker(latlng); // sender a simple circle marker.
        },
        function1: function(feature, latlng, context) {
            return L.circleMarker(latlng); // sender a simple circle marker.
        }
    }
});