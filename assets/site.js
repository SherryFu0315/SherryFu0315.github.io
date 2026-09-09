/* The address is shown as "name [at] domain" so a scraper reading the HTML
   does not get a usable string. The href is assembled here, at view time, so
   the link still works for a person. Visible text is left alone on purpose. */
(function () {
  var links = document.querySelectorAll('a.mail');
  for (var i = 0; i < links.length; i++) {
    var a = links[i];
    var user = a.getAttribute('data-u');
    var dom = a.getAttribute('data-d');
    if (!user || !dom) continue;
    var href = 'mailto:' + user + String.fromCharCode(64) + dom;
    var q = [];
    if (a.getAttribute('data-s')) q.push('subject=' + encodeURIComponent(a.getAttribute('data-s')));
    if (a.getAttribute('data-b')) q.push('body=' + encodeURIComponent(a.getAttribute('data-b')));
    if (q.length) href += '?' + q.join('&');
    a.setAttribute('href', href);
  }
})();
