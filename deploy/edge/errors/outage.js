(() => {
  const status = document.getElementById('status');
  const retry = document.getElementById('retry');
  status.hidden = false;
  document.getElementById('check-hint').textContent = 'Доступность проверяется автоматически';
  retry.hidden = false;
  // Navigate with GET: never reload/replay a failed POST or upload.
  retry.addEventListener('click', () => window.location.assign(window.location.href));
  const endpoint = window.location.pathname.startsWith('/ops') ? '/_edge/ready-ops' : '/_edge/ready';
  let attempts = 0;
  async function check() {
    if (document.hidden) { window.setTimeout(check, 15000); return; }
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 4000);
    try {
      const response = await fetch(endpoint, {cache: 'no-store', credentials: 'same-origin', signal: controller.signal});
      if (response.ok) {
        status.textContent = 'Сервис снова доступен. Можно открыть страницу.';
        status.classList.add('ready');
        return;
      }
      status.textContent = 'Сервис пока недоступен. Следующая проверка через 15 секунд.';
    } catch (_) {
      status.textContent = 'Не удалось связаться с сервисом. Проверим ещё раз через 15 секунд.';
    } finally { window.clearTimeout(timeout); }
    if (++attempts < 40) window.setTimeout(check, 15000);
    else status.textContent = 'Автопроверка завершена. Попробуйте открыть страницу позже.';
  }
  check();
})();
