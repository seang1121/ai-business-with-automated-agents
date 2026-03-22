/* AI Business Agents — Dashboard JS */

// Auto-refresh dashboard every 30 seconds
(function() {
  const isDashboard = document.querySelector('.dashboard-grid');
  if (isDashboard) {
    setTimeout(function() {
      window.location.reload();
    }, 30000);
  }
})();
