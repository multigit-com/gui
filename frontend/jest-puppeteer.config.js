module.exports = {
  launch: {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  },
  server: {
    command: 'npx http-server public -p 8080',
    port: 8080,
    launchTimeout: 10000,
    debug: true,
  },
}
