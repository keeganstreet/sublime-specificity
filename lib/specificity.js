#!/usr/bin/env node

/*globals require, process, console */

(function () {

	'use strict';

	var program = require('commander'),
		specificity = require('specificity'),
		// Parse user input. Separate selectors by commas and line breaks
		parseList = function (val) {
			var array = val.split(/[\n,]/),
				result = [],
				i, len, item;
			for (i = 0, len = array.length; i < len; i += 1) {
				item = array[i].trim();
				if (item.length > 0) {
					if (item.indexOf("{") !== -1) {
						item = item.substr(0, item.indexOf("{")).trim();
					}
					result.push(item);
				}
			}
			return result;
		},
		i, len, result, output = '';

	// Initialise CLI
	program
		.version('0.0.1')
		.option('-s, --selectors <string>', 'Comma or line break separated list of CSS selectors', parseList)
		.parse(process.argv);

	// Show the help if no arguments were provided
	if (!process.argv.length) {
		program.help();
		return;
	}

	if (!program.selectors) {
		console.log('The --selectors argument is required.');
		return;
	}

	// Loop through each selector and calculate its specificity
	for (i = 0, len = program.selectors.length; i < len; i += 1) {
		result = specificity.calculate(program.selectors[i]);
		output += result[0].selector + ' - [' + result[0].specificity + ']';
		if (i < len - 1) {
			output += '\n';
		}
	}
	console.log(output);
}());
