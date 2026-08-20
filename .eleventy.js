module.exports = function(eleventyConfig) {
  // Copy assets folder to output
  eleventyConfig.addPassthroughCopy('assets');
  eleventyConfig.addPassthroughCopy('book');
  eleventyConfig.addPassthroughCopy('*.png');
  eleventyConfig.addPassthroughCopy('*.webp');
  eleventyConfig.addPassthroughCopy('*.ico');
  eleventyConfig.addPassthroughCopy('*.xml');
  eleventyConfig.addPassthroughCopy('*.txt');
  eleventyConfig.addPassthroughCopy('manifest.json');
  eleventyConfig.addPassthroughCopy('sw.js');

  // Keep your existing _includes and _layouts structure
  return {
    dir: {
      input: '.',
      output: '_site',
      includes: '_includes',
      layouts: '_layouts'
    },
    htmlTemplateEngine: 'liquid'
  };
};