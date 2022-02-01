
const autoprefixer = require('autoprefixer');
const browserSync = require('browser-sync').create();
const cleanCSS = require('gulp-clean-css');
const gulp = require('gulp');
const historyFallback = require('connect-history-api-fallback');
const JavaScriptObfuscator = require('webpack-obfuscator');
const postcss = require('gulp-postcss');
const sass = require('gulp-sass')(require('sass'));
const webpack = require('webpack-stream');

const dist = '../app/static';
const prod = '../app/static';

gulp.task('copy-html', () => {
  return gulp.src('./app/src/index.html')
    .pipe(gulp.dest(dist))
    .pipe(browserSync.stream());
});

gulp.task('build-js', () => {
  return gulp.src('./app/src/main.js')
    .pipe(webpack({
      mode: 'development',
      output: {
        filename: 'script.js'
      },
      watch: false,
      devtool: 'source-map',
      module: {
        rules: [
          {
            test: /\.scss$/,
            use: [
              'style-loader',
              'css-loader',
              'sass-loader'
            ]
          },
          {
            test: /\.css$/,
            use: [
              'style-loader',
              'css-loader'
            ]
          },
          {
            test: /\.m?js$/,
            exclude: /(node_modules|bower_components)/,
            use: {
              loader: 'babel-loader',
              options: {
                presets: [['@babel/preset-env', {
                  debug: false,
                  corejs: 3,
                  useBuiltIns: 'usage'
                }],
                  '@babel/react']
              }
            }
          }
        ]
      }
    }))
    .pipe(gulp.dest(dist))
    .pipe(browserSync.stream());
});

gulp.task('build-sass', () => {
  return gulp.src('./app/scss/style.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(postcss([autoprefixer()]))
    .pipe(cleanCSS())
    .pipe(gulp.dest(dist))
    .pipe(browserSync.stream());
});

gulp.task('copy-static', () => {
  return gulp.src('./app/static/**/*.*')
    .pipe(gulp.dest(dist))
    .pipe(browserSync.stream());
});


gulp.task('watch', () => {
  browserSync.init({
    server: {
      baseDir: dist,
      middleware: [
        historyFallback()
      ]
    }
  });

  gulp.watch('./app/src/index.html', gulp.parallel('copy-html')).on('change', browserSync.reload);
  gulp.watch('./app/static/**/*.*', gulp.parallel('copy-static')).on('change', browserSync.reload);
  gulp.watch('./app/scss/**/*.scss', gulp.parallel('build-sass')).on('change', browserSync.reload);
  gulp.watch('./app/src/**/*.js', gulp.parallel('build-js')).on('change', browserSync.reload);
});

gulp.task('build', gulp.parallel('copy-html', 'copy-static', 'build-sass', 'build-js'));

gulp.task('prod', () => {
  gulp.src('./app/src/index.html')
    .pipe(gulp.dest(prod));
  gulp.src('./app/static/**/*.*')
    .pipe(gulp.dest(prod));

  gulp.src('./app/src/main.js')
    .pipe(webpack({
      mode: 'production',
      output: {
        filename: 'script.js'
      },
      module: {
        rules: [
          {
            test: /\.scss$/,
            use: [
              'style-loader',
              'css-loader',
              'sass-loader'
            ]
          },
          {
            test: /\.css$/,
            use: [
              'style-loader',
              'css-loader'
            ]
          },
          {
            test: /\.m?js$/,
            exclude: /(node_modules|bower_components)/,
            use: {
              loader: 'babel-loader',
              options: {
                presets: [['@babel/preset-env', {
                  debug: false,
                  corejs: 3,
                  useBuiltIns: 'usage'
                }],
                  '@babel/react']
              }
            }
          }
        ]
      },
      plugins: [
        new JavaScriptObfuscator({
          rotateUnicodeArray: true
        }, ['excluded_bundle_name.js']),
      ],
    }))
    .pipe(gulp.dest(prod));

  return gulp.src('./app/scss/style.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(postcss([autoprefixer()]))
    .pipe(cleanCSS())
    .pipe(gulp.dest(prod));
});

gulp.task('default', gulp.parallel('watch', 'build'));