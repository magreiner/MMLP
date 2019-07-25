module.exports = {
  devServer: {
    disableHostCheck: true,
    key: 'cert/privkey.pem',
    cert: 'cert/cert.pem',
    ca: 'cert/fullchain.pem'
  }
}
