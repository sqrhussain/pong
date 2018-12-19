function Router() {
  this.routes = {
    '': {'routeId': 'start-route', route: startRoute},
    '#play': {'routeId': 'game-route', route: gameRoute},
    '#end': {'routeId': 'game-end-route', route: gameEndRoute},
    '#highscore': {'routeId': 'highscore-route', route: highscoreRoute}
  };
  this.currentRoute = null;

  this.updateRoutes();

  var self = this;
  window.addEventListener('hashchange', function() {
    self.updateRoutes();
  }, false);
}

Router.prototype.getCurrentRoute = function() {
  var route = this.routes[window.location.hash];
  return route ? route : this.routes[''];
};

Router.prototype.hideAllRoutes = function() {
  var routeElements = document.getElementsByClassName('route');
  if (routeElements) {
    for (var i = 0; i < routeElements.length; i++) {
      routeElements[i].style.display = 'none';
    }
  }
};

Router.prototype.hideRoute = function(routeId) {
  var routeElement = document.getElementById(routeId);
  if (routeElement) {
    routeElement.style.display = 'none';
  }
};

Router.prototype.showRoute = function(routeId) {
  var routeElement = document.getElementById(routeId);
  if (routeElement) {
    routeElement.style.display = 'block';
  }
};

Router.prototype.updateRoutes = function() {
  this.currentRoute = this.getCurrentRoute();
  this.hideAllRoutes();
  this.showRoute(this.currentRoute.routeId);
  this.currentRoute.route();
};
