const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = (env, argv) => {
	const isDevelopment = argv.mode === 'development';

	return {
		mode: isDevelopment ? 'development' : 'production',
		entry: './src/index.js',
		output: {
			filename: isDevelopment ? '[name].js' : '[name].[contenthash].js',
			path: path.resolve(__dirname, 'dist'),
		},
		devtool: isDevelopment ? 'eval-source-map' : false,
		devServer: {
			host: '0.0.0.0',
			hot: true,
			port: 3000,
			compress: false,
		},
		watchOptions: {
			poll: 1000
		},
		module: {
			rules: [
				{
					test: /\.js$/,
					exclude: /node_modules/,
					use: {
						loader: 'babel-loader',
						options: {
							presets: [
								['@babel/preset-env', { targets: { node: 'current' } }],
								'@babel/preset-react',
							],
						},
					},
				},
			],
		},
		plugins: [
			new HtmlWebpackPlugin({
				template: './public/index.html',
			}),
		],
		optimization: {
			splitChunks: {
				chunks: 'all',
			},
		},
		performance: {
			hints: isDevelopment ? false : 'warning',
		},
	};
};