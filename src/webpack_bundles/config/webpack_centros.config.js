var path = require('path')
var webpack = require('webpack')
var PrerenderSPAPlugin = require('prerender-spa-plugin')
const Renderer = PrerenderSPAPlugin.PuppeteerRenderer
var BundleTracker = require('webpack-bundle-tracker')
const VueLoaderPlugin = require('vue-loader/lib/plugin')


module.exports = {
  context: path.resolve(__dirname, '../../'),
  entry: './webpack_bundles/bundles/appcentroseducativos/main.js',
  output: {
    path: path.resolve(__dirname, '../../static/js/webpack_dist'),
    publicPath: '/static/js/webpack_dist/',
    filename: 'buildcentroseducativos.js'
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.(scss|css)$/,
        use: ["vue-style-loader", "css-loader", "sass-loader"]
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        resourceQuery: /blockType=i18n/,
        type: 'javascript/auto',
        loader: '@intlify/vue-i18n-loader'
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      '$styles': path.resolve('src/assets/styles'),

    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true
  },
  performance: {
    hints: false
  },
  devtool: 'eval-source-map',
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new VueLoaderPlugin()
  ]
}

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = 'source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    }),

    // == PRERENDER SPA PLUGIN == //
    new PrerenderSPAPlugin({
      // Index.html is in the root directory.
      staticDir: path.join(__dirname),
      routes: [ '/' ],
      outputDir: path.join(__dirname, 'prerendered'),
      // Optional minification.
      minify: {
        collapseBooleanAttributes: true,
        collapseWhitespace: true,
        decodeEntities: true,
        keepClosingSlash: true,
        sortAttributes: true
      },
      renderer: new Renderer({
        renderAfterDocumentEvent: 'render-event'
      })
    })
  ])
}
