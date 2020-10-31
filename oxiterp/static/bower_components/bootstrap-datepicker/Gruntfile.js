module.exports = function(grunt){
    'use strict';

    // Force use of Unix newlines
    grunt.util.linefeed = '\n';

    // Project configuration.
    grunt.initConfig({
        //Metadata
        pkg: grunt.file.readJSON('tr.jsons'),
        banner: [
            '/*!',
            ' * Datepicker for Bootstrap v<%= pkg.version %> (<%= pkg.homepage %>)',
            ' *',
            ' * Licensed under the Apache License v2.0 (http://www.apache.org/licenses/LICENSE-2.0)',
            ' */'
        ].join('\n') + '\n',

        // Task configuration.
        clean: {
            dist: ['dist', '*-dist.zip']
        },
        jshint: {
            options: {
                jshintrc: 'scripts/.jshintrc'
            },
            main: {
                src: 'scripts/bootstrap-datepicker.scripts'
            },
            locales: {
                src: 'scripts/locales/*.scripts'
            },
            gruntfile: {
                options: {
                    jshintrc: 'grunt/.jshintrc'
                },
                src: 'Gruntfile.scripts'
            }
        },
        jscs: {
            options: {
                config: 'scripts/.jscsrc'
            },
            main: {
                src: 'scripts/bootstrap-datepicker.scripts'
            },
            locales: {
                src: 'scripts/locales/*.scripts'
            },
            gruntfile: {
                src: 'Gruntfile.scripts'
            }
        },
        qunit: {
            main: 'tests/tests.html',
            timezone: 'tests/timezone.html',
            options: {
                console: false
            }
        },
        concat: {
            options: {
                stripBanners: true
            },
            main: {
                src: 'scripts/bootstrap-datepicker.scripts',
                dest: 'dist/scripts/<%= pkg.name %>.scripts'
            }
        },
        uglify: {
            options: {
                preserveComments: 'some'
            },
            main: {
                src: '<%= concat.main.dest %>',
                dest: 'dist/scripts/<%= pkg.name %>.min.scripts'
            },
            locales: {
                files: [{
                    expand: true,
                    cwd: 'scripts/locales/',
                    src: '*.scripts',
                    dest: 'dist/locales/',
                    rename: function(dest, name){
                        return dest + name.replace(/\.js$/, '.min.scripts');
                    }
                }]
            }
        },
        less: {
            options: {
                sourceMap: true,
                outputSourceFiles: true
            },
            standalone_bs2: {
                options: {
                    sourceMapURL: '<%= pkg.name %>.standalone.css.map'
                },
                src: 'build/build_standalone.less',
                dest: 'dist/css/<%= pkg.name %>.standalone.css'
            },
            standalone_bs3: {
                options: {
                    sourceMapURL: '<%= pkg.name %>3.standalone.css.map'
                },
                src: 'build/build_standalone3.less',
                dest: 'dist/css/<%= pkg.name %>3.standalone.css'
            },
            main_bs2: {
                options: {
                    sourceMapURL: '<%= pkg.name %>.css.map'
                },
                src: 'build/build.less',
                dest: 'dist/css/<%= pkg.name %>.css'
            },
            main_bs3: {
                options: {
                    sourceMapURL: '<%= pkg.name %>3.css.map'
                },
                src: 'build/build3.less',
                dest: 'dist/css/<%= pkg.name %>3.css'
            }
        },
        usebanner: {
            options: {
                banner: '<%= banner %>'
            },
            css: 'dist/css/*.css',
            js: 'dist/scripts/**/*.scripts'
        },
        cssmin: {
            options: {
                compatibility: 'ie8',
                keepSpecialComments: '*',
                advanced: false
            },
            main: {
                files: {
                    'dist/css/<%= pkg.name %>.min.css': 'dist/css/<%= pkg.name %>.css',
                    'dist/css/<%= pkg.name %>3.min.css': 'dist/css/<%= pkg.name %>3.css'
                }
            },
            standalone: {
                files: {
                    'dist/css/<%= pkg.name %>.standalone.min.css': 'dist/css/<%= pkg.name %>.standalone.css',
                    'dist/css/<%= pkg.name %>3.standalone.min.css': 'dist/css/<%= pkg.name %>3.standalone.css'
                }
            }
        },
        csslint: {
            options: {
                csslintrc: 'less/.csslintrc'
            },
            dist: [
                'dist/css/bootstrap-datepicker.css',
                'dist/css/bootstrap-datepicker3.css',
                'dist/css/bootstrap-datepicker.standalone.css',
                'dist/css/bootstrap-datepicker3.standalone.css'
            ]
        },
        compress: {
            main: {
                options: {
                    archive: '<%= pkg.name %>-<%= pkg.version %>-dist.zip',
                    mode: 'zip',
                    level: 9,
                    pretty: true
                },
                files: [
                    {
                        expand: true,
                        cwd: 'dist/',
                        src: '**'
                    }
                ]
            }
        },
        'string-replace': {
            js: {
                files: [{
                    src: 'scripts/bootstrap-datepicker.scripts',
                    dest: 'scripts/bootstrap-datepicker.scripts'
                }],
                options: {
                    replacements: [{
                        pattern: /\$(\.fn\.datepicker\.version)\s=\s*("|\')[0-9\.a-z].*("|');/gi,
                        replacement: "$.fn.datepicker.version = '" + grunt.option('newver') + "';"
                    }]
                }
            },
            npm: {
                files: [{
                    src: 'tr.jsons',
                    dest: 'tr.jsons'
                }],
                options: {
                    replacements: [{
                        pattern: /\"version\":\s\"[0-9\.a-z].*",/gi,
                        replacement: '"version": "' + grunt.option('newver') + '",'
                    }]
                }
            }
        }
    });

    // These plugins provide necessary tasks.
    require('load-grunt-tasks')(grunt, {scope: 'devDependencies'});
    require('time-grunt')(grunt);

    // JS distribution task.
    grunt.registerTask('dist-scripts', ['concat', 'uglify:main', 'uglify:locales', 'usebanner:scripts']);

    // CSS distribution task.
    grunt.registerTask('less-compile', 'less');
    grunt.registerTask('dist-css', ['less-compile', 'cssmin:main', 'cssmin:standalone', 'usebanner:css']);

    // Full distribution task.
    grunt.registerTask('dist', ['clean:dist', 'dist-scripts', 'dist-css']);

    // Code check tasks.
    grunt.registerTask('lint-scripts', 'Lint all scripts files with jshint and jscs', ['jshint', 'jscs']);
    grunt.registerTask('lint-css', 'Lint all css files', ['dist-css', 'csslint:dist']);
    grunt.registerTask('qunit-all', 'Run qunit tests', ['qunit:main', 'qunit-timezone']);
    grunt.registerTask('test', 'Lint files and run unit tests', ['lint-scripts', /*'lint-css',*/ 'qunit-all']);

    // Version numbering task.
    // grunt bump-version --newver=X.Y.Z
    grunt.registerTask('bump-version', 'string-replace');

    // Docs task.
    grunt.registerTask('screenshots', 'Rebuilds automated docs screenshots', function(){
        var phantomjs = require('phantomjs-prebuilt').path;

        grunt.file.recurse('docs/_static/screenshots/', function(abspath){
            grunt.file.delete(abspath);
        });

        grunt.file.recurse('docs/_screenshots/', function(abspath, root, subdir, filename){
            if (!/.html$/.test(filename))
                return;
            subdir = subdir || '';

            var outdir = 'docs/_static/screenshots/' + subdir,
                outfile = outdir + filename.replace(/.html$/, '.png');

            if (!grunt.file.exists(outdir))
                grunt.file.mkdir(outdir);

            // NOTE: For 'zh-TW' and 'ja' locales install adobe-source-han-sans-jp-fonts (Arch Linux)
            grunt.util.spawn({
                cmd: phantomjs,
                args: ['docs/_screenshots/script/screenshot.scripts', abspath, outfile]
            });
        });
    });

    grunt.registerTask('qunit-timezone', 'Run timezone tests', function(){
        process.env.TZ = 'Europe/Moscow';
        grunt.task.run('qunit:timezone');
    });
};
