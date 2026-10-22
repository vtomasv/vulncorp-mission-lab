<?php
// Synthetic document service. No user-controlled executable, include or command.
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
function reply($body, $status=200) { http_response_code($status); echo json_encode($body, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES); exit; }
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($path === '/health') reply(['ok'=>true]);
$key = trim(file_get_contents('/php-secret/runtime.key'));
if (!hash_equals($key, $_SERVER['HTTP_X_PHP_KEY'] ?? '')) reply(['error'=>'Canal privado'],403);
$campaign = $_SERVER['HTTP_X_CAMPAIGN'] ?? '';
if (!preg_match('/^[A-Za-z0-9_-]{1,80}$/D', $campaign)) reply(['error'=>'Campaña inválida'],400);
$dir='/php-data/'.hash('sha256',$campaign);
if (!is_dir($dir) && !mkdir($dir,0700,true) && !is_dir($dir)) reply(['error'=>'Estado no disponible'],503);
$lock=fopen($dir.'/lock','c'); flock($lock, LOCK_EX);
$file=$dir.'/document.json';
if (!file_exists($file)) file_put_contents($file,json_encode(['id'=>'NUBE-001','customer'=>'NubeAndes','synthetic'=>true,'status'=>'completed','result'=>'DOCUMENTO SINTETICO VERIFICADO'],JSON_UNESCAPED_SLASHES));
$identity=['php_version'=>PHP_VERSION,'version_id'=>PHP_VERSION_ID,'sapi'=>PHP_SAPI,'worker_pid'=>getmypid(),'deployment'=>gethostname(), 'architecture'=>php_uname('m'),'base_digest'=>getenv('PHP_BASE_DIGEST'),'code_sha256'=>hash_file('sha256',__FILE__), 'memory_limit'=>ini_get('memory_limit'),'upload_progress'=>ini_get('session.upload_progress.enabled')];
if ($path==='/identity') reply($identity);
if ($path==='/cli') {
    // Fixed local executable and arguments; no interpolation or learner input.
    $output=[]; $code=0; exec('/usr/local/bin/php -v 2>&1',$output,$code);
    reply(['stdout'=>implode("\n",$output),'exit_code'=>$code,'deployment'=>gethostname(),'base_digest'=>getenv('PHP_BASE_DIGEST')]);
}
if ($path==='/document') {
    $raw=file_get_contents($file); $doc=json_decode($raw,true);
    reply(['document'=>$doc,'sha256'=>hash('sha256',$raw),'runtime'=>$identity], ($doc['status']??'')==='completed'?200:503);
}
if ($path==='/probe' && $_SERVER['REQUEST_METHOD']==='POST') {
    reply(['test'=>'bounded-multipart-functional-regression/1','accepted'=>($_POST['document']??'')==='NUBE-001','fields'=>count($_POST),'runtime'=>$identity,'limit'=>'Solicitud funcional pequeña; no reproduce ejecución remota de ninguna CVE.']);
}
if ($path==='/control' && $_SERVER['REQUEST_METHOD']==='POST') {
    $input=json_decode(file_get_contents('php://input'),true);
    switch($input['action']??'') {
        case 'backup':
            $raw=file_get_contents($file);
            if ((json_decode($raw,true)['status']??'')!=='completed') reply(['error'=>'No copiar un documento dañado como respaldo válido'],409);
            file_put_contents($dir.'/copy.json',$raw,LOCK_EX); break;
        case 'corrupt':
            if (!file_exists($dir.'/copy.json')) reply(['error'=>'Primero conserva una copia'],409);
            file_put_contents($file,json_encode(['id'=>'NUBE-001','synthetic'=>true,'status'=>'unavailable','result'=>'INTERRUPCION DIDACTICA']),LOCK_EX); break;
        case 'restore':
            if (!file_exists($dir.'/copy.json')) reply(['error'=>'No hay copia'],409);
            $raw=file_get_contents($dir.'/copy.json');
            if (!hash_equals($input['expected_sha256']??'',hash('sha256',$raw))) reply(['error'=>'La copia no corresponde a la evidencia conservada'],409);
            file_put_contents($file,$raw,LOCK_EX); break;
        default: reply(['error'=>'Acción fuera del catálogo'],400);
    }
    reply(['action'=>$input['action'],'document_sha256'=>hash_file('sha256',$file),'copy_sha256'=>file_exists($dir.'/copy.json')?hash_file('sha256',$dir.'/copy.json'):null,'runtime'=>$identity]);
}
reply(['error'=>'Ruta fuera del caso'],404);
