// Platform bar
var platform_bar = '<div class="botbar"><h1 class="bottitle">' + bot_title + '</h1><image class="logo" src="images/'+bot_logo+'"></div>';
if ( window.location.search.match( /print-pdf/gi ) ) {
    $('section').append(platform_bar);
}
else {
    $('div.reveal').append(platform_bar);
}