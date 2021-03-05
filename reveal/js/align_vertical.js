// Centered page with flexbox CSS3 new properties, as proposed by millermedeiros in issue 563
// https://github.com/hakimel/reveal.js/issues/563
function toArray(o) {
    return Array.prototype.slice.call(o);
}

toArray( document.querySelectorAll( '.reveal .slides section' ) ).forEach(function(slide){
    var outerWrapper = document.createElement('div');
    if ( window.location.search.match( /print-pdf/gi ) ) {
        // Some styles are only applied for PDF printing
        outerWrapper.style.cssText = 'display:flex; align-items:center; height:85%';
    }

    var wrapper = document.createElement('div');
    wrapper.className = "content";
    //wrapper.style.width = '100%';
    outerWrapper.appendChild(wrapper);

    toArray( slide.children ).forEach(wrapper.appendChild, wrapper);

    if ( window.location.search.match( /print-pdf/gi ) ) {
        // Some styles are only applied for PDF printing
        slide.style.height = '100%';
    }
    slide.appendChild(outerWrapper);
});
