/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _polygon_com = __webpack_require__(1);

var polygon_com = _interopRequireWildcard(_polygon_com);

var _map_com = __webpack_require__(2);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

Vue.component('polygon-input', polygon_com.ploygon_editor);

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
var ploygon_editor = exports.ploygon_editor = {
    props: ['name', 'row', 'kw'],
    template: '<div>\n            <span v-if="row[name]"><i class="fa fa-map-o fa-2x" aria-hidden="true"></i></span>\n            <button @click="create_new()" title="\u65B0\u5EFA"><i class="fa fa-plus-square-o" aria-hidden="true"></i></button>\n            <button @click="edit()" title="\u7F16\u8F91"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>\n            <button @click="copy()">copy</button>\n            <button @click="paste()">paste</button>\n        </div>',
    methods: {
        create_new: function create_new() {
            //map.clearMap()

            drawer.show();
            drawer.create_polygon(function (polygon) {
                var poly_obj = drawer.insert_polygon(polygon);
                drawer.edit_polygon(poly_obj);
            });
            this.listn_submit();
        },
        edit: function edit() {
            drawer.show();
            if (this.row[this.name]) {
                var polygon = JSON.parse(this.row[this.name]);
                var poly_obj = drawer.insert_polygon(polygon);
                drawer.edit_polygon(poly_obj);
            }
            this.listn_submit();
        },
        listn_submit: function listn_submit() {
            var self = this;
            drawer.onsubmit = function (polygon) {
                var point_arr = ex.map(polygon, function (point) {
                    return [point.lng, point.lat];
                });
                self.row[self.name] = JSON.stringify(point_arr);
            };
        },
        copy: function copy() {
            localStorage.setItem('clip_polygon', this.row[this.name]);
            alert('复制成功!');
        },
        paste: function paste() {
            var clip_polygon = localStorage.getItem('clip_polygon');
            if (clip_polygon) {
                this.row[this.name] = clip_polygon;
            }
            alert('粘贴成功!');
        }
    }
};

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
/*分发页面的地图组件
 *
 * */

var map_com = exports.map_com = {
    template: "<div id=\"container\"></div>",
    mounted: function mounted() {
        var self = this;

        ex.load_css("http://cache.amap.com/lbs/static/main1119.css");

        //ex.load_js('https://webapi.amap.com/maps?v=1.3&key=您申请的key值&plugin=AMap.PolyEditor,AMap.CircleEditor,AMap.MouseTool',function(){
        //    ex.load_js('http://cache.amap.com/lbs/static/addToolbar.js',function(){
        self.init();
        //    })
        //})


        //ex.load_js("http://webapi.amap.com/maps?v=1.3&key=您申请的key值&plugin=AMap.PolyEditor,AMap.CircleEditor,AMap.MouseTool",function(){
        //    ex.load_js("http://cache.amap.com/lbs/static/addToolbar.js",function(){
        //        setTimeout(function(){
        //            self.init()
        //        },10)
        //
        //    })
        //
        //
        //})

    },
    data: function data() {
        return {
            ploygons: []
        };
    },
    methods: {
        on_init: function on_init(callback) {
            this.on_init_call = callback;
        },
        on_polygon_click: function on_polygon_click(callback) {
            this.on_polygon_click_callback = callback;
        },
        init: function init() {
            //this.editorTool,
            this.map = new AMap.Map(this.$el, {
                resizeEnable: true,
                center: [121.058274, 31.140793], //地图中心点
                zoom: 13 //地图显示的缩放级别
            });
            if (this.on_init_call) {
                this.on_init_call();
            }
            this.$emit('loaded', this);
        },
        insert_polygon: function insert_polygon(arr) {
            var self = this;
            var _polygon = new AMap.Polygon({
                map: this.map,
                path: arr,
                strokeOpacity: 1,
                fillOpacity: 0.2,
                strokeWeight: 1,
                strokeColor: "#000000",
                fillColor: "#f5deb3"
            });
            this.ploygons.push(_polygon);
            _polygon.on('click', function () {
                if (self.on_polygon_click_callback) {
                    self.on_polygon_click_callback(_polygon);
                }
            });
            return _polygon;
        },
        detach_polygon: function detach_polygon(poly) {
            poly.setMap(null);
        },
        add_polygon: function add_polygon(poly) {
            poly.setMap(this.map);
        },
        highlight_polygon: function highlight_polygon(poly, color) {
            color = color || 'red';
            poly.setOptions({
                fillColor: color,
                strokeWeight: 3,
                strokeColor: "#0000ff"
            });
        },
        remove_highlight_polygon: function remove_highlight_polygon(poly, color) {
            color = color || '#f5deb3';
            poly.setOptions({
                strokeWeight: 1,
                strokeColor: "#000000",
                fillColor: color
            });
        }

    }
};

Vue.component('com-map', map_com);

/***/ })
/******/ ]);