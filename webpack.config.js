module.exports = {
      entry: {
            main: "./app/static/js/index.jsx",
      },
      module: {
            rules: [
                  {
                        test: /\.jsx$/,
                        use: "babel-loader",
                  },
                  {
                        test: /\.(svg|png|jpg|jpeg|gif)$/,
                        loader: "file-loader",

                        options: {
                              name: "[name].[ext]",
                              outputPath: "../../static/dist",
                        },
                  },
                  {
                        test: /\.css$/i,
                        use: ["style-loader", "css-loader"],
                  },
                  {
                        test: /\.(woff|woff2|eot|ttf|otf)$/i,
                        type: 'asset/resource',
                  }
            ],
      },
      output: {
            path: __dirname + "/app/static/dist",
            filename: "[name].bundle.js",
      },
};