/* Dependency-free local preview, including the same custom 404 used by Pages. */
const http = require('http');
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
function createPreviewServer() {
  return http.createServer((req,res) => {
    let requested;
    try { requested=decodeURIComponent(req.url.split('?')[0]); }
    catch { res.writeHead(400); return res.end('Invalid URL'); }
    const local=path.resolve(root, '.'+(requested==='/'?'/index.html':requested));
    if(!local.startsWith(root+path.sep)){res.writeHead(403);return res.end();}
    const exists=fs.existsSync(local)&&fs.statSync(local).isFile();
    const file=exists?local:path.join(root,'404.html');
    const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.ico':'image/x-icon','.pdf':'application/pdf','.mp4':'video/mp4'};
    res.writeHead(exists?200:404,{'Content-Type':types[path.extname(file).toLowerCase()]||'application/octet-stream'});
    fs.createReadStream(file).pipe(res);
  });
}
module.exports={createPreviewServer};
if(require.main===module){
  const port=Number(process.argv[2])||8123;
  createPreviewServer().listen(port,'127.0.0.1',()=>console.log(`Preview: http://127.0.0.1:${port}`));
}
