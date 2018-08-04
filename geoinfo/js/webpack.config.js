var path = require( 'path' );
//var ExtractTextPlugin = require("extract-text-webpack-plugin");
//const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

var webpack = require('webpack')

module.exports =
{
    //context:__dirname,
    entry: {
        geoinfo: './main.js',
    },
    output: {
        path:path.resolve(__dirname, '../static/js'),
        filename: '[name].pack.js'
    },

    watch: true,
    //resolve:{
    //    modules:["D:/coblan/webcode/node_modules"],
    //},
    resolveLoader: {
        //moduleExtensions:["D:/coblan/webcode/node_modules"],
        modules: ["D:/coblan/webcode/node_modules"],
        //resolver:["D:/coblan/webcode/node_modules"],
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                loader:'babel-loader',
                //loader: 'babel', // 'babel-loader' is also a legal name to reference
                query: {
                    presets: ['es2015'],
                }
            },
            {
                test: /\.scss$/,
                use: [{
                    loader: "style-loader" // creates style nodes from JS strings
                }, {
                    loader: "css-loader" // translates CSS into CommonJS
                }, {
                    loader: "sass-loader" // compiles Sass to CSS
                }]
            }
        ],
        //rules: [{
        //	test: /\.scss$/,
        //	use: [{
        //		loader: "style-loader" // creates style nodes from JS strings
        //	}, {
        //		loader: "css-loader" // translates CSS into CommonJS
        //	}, {
        //		loader: "sass-loader" // compiles Sass to CSS
        //	}]
        //}]

    },
    plugins: [
        //new webpack.optimize.UglifyJsPlugin({  //压缩包
         //    compress: {
         //      warnings: false
         //    },
         //   sourceMap: true,
         //   mangle: false
        //}),



        //new UglifyJSPlugin()
        //new webpack.DefinePlugin({
            //'process.env.NODE_ENV': JSON.stringify('production'),
        //}),
    ]
}



